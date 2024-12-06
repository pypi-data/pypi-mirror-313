from django.conf import settings

from tinyturret.base_settings import BASE_TINY_TURRET_SETTINGS


TINY_TURRET_SETTINGS = BASE_TINY_TURRET_SETTINGS
TINY_TURRET_SETTINGS.update(
    getattr(settings, 'TINY_TURRET_SETTINGS', {})
)
SHOW_ADMIN_LINK = getattr(settings, 'TINY_TURRET_SHOW_ADMIN_LINK', False)

MIDDLEWARE = [
    'tinyturret.middleware.DjangoExceptionMiddleware'
] + getattr(settings, 'MIDDLEWARE', [])
