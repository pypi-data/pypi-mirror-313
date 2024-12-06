import os

try:
    import django
    has_django = True
except ImportError:
    has_django = False

from .base_settings import BASE_TINY_TURRET_SETTINGS


TINY_TURRET_SETTINGS = BASE_TINY_TURRET_SETTINGS


if has_django:
    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tinyturret.base_settings'

    from django.conf import settings as djsettings

    if hasattr(djsettings, "TINY_TURRET_SETTINGS"):
        TINY_TURRET_SETTINGS.update(djsettings.TINY_TURRET_SETTINGS)

    SHOW_ADMIN_LINK = getattr(djsettings, 'TINY_TURRET_SHOW_ADMIN_LINK', False)

    TINY_TURRET_SETTINGS.update(
        getattr(djsettings, 'TINY_TURRET_SETTINGS', {})
    )

    MIDDLEWARE = [
        'tinyturret.middleware.DjangoExceptionMiddleware'
    ] + getattr(djsettings, 'MIDDLEWARE', [])
