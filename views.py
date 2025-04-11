import json
import logging
import requests

from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.conf import settings
from django.views.decorators.cache import cache_page
from .models import Movie, User
from django.contrib.auth.decorators import login_required


User = get_user_model()
logger = logging.getLogger(__name__)

# Constants (лучше вынести в settings.py)
PAGINATION_PER_PAGE = getattr(settings, 'PAGINATION_PER_PAGE', 10)
API_TIMEOUT = getattr(settings, 'API_TIMEOUT', 10)


@ensure_csrf_cookie
@require_http_methods(["GET"])
def login_view_page(request):
    """Страница входа"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'registration/login.html')


@csrf_exempt
@ensure_csrf_cookie
@require_http_methods(["POST"])
def login(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()  # Обратите внимание - теперь email вместо username
        password = data.get('password', '').strip()

        if not email or not password:
            return JsonResponse({"error": "Email и пароль обязательны"}, status=400)

        # Ищем пользователя по email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "Неверные учетные данные"}, status=401)

        user = authenticate(request, username=user.username, password=password)

        if user is None:
            return JsonResponse({"error": "Неверные учетные данные"}, status=401)

        auth_login(request, user)

        response = JsonResponse({
            "message": "Вход выполнен успешно",
            "user": {"id": user.id, "email": user.email}
        })

        response.set_cookie(
            "sessionid",
            request.session.session_key,
            httponly=True,
            samesite="Lax",
            secure=False,  # True если используете HTTPS
            max_age=60 * 60 * 24 * 7
        )

        return response

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return JsonResponse({"error": "Внутренняя ошибка сервера"}, status=500)



@ensure_csrf_cookie
def csrf_view(request):
    """View для получения CSRF токена"""
    token = get_token(request)
    response = JsonResponse({'detail': 'CSRF cookie set', 'token': token})
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response


def home(request):
    """Главная страница"""
    if not request.user.is_authenticated:
        return redirect('login_page')
    return render(request, 'home.html')


@ensure_csrf_cookie
@require_http_methods(["GET"])
def registration_view(request):
    """Страница регистрации"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'registration/register.html')


@csrf_protect
@require_http_methods(["POST"])
def register(request):
    """Улучшенная функция регистрации"""
    response_data = {
        'status': 'error',
        'message': '',
        'data': None
    }

    try:
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            email = data.get('email', '').strip().lower() or None
        except Exception as e:
            logger.error(f"Ошибка парсинга: {str(e)}")
            response_data['message'] = 'Неверный формат запроса'
            return JsonResponse(response_data, status=400)

        errors = []
        if not username:
            errors.append('Требуется имя пользователя')
        elif len(username) < 4:
            errors.append('Имя пользователя слишком короткое (минимум 4 символа)')
        elif User.objects.filter(username__iexact=username).exists():
            errors.append('Имя пользователя уже занято')

        if not password:
            errors.append('Требуется пароль')
        elif len(password) < 8:
            errors.append('Пароль слишком короткий (минимум 8 символов)')

        if email and User.objects.filter(email__iexact=email).exists():
            errors.append('Email уже зарегистрирован')

        if errors:
            response_data['message'] = ', '.join(errors)
            return JsonResponse(response_data, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        auth_login(request, user)

        response = JsonResponse({
            'status': 'success',
            'message': 'Регистрация прошла успешно',
            'data': {
                'user_id': user.id,
                'username': user.username
            }
        })
        response["Access-Control-Allow-Origin"] = settings.ALLOWED_CORS_ORIGINS
        response["Access-Control-Allow-Credentials"] = "true"
        return response

    except IntegrityError as e:
        logger.error(f"Ошибка целостности данных: {str(e)}")
        response_data['message'] = 'Ошибка базы данных'
        return JsonResponse(response_data, status=500)

    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {str(e)}", exc_info=True)
        response_data['message'] = 'Внутренняя ошибка сервера'
        return JsonResponse(response_data, status=500)


@cache_page(60 * 15)
@require_http_methods(["GET"])
def search_movies(request):
    """Поиск фильмов через API Кинопоиска"""
    query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page', 1)
    context = {'query': query}

    if query:
        try:
            response = requests.get(
                f'{settings.KINOPOISK_API_BASE_URL}/movie',
                headers={
                    'X-API-KEY': settings.KINOPOISK_API_KEY,
                    'Accept': 'application/json'
                },
                params={
                    'query': query,
                    'page': page_number,
                    'limit': PAGINATION_PER_PAGE
                },
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()

            if 'docs' in data:
                paginator = Paginator(data['docs'], PAGINATION_PER_PAGE)
                page_obj = paginator.get_page(page_number)
                context['movies'] = page_obj
            else:
                context['error'] = 'Фильмы не найдены'

        except Exception as e:
            logger.error(f"Ошибка API Кинопоиска: {str(e)}")
            context['error'] = 'Ошибка при поиске фильмов'

    return render(request, 'movies/search_results.html', context)


@cache_page(60 * 30)
@require_http_methods(["GET"])
def movie_list(request):
    """Список фильмов из базы данных"""
    movies_list = Movie.objects.all().order_by('-rating')
    paginator = Paginator(movies_list, PAGINATION_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'movies/movie_list.html', {'movies': page_obj})


@require_http_methods(["GET"])
def movie_detail(request, movie_id):
    """Детальная страница фильма"""
    try:
        movie = Movie.objects.get(id=movie_id)
        reviews = movie.reviews.all().order_by('-created_at')
        return render(request, 'movies/movie_detail.html', {
            'movie': movie,
            'reviews': reviews
        })
    except Movie.DoesNotExist:
        logger.warning(f"Фильм с ID {movie_id} не найден")
        raise Http404("Фильм не найден")


def handler404(request, exception):
    """Обработчик 404 ошибок"""
    logger.warning(f"Страница не найдена: {request.path}")
    return render(request, '404.html', status=404)


@require_http_methods(["GET"])
@cache_page(60 * 15)
def kinopoisk_proxy(request):
    """Прокси-запросы к API Кинопоиска"""
    try:
        params = {
            'page': request.GET.get('page', 1),
            'limit': request.GET.get('limit', 10)
        }

        response = requests.get(
            settings.KINOPOISK_API_BASE_URL + '/movie',
            headers={
                'X-API-KEY': settings.KINOPOISK_API_KEY,
                'Accept': 'application/json'
            },
            params=params,
            timeout=API_TIMEOUT
        )
        response.raise_for_status()

        return JsonResponse(response.json())

    except Exception as e:
        logger.error(f"Ошибка API Кинопоиска: {str(e)}")
        return JsonResponse(
            {'error': 'Ошибка при получении данных о фильмах'},
            status=502
        )


@login_required
def profile_view(request):
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
        'full_name': user.get_full_name(),
        'avatar': user.avatar.url if user.avatar else None,
        'phone': user.phone,
        'bio': user.bio,
        'date_joined': user.date_joined.strftime('%Y-%m-%d'),
    }
    return JsonResponse(data)


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.bio = data.get('bio', user.bio)

        # Обработка аватара (если нужно)
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)