

class BaseExceptionStore:

    def __init__(self, settings):
        self.settings = settings
        self.MAX_EXCEPTIONS_PER_GROUP = settings.get('MAX_EXCEPTIONS_PER_GROUP', 100)
        self.MAX_EXCEPTION_GROUPS = settings.get('MAX_EXCEPTION_GROUPS', 100)

    def save_exception(self, group_key, group_struct, get_exc_struct):
        "Main entry point to save an exception."
        raise NotImplemented('Todo!')

    def get_group_list(self, limit=10):
        raise NotImplemented('Todo!')

    def get_exceptions(self, group_key):
        raise NotImplemented('Todo!')
