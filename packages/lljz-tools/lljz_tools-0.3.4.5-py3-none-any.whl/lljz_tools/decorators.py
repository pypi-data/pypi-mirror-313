# coding=utf-8
import datetime
import inspect
import threading
import time
import traceback
from functools import wraps
from typing import Callable, Any, Type

from lljz_tools.color import Color


def cache_with_params(*params: str):
    """
    缓存数据，根据传入的参数进行缓存
    :param params:
    :return:
    """

    def decorator(func: Callable):

        __cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取func的参数定义
            argspec = inspect.getfullargspec(func)
            call_values = dict(zip(argspec.args, args))
            call_values.update(kwargs)
            call_values.pop('self', None)
            call_values.pop('cls', None)
            if not params:
                key = tuple(sorted(call_values.items()))
            else:
                key = tuple(sorted(item for item in call_values.items() if item[0] in params))
            try:
                if key in __cache:
                    return __cache[key]
                __cache[key] = func(*args, **kwargs)
                return __cache[key]
            except TypeError as e:
                if str(e).startswith('unhashable type'):
                    print(Color.yellow(f"[WARNING]传入的值必须是可哈希才能使用缓存，无法缓存参数：{key}"))
                    return func(*args, **kwargs)
                else:
                    raise e

        return wrapper
    return decorator


def time_cache(__time: float, /):
    """
    给缓存数据设置超时时间，
    :param __time: 缓存时间
    :return:
    """
    __cache = {}

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, *args, *tuple(kwargs.items()))
            if key in __cache and time.time() - __cache[key][0] <= __time:
                return __cache[key][1]
            res = func(*args, **kwargs)
            __cache[key] = (time.time(), res)
            return res

        return wrapper

    return decorator


def timer(__loop=1):
    """
    函数运行计时，重复的运行函数多次，查看函数最终的运行时间
    :param __loop: 重复次数
    :return:
    """

    def outer(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f'function [{Color.yellow(func.__name__)}] start running at {datetime.datetime.now()}')
            start = time.perf_counter()
            res = None
            for _ in range(__loop):
                res = func(*args, **kwargs)
            end = time.perf_counter()
            print(f'function [{Color.yellow(func.__name__)}]      finished at {datetime.datetime.now()}, '
                  f'loop {Color.green(str(__loop))} times, use time {Color.cyan(f"{(end - start) * 1000:.4f}")} ms')
            return res

        return wrapper

    return outer


def catch_exception(
        exceptions: list[Type[Exception]] | Type[Exception] | None = None,
        print_exception: Any | Callable = traceback.print_exception,
        retry_times: int = 0,
        retry_interval: float = 0,  # unit second
):
    """
    自动捕获异常
    :param exceptions: 异常类，默认为Exception
    :param print_exception: 输出异常的方法，默认traceback.print_exception
    :param retry_times: 重试次数，0表示不重试，默认值0
    :param retry_interval: 重试间隔，默认值0，单位秒
    :return:
    """
    if not exceptions:
        exceptions = [Exception]
    elif not isinstance(exceptions, list | tuple | set):
        exceptions = [exceptions]

    def outer(func: Callable):
        @wraps(func)
        def inner(*args, **kwargs):
            for i in range(retry_times + 1):
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as e:

                    if i < retry_times:
                        print(
                            f'[{Color.yellow(func.__name__)}] {Color.magenta(e.__class__.__name__)}: '
                            f'{Color.red(str(e))}, {Color.green(f"retry {i + 1}/{retry_times}")}')
                        time.sleep(retry_interval)
                    else:
                        if callable(print_exception):
                            print_exception(e)

        return inner

    return outer


def retry(
        __retry: int = 1,
        /, *,
        interval: float = 0,  # unit second
        exceptions: list[Type[Exception]] | Type[Exception] | None = None,
):
    """
    自动重试（和catch_exception不同的在于最后一次没有成功不会捕获异常）
    :param __retry: 重试次数，0表示不重试，默认值1
    :param interval: 重试间隔，默认值0，单位秒
    :param exceptions: 异常类，默认为Exception，只有捕获到这个异常才会进行重试
    :return:
    """
    if not exceptions:
        exceptions = [Exception]
    elif not isinstance(exceptions, list | tuple | set):
        exceptions = [exceptions]

    def outer(func: Callable):
        @wraps(func)
        def inner(*args, **kwargs):
            for i in range(__retry):
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as e:
                    print(f'[{Color.yellow(func.__name__)}] {Color.magenta(e.__class__.__name__)}: '
                          f'{Color.red(str(e))}, {Color.green(f"retry {i + 1}/{__retry}")}')

                    time.sleep(interval)
            return func(*args, **kwargs)

        return inner

    return outer


