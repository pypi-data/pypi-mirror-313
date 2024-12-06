import os

try:
    import django
    has_django = True
except ImportError:
    has_django = False


from tinyturret.base_settings import (
    BASE_TINY_TURRET_SETTINGS,
)


TINY_TURRET_SETTINGS = BASE_TINY_TURRET_SETTINGS


if has_django:
    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tinyturret.base_settings'

    from django.conf import settings
    if hasattr(settings, "TINY_TURRET_SETTINGS"):
        TINY_TURRET_SETTINGS.update(settings.TINY_TURRET_SETTINGS)


def apply_settings(settings_dict):
    global TINY_TURRET_SETTINGS
    TINY_TURRET_SETTINGS.update(settings_dict)
