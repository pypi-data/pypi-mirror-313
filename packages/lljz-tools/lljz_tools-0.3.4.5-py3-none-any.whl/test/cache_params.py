# coding=utf-8

"""
@fileName       :   test_cache_params.py
@data           :   2024/12/2
@author         :   jiangmenggui@hosonsoft.com
"""
from lljz_tools.decorators import cache_with_params


@cache_with_params('a')
def func(a, /, b, c, d=7, *, e=7):
    print('call func', a, b, c, d)
    return a + b + c + d


class A:

    @cache_with_params('a')
    def f(self, a, b, c, d):
        print('call f')
        return a + b + c + d


if __name__ == '__main__':
    func(1, 2, 3, d=4, e=1)
    func(2, 3, 4, d=5, e=1)
    func(6, 7, 8, d=9, e=1)
    func(1, 3, 5, d=7, e=1)
    a = A()
    a.f([1], [2], [3], [5])
    a.f([1], [2], [3], [5])
    a.f([1], [2], [3], [5])
    pass