def debug(func: Callable):
    """
    执行函数时，自动打印函数执行信息
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        def init_arg(arg: Any):
            arg = f'{arg!r}'
            if len(arg) > 50:
                arg = arg[:50] + '...'
            return arg

        args_str = (*map(lambda x: init_arg(x), args), *map(lambda x: f"{x[0]}={init_arg(x[1])}", kwargs.items()))
        _f_info = (f'{Color.yellow(func.__name__)}{Color.blue("(")}'
                   f'{", ".join(map(str, map(Color.green, map(str, args_str))))}{Color.blue(")")}')
        now = datetime.datetime.now()
        t = time.perf_counter()

        res = func(*args, **kwargs)
        print(
            f'function [{Color.yellow(func.__name__)}] execute info: \n'
            f'  execute :  {_f_info[:500]}\n'
            f' start at :  {now}'
        )
        print(
            f'finish at :  {datetime.datetime.now()}\n'
            f'   result :  {str(res)[:500]}\n'
            f' use time :  {Color.cyan(f"{(time.perf_counter() - t) * 1000:.4f}")} ms'
        )
        return res

    return wrapper


def singleton(cls: str | type = ''):
    """
    实现单例模式
    :param cls:
    :return:
    """
    _instance = {}
    lock = threading.Lock()  # noqa
    if isinstance(cls, str):
        def outer(cls_):
            @wraps(cls_)
            def inner(*args, **kwargs):
                with lock:
                    key = kwargs.get(cls, (str(args[0]) if args else None))
                    key = (cls_, key)
                    if key not in _instance:
                        _instance[key] = cls_(*args, **kwargs)
                    return _instance[key]

            return inner

        return outer
    else:

        @wraps(cls)
        def wrapper(*args, **kwargs):
            with lock:
                if cls not in _instance:
                    _instance[cls] = cls(*args, **kwargs)
                return _instance[cls]

        return wrapper


def count_call(func: Callable):
    """
    统计函数被调用的次数
    :param func:
    :return:
    """
    __attr = {'count': 0}

    @wraps(func)
    def wrapper(*args, **kwargs):
        __attr['count'] += 1
        result = func(*args, **kwargs)
        print(f'[{Color.thin_green(str(datetime.datetime.now())[:-3])}]'
              f'[{Color.yellow(func.__name__)}]已被调用了 {Color.green(str(__attr["count"]))} 次')
        return result

    return wrapper


def rate_limited(__max_called_pre_second: float = 1, /, *, auto_wait=False):
    """
    限制函数被调用的频率
    
    :param __max_called_pre_second: 每秒最大调用次数
    :param auto_wait: 是否自动等待，默认值为False
        - True表示自动等待，
        - False表示不等待，超过频率则会抛出异常
    :return:
    """
    if __max_called_pre_second <= 0:
        raise ValueError('__max_called_pre_second must > 0')

    __attr = {'last_called': None, "interval": 1 / __max_called_pre_second}

    def outer(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if not __attr['last_called']:
                __attr['last_called'] = now

            elif now - __attr['last_called'] < __attr['interval']:
                if auto_wait:
                    time.sleep(__attr['interval'] - (now - __attr['last_called']))
                else:
                    raise RuntimeError(
                        f'[{Color.yellow(func.__name__)}]调用过于频繁，'
                        f'每次调用间隔不得低于 {Color.green(f"{__attr["interval"]:.3f}")} 秒！'
                    )
            __attr['last_called'] = time.time()
            return func(*args, **kwargs)

        return wrapper

    return outer


def thread_lock(func: Callable):
    """
    一个装饰器函数，为被装饰的函数提供线程锁，确保该函数在多线程环境下的正确执行。

    参数:
    - func (Callable): 要被装饰，即添加线程锁功能的函数。

    返回值:
    - 返回一个封装了原函数的新函数，该新函数在执行原函数前会获取线程锁。
    """
    lock = threading.Lock()

    @wraps(func)
    def inner(*args, **kwargs):
        nonlocal lock
        # 在执行原函数前，尝试获取线程锁
        with lock:
            # 获取到锁后，执行原函数，并传递所有接收到的参数
            return func(*args, **kwargs)

    return inner


if __name__ == '__main__':
    # @rate_limited(5, auto_wait=False)
    @count_call
    @debug
    def test(*args, **kwargs):
        ...


    from pydantic import BaseModel


    class Cat(BaseModel):
        companyIds: list[int] = [1]
        status: str = '123'
        modelCode: str = 'dsadsf'
        materialCode: str = 'ffffqwfq'
        colorCode: str = 'ggggh'
        shellCode: str = 'hhhhhhhhhhhhhh'
        size: int = 50
        current: int = 1


    for i in range(1):
        test(1, 2, 'cat', Cat(), None, name='dog', age=Cat())
