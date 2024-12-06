from tinyturret.utils import (
    capture_exception,
    get_exception_groups,
    clear_storages,
)
import tinyturret


def test_basic_caputure():
    tinyturret.TINY_TURRET_SETTINGS['IGNORE_STORAGE_ERRORS'] = False
    clear_storages()

    try:
        return 1 / 0
    except Exception:
        capture_exception()

    for _ in range(10):
        try:
            return 5 / 0
        except Exception:
            capture_exception()

        infos = get_exception_groups()

    assert len(infos) == 2
    assert infos[0]['info']['error_count'] == 10
    assert infos[1]['info']['error_count'] == 1


# def test_sqlite():
#     tinyturret.TINY_TURRET_SETTINGS['IGNORE_STORAGE_ERRORS'] = False
#     clear_storages()

#     try:
#         return 1 / 0
#     except Exception:
#         capture_exception()

#     for _ in range(10):
#         try:
#             return 5 / 0
#         except Exception:
#             capture_exception()

#         infos = get_exception_groups()

#     assert len(infos) == 2
#     assert infos[0]['info']['error_count'] == 10
#     assert infos[1]['info']['error_count'] == 1
