# coding=utf-8

"""
@fileName       :   compare.py
@data           :   2024/9/10
@author         :   jiangmenggui@hosonsoft.com
"""


def compare_dict(__a: dict, __b: dict, *ignore_keys: str):
    """
    比较两个字典，判断数据是否一致
    :param __a: 待比较的字典1
    :param __b: 待比较的字典2
    :param ignore_keys: 忽略比较的key
    :return:
    """
    keys = (set(__a.keys()) | set(__b.keys())) - set(ignore_keys)
    return {key: [__a.get(key), __b.get(key)] for key in keys if __a.get(key) != __b.get(key)}


def compare_table(__a: list[dict], __b: list[dict], *keys: str):
    print(__a == __b)
    if len(keys) == 0:
        raise TypeError('compare_table() missing 1 required positional argument: \'keys\'')
    a = sorted(__a, key=lambda x: tuple(x[k] for k in keys))
    b = sorted(__b, key=lambda x: tuple(x[k] for k in keys))
    i = j = 0
    result = []
    while i < len(a) and j < len(b):
        k1 = tuple(a[i][k] for k in keys)
        k2 = tuple(b[j][k] for k in keys)
        if k1 < k2:
            result.append({'type': 'missing', 'key': k1, 'value': a[i], 'message': '数据2中缺少数据'})
            i += 1
        elif k1 > k2:
            result.append({'type': 'missing', 'key': k2, 'value': b[j], 'message': '数据1中缺少数据'})
            j += 1
        else:
            dif = compare_dict(a[i], b[j])
            if dif:
                result.append({'type': 'different', 'key': k1, 'value': dif, 'message': '数据不一致'})
            i += 1
            j += 1
    for k_ in range(i, len(a)):
        result.append({'type': 'missing', 'key': tuple(a[k_][k] for k in keys), 'value': a[k_], 'message': '数据2中缺少数据'})
    for k_ in range(j, len(b)):
        result.append({'type': 'missing', 'key': tuple(b[k_][k] for k in keys), 'value': b[k_], 'message': '数据1中缺少数据'})
    return result

if __name__ == '__main__':
    data = compare_table(
        [{'name': 'tom', 'age': 11, 'sex': 'male'}],
        [{'name': 'tom', 'age': 10, 'sex': 'male'}, {'name': 'jim', 'age': 10, 'sex': 'male'}],
        'name'
    )
    print(*data, sep='\n')
    pass
