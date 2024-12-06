"""Custom decorators."""
from retry import retry

from t_office_365.exceptions import BadRequestError, UnexpectedError


def retry_if_exception(func):
    """Retry the function if it raises a BadRequestError or an UnexpectedError."""
    tries = 3
    backoff = 2
    delay = 1

    @retry(exceptions=(BadRequestError, UnexpectedError), tries=tries, delay=delay, backoff=backoff)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
