from functools import wraps
from flask_login import current_user


def login_required(func):
    @wraps(func)
    def wrapper(self, *args):
        if current_user is None or not current_user.is_authenticated:
            return self.response_401()
        else:
            return func(self, *args)

    return wrapper
