import inspect


def assert_obj_has_method(obj, method_name: str, method_args: list):
    """
    Inspect if a class object defines method and if the defined method has proper arguments

    :param obj: a class object
    :param method_name: name of the inspected method
    :param method_args: list of argument names of the inspected method
    :return: None

    >>> def func(a, b, c):
    ...     pass
    >>> Foo = type('Foo', (), {'func': func})
    >>> assert_obj_has_method(obj=Foo(), method_name='func', method_args=['a', 'b', 'c'])

    """
    if not hasattr(obj, method_name):
        raise ValueError(
            f"{type(obj).__name__} object must define method '{method_name}'"
        )

    method = getattr(obj, method_name)
    train_args_names = inspect.getfullargspec(method).args
    if not train_args_names == method_args:
        raise ValueError(
            f"{method_name} method must have argument list: {method_args}"
        )


def assert_obj_has_attribute(obj, attr_name: str):
    """
    Inspect if a class object defines attribute and if the defined attribute is None

    :param obj: a class object
    :param attr_name: name of the inspected attribute
    :return: None

    >>> Foo = type('Foo', (), {'attr': 1})
    >>> assert_obj_has_attribute(obj=Foo(), attr_name='attr')
    """
    if not (hasattr(obj, attr_name) and getattr(obj, attr_name) is not None):
        raise ValueError(
            f"{type(obj).__name__} object must define attribute '{attr_name}'"
        )


def get_attr_by_path(obj, attr_path):
    """
    Enhanced built-in getattr with attribute path

    >>> class Bar:
    ...     attr = 1
    ...
    >>> class Foo:
    ...     bar = Bar()
    ...
    >>> foo = Foo()
    >>> get_attr_by_path(foo, 'bar.attr')
    1
    """
    for attr in attr_path.split('.'):
        obj = getattr(obj, attr)
    return obj


def attr_dict(obj, attrs):
    """
    Return a dict containing certain attributes of a object

    >>> class Bar:
    ...     attr = 1
    ...
    >>> class Foo:
    ...     bar = Bar()
    ...     attr = 2
    ...
    >>> foo = Foo()
    >>> attr_dict(foo, ['bar.attr', 'attr'])
    {'bar.attr': 1, 'attr': 2}
    """
    return {attr: get_attr_by_path(obj, attr) for attr in attrs}
