from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from movies.views import csrf_view, handler404, register  # Добавлен импорт register

urlpatterns = [
    path('admin/', admin.site.urls),

    # Основные маршруты (views)
    path('', include('movies.urls')),

    # API endpoints
    path('api/', include('api.urls')),

    # CSRF endpoint (оставлен как есть для совместимости)
    path('api/csrf/', csrf_view, name='csrf_token'),

    path('api/csrf/', csrf_view, name='csrf'),

    # Явный маршрут для регистрации через API
    path('api/register/', register, name='api_register'),
]

# Добавляем обработку медиа файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обработчики ошибок
handler404 = handler404