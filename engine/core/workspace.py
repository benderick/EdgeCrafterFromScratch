import inspect # 系统库，它提供一些探查某个对象是不是函数是不是类的谓词

REGISTRY = {} # 这个是我们的全局注册表，类型是字典

def register(foo):
    """
    1. 这是一个装饰器函数，接受一个参数 foo，可以是函数或者类
    2. 它会将 foo 注册到 REGISTRY 中，注册的方式是根据 foo 的类型来决定的：
    - 如果 foo 是一个函数，那么直接将 foo 的名字作为键，foo 本身作为值存入 REGISTRY
    - 如果 foo 是一个类，那么将 foo 的名字作为键，值是一个字典，包含了类的名字和它所在的模块路径
    3. 如果 foo 既不是函数也不是类，那么抛出一个 ValueError 异常，说明不支持这种类型的注册
    4. 不能注册重名对象，会抛出断言错误
    """
    register_name = foo.__name__

    assert foo.__name__ not in REGISTRY, \
            f'{foo.__name__} 已被注册，不能重复注册同名对象'

    if inspect.isfunction(foo):
        REGISTRY[foo.__name__] = foo
    elif inspect.isclass(foo):
        REGISTRY[register_name] = {
            '_name': foo.__name__,
            '_pymodule': f"{foo.__module__}.{foo.__name__}"
    }
    else:
        raise ValueError(f'不支持 {type(foo)} 类型的注册')

    return foo
