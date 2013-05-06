from functools import wraps


class CommandRegistry(object):
    def __init__(self):
        self.registry = {}

    def register(self, name, description, help_message, usage):
        def decorator_wrapper(func):
            self.registry[name] = {
                'entry_point': func,
                'description': description,
                'help_message': help_message,
                'usage': usage,
            }

            @wraps(func)
            def decorated_apply(*args, **kwargs):
                return func(*args, **kwargs)

            return decorated_apply

        return decorator_wrapper

    def get_command_entry_point(self, name):
        return self.registry[name]['entry_point']


command_registry = CommandRegistry()
