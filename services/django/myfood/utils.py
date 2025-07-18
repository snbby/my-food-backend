import functools
from typing import Callable, Optional

def str2bool(some_str: str) -> bool:
    return some_str.lower() == 'true'


def _set_attributed_attrs(wrapper: Callable, label: Optional[str], **kwargs: dict) -> None:
    if label is not None:
        wrapper.label = label

    for key, value in kwargs.items():
        setattr(wrapper, key, value)


def attributed(label: str = None, **kwargs) -> Callable:
    """
    Admin fields and actions decorator.

    Allows easily specify label, short description and so on for callable.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> None:
            return func(*args, **kwargs)

        _set_attributed_attrs(wrapper, label, **kwargs)

        return wrapper

    return decorator

# Todo add to model maybe
def init_kwargs(model, arg_dict):
    model_fields = [f.name for f in model._meta.get_fields()]
    return {k: v for k, v in arg_dict.items() if k in model_fields}
        