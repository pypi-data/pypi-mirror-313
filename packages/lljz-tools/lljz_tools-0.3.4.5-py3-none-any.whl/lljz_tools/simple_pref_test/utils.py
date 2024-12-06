# coding=utf-8

"""
@fileName       :   utils.py
@data           :   2024/8/27
@author         :   jiangmenggui@hosonsoft.com
"""
import os
from typing import NamedTuple

type FilePath = str | os.PathLike


class DataBase(NamedTuple):
    uri: str
    sql: str
    ssh_url: str | None = None
    show_sql: bool = False
if __name__ == '__main__':
    pass
