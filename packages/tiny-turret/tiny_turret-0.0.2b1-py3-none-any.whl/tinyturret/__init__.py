from tinyturret.settings import (
    TINY_TURRET_SETTINGS,
)


def apply_settings(settings_dict):
    global TINY_TURRET_SETTINGS
    TINY_TURRET_SETTINGS.update(settings_dict)
