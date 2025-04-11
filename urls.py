from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from .views import profile_view, update_profile

from .views import (
    home,
    search_movies,
    movie_list,
    movie_detail,
    registration_view,
    login_view_page,
    register,
    login,
    csrf_view,  # Используем только csrf_view вместо get_csrf_token
    handler404,
    kinopoisk_proxy
)

# Константы для кэширования
CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 15)  # 15 минут по умолчанию

urlpatterns = [
    path('api/movies/', kinopoisk_proxy, name='kinopoisk_proxy'),
    path('', home, name='home'),

    # Movie routes
    path('search/',
         cache_page(CACHE_TTL)(search_movies),
         name='search_movies'),
    path('movies/',
         cache_page(CACHE_TTL * 2)(movie_list),
         name='movie_list'),
    path('movies/<int:movie_id>/',
         movie_detail,
         name='movie_detail'),

    # Auth routes
    path('register/',
         ensure_csrf_cookie(registration_view),
         name='register_page'),
    path('register/submit/',
         register,
         name='register_submit'),
    path('login/',
         ensure_csrf_cookie(login_view_page),
         name='login_page'),
    path('login/submit/',
         login,
         name='login_submit'),

    # CSRF route (объединенная)
    path('csrf/',
         csrf_view,
         name='csrf_token'),  # Используем единую точку для CSRF

    path('api/profile/', profile_view, name='profile'),

    path('api/profile/update/', update_profile, name='update_profile'),

]

# Обработчики ошибок
handler404 = handler404
handler500 = 'django.views.defaults.server_error'