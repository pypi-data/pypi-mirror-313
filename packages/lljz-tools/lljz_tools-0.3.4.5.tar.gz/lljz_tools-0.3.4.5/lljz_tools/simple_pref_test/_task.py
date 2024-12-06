# coding=utf-8

"""
@fileName       :   task.py
@data           :   2024/8/27
@author         :   jiangmenggui@hosonsoft.com
"""
import functools
import inspect
import random
import sys
import time
from types import FunctionType
from typing import Any, Callable, TypeVar

from lljz_tools import logger
from lljz_tools.client.http_client import HTTPClient
from lljz_tools.simple_pref_test.core import TaskResult, TaskResultSet
from lljz_tools.simple_pref_test.task_config import TaskConfig, TaskConfigGroup

T = TypeVar('T', bound=Callable)

def _task_on_function(func: T) -> T:
    task_name = func.__name__

    @functools.wraps(func)
    def inner(*args: Any, **kwargs: Any) -> Any:
        t1 = time.time()
        try:
            res = func(*args, **kwargs)
            t2 = time.time()
            TaskResultSet.put(TaskResult(name=task_name, start=t1, end=t2))
            return res
        except AssertionError as e:
            t2 = time.time()
            TaskResultSet.put(
                TaskResult(name=task_name, start=t1, end=t2, message=f'断言失败：{str(e)}', success=False))
            logger.error(f'{task_name}失败：{str(e)}', stacklevel=2)
        except Exception as e:
            t2 = time.time()
            TaskResultSet.put(TaskResult(
                name=task_name, start=t1, end=t2, message=f'{e.__class__.__name__}: {str(e)}', success=False
            ))
            logger.exception(f'{task_name}错误：{e}', stacklevel=2)

    setattr(inner, 'is_task', True)
    setattr(inner, 'weight', 1)
    setattr(inner, 'name', task_name)
    return inner  # type: ignore

def _task_on_name(name: str = '', weight: int = 1, recode_result: bool = True) -> Callable[[T], T]:
    if not isinstance(weight, int) or weight < 0:
        raise ValueError("任务权重（weight参数）必须为大于0的整数")

    def outer(func: T) -> T:
        task_name = name or func.__name__

        @functools.wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            t1 = time.time()
            try:
                res = func(*args, **kwargs)
                t2 = time.time()
                if recode_result:
                    TaskResultSet.put(TaskResult(name=task_name, start=t1, end=t2))
                return res
            except AssertionError as e:
                t2 = time.time()
                if recode_result:
                    TaskResultSet.put(
                        TaskResult(name=task_name, start=t1, end=t2, message=f'断言失败：{str(e)}', success=False))
                logger.error(f'{task_name}失败：{str(e)}', stacklevel=2)
            except Exception as e:
                t2 = time.time()
                if recode_result:
                    TaskResultSet.put(TaskResult(
                        name=task_name, start=t1, end=t2, message=f'{e.__class__.__name__}: {str(e)}', success=False
                    ))
                logger.exception(f'{task_name}错误：{e}', stacklevel=2)

        setattr(inner, 'is_task', True)
        setattr(inner, 'weight', weight)
        setattr(inner, 'name', task_name)
        return inner  # type: ignore

    return outer

def task(name: FunctionType | str = '', /, *, weight: int = 1, recode_result: bool = True):
    if isinstance(name, FunctionType):
        return _task_on_function(name)
    elif isinstance(name, str):
        return _task_on_name(name)
    else:
        raise TypeError(f'不支持的参数类型：{type(name)}')

# 只是用来标记task，不会记录最终的执行耗时结果
mark_task = functools.partial(task, recode_result=False)

class TaskSet:
    client: HTTPClient | None = None
    static: bool = True
    weight: int = 1
    task_config: TaskConfig | None = None
    task_config_group: TaskConfigGroup | None = None

    def __init__(self):
        self._task = []

    def setup_class(self):
        """执行所有任务前都会执行setup_class"""
        pass

    def teardown_class(self):
        """执行所有任务后都会执行teardown_class"""
        pass

    def setup(self, task_name: str):
        """
        每个任务执行前都会执行setup

        :param task_name: 任务名，可以根据__task_name判断需要执行的步骤
        """
        pass

    def teardown(self, task_name: str):
        """
        每个任务执行后都会执行teardown

        :param task_name: 任务名，可以根据__task_name判断需要执行的步骤

        """
        pass

    @property
    def tasks(self):
        if self._task:
            return self._task
        for k in self.__dir__():
            obj = getattr(self, k, None)

            if obj is None:
                continue
            if inspect.ismethod(obj) and getattr(obj, 'is_task', None) is True:
                for _ in range(getattr(obj, 'weight', 1)):
                    self._task.append(obj)
        random.shuffle(self._task)
        return self._task

class _TaskSetFunction:

    def __init__(self, task: Callable):
        self.tasks = [task]

    def setup_class(self):
        """执行所有任务前都会执行setup_class"""
        pass

    def teardown_class(self):
        """执行所有任务后都会执行teardown_class"""
        pass

    def setup(self, task_name: str):
        """
        每个任务执行前都会执行setup

        :param task_name: 任务名，可以根据__task_name判断需要执行的步骤
        """
        pass

    def teardown(self, task_name: str):
        """
        每个任务执行后都会执行teardown

        :param task_name: 任务名，可以根据__task_name判断需要执行的步骤
        """
        pass

class TaskGroup:
    """group中会初始化任务示例，初始化的时候会执行setup_class"""

    def __init__(self, task_group: list):
        self.data: list[TaskSet | _TaskSetFunction] = []
        for v in task_group:
            self.add_task(v)

    def add_task(self, __task):
        if inspect.isfunction(__task):
            instance = _TaskSetFunction(__task)
            self.data.extend(instance for _ in range(getattr(__task, 'weight', 1)))
        elif inspect.isclass(__task):
            instance = __task()
            instance.setup_class()
            self.data.extend(instance for _ in range(getattr(__task, 'weight', 1)))
        else:
            raise ValueError('任务必须为函数或者类')

    def get(self) -> TaskSet | _TaskSetFunction:
        return random.choice(self.data)

    def teardown_all(self):
        for t in set(self.data):
            t.teardown_class()

def find_tasks(*modules):
    modules = (*modules, sys.modules['__main__'])
    task_list = []
    for module in modules:
        for k, v in module.__dict__.items():
            if (inspect.isclass(v) and issubclass(v, TaskSet) and v.__dict__.get('static') is not True
                    or inspect.isfunction(v) and getattr(v, 'is_task', False)):
                task_list.append(v)

    return task_list

if __name__ == '__main__':
    pass
