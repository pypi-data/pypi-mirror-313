"""
@file   : c_random.py
@author : jiangmenggui@hosonsoft.com
@data   : 2024/4/2
"""
import enum
import random


class GroupType(enum.Enum):
    """随机字符允许出现的类型"""
    NUMBER = 'integer'  # 数字
    LETTERS = 'letters'  # 字母
    LETTERS_UPPER = 'lettersUpper'  # 大写字母
    LETTERS_LOWER = 'lettersLower'  # 小写字母
    SPECIAL = 'special'  # 特殊符号


def random_upper_or_lower(s: str):
    """将字符中的字母随机转换为大写或者小写"""
    return ''.join(random.choice([i.upper(), i.lower()]) for i in s)


def random_string(size: int | list[int] = 15, groups: list[GroupType | str] | None = None):
    """
    :param size: 随机得到的字符长度，如果给出一个数组，则表示每种字符类型的长度
    :param groups: 包含的字符类型：number（数字）、letters（全部字母）lettersUpper（大写字母）、lettersLower（小写字母）、special（特殊字符）
    :return:
    """
    groups = groups or ['integer', 'letters']
    groups = [group.value if isinstance(group, GroupType) else group for group in groups]
    if isinstance(size, list):
        return ''.join(random_string(i, [j]) for i, j in zip(size, groups))
    charList = []
    for g in groups:
        if g == 'integer':
            charList.extend(list('0123456789'))
        elif g == 'letters':
            charList.extend(list(chr(i) for i in range(ord('a'), ord('z') + 1)))
            charList.extend(list(chr(i) for i in range(ord('A'), ord('Z') + 1)))
        elif g == 'lettersUpper':
            charList.extend(list(chr(i) for i in range(ord('A'), ord('Z') + 1)))
        elif g == 'lettersLower':
            charList.extend(list(chr(i) for i in range(ord('a'), ord('z') + 1)))
        elif g == 'special':
            charList.extend(list('`~!@#$%^&*()_+-={}|:"?><,./;\'[]\\'))
    random.shuffle(list(set(charList)))
    result = ''.join(random.choice(charList) for _ in range(size))
    while result.startswith('0'):
        result = random_integer(size)
    return result


def random_integer(size: int | list[int]):
    """生成一个指定长度的随机数字"""
    return random_string(size, groups=[GroupType.NUMBER])


def random_string_series(series: int, size=15, groups: list[str | GroupType] | None = None):
    """
    生成一系列的String，字符前缀都相同，后面的序号不同
    random_string_series(3)
    ['3cO5WiACaDVex9M001', '3cO5WiACaDVex9M002', '3cO5WiACaDVex9M003']  # 一个可能的输出

    :param series: 生成的个数,1~100的整数
    :param size: 字符的长度，实际长度为size+序列号
    :param groups: 随机字符允许出现的类型
    :return:
    """
    series = max(1, min(series, 100))
    s = random_string(size, groups)
    size = max(2, len(str(series)))
    return (f'{s}{i:0>{size}}' for i in range(1, series + 1))


if __name__ == '__main__':
    print(list(random_string_series(3)))
    print(random_integer(3))
    print(random_string(20))
    pass
