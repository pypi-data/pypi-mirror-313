# Tiny Turret settings
BASE_TINY_TURRET_SETTINGS = {
    'MAX_EXCEPTION_PER_GROUP': 100,
    'MAX_EXCEPTION_GROUPS': 10,
    'CLEANUP_TRIGGER_RATE': 0.05,
    'IGNORE_STORAGE_ERRORS': True,
    'CAPTURE_LOCALS': False,
    'STORAGE_BACKENDS': [
        {
            'class': 'tinyturret.storage_backends.shelve_store.ShelveStore',
            'settings': {
                'path': '/tmp/'
            }
        }
    ]
}
