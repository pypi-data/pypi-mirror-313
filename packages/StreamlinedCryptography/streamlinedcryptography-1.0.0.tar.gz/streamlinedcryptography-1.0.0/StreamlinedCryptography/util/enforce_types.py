import inspect


def enforce_types():
    """
    A decorator which enforces a function's type annotations.

    Usage:
        @enforce_types()
        def func(string_value: str, int_value: int): pass # The annotations provided will be enforced.

    Raises:
        TypeError: If an argument does not match its annotated type.

    Notes:
        - Parameters without annotations are skipped.
        - Variadic parameters (*args, **kwargs) are not enforced.
    """

    def decorator(func):
        params = inspect.signature(func).parameters
        param_names = list(params.keys())

        def wrapper(*fargs, **fkwargs):
            for arg in range(min(len(fargs), len(param_names))):
                param = params[param_names[arg]]
                annotation = param.annotation

                if annotation == inspect.Parameter.empty:
                    continue

                if not isinstance(fargs[arg], param.annotation):
                    raise TypeError(f"Parameter {param_names[arg]} of {func.__name__} must be of type {annotation.__name__}")

            return func(*fargs, **fkwargs)
        return wrapper
    return decorator
