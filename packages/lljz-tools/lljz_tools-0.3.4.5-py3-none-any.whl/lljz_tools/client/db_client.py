# coding=utf-8

"""
@fileName       :   db_client_2.py
@data           :   2024/5/11
@author         :   jiangmenggui@hosonsoft.com
"""
import re
try:
    import pymysql
    import pymysql.cursors
    from pymysql.cursors import DictCursor
    from dbutils.pooled_db import PooledDB
    from sshtunnel import SSHTunnelForwarder
except ImportError as e:
    print('pymysql not installed, please install it by pip install pymysql dbutils sshtunnel')
    raise ImportError('package not installed! use "pip install pymysql "')



from lljz_tools import logger
from lljz_tools.log_manager import LogManager

_logger = LogManager('sshtunnel', console_level='WARNING', file_path=None).get_logger()

ArgsType = list | tuple | None

class MySQLConnectionPool:

    def __init__(self, uri: str, ssh_uri='', show_sql: bool = False):
        database_config = self._init_uri(uri)
        database_config['cursorclass'] = DictCursor
        database_config['charset'] = 'utf8mb4'
        self._ssh = None
        self.show_sql = show_sql

        if ssh_uri:
            ssh_config = self._init_ssh_uri(ssh_uri)
            self._ssh = self._get_tunnel_ssh(
                database_config['host'], database_config['port'],
                ssh_config['host'], ssh_config['port'], ssh_config['user'], ssh_config['password']
            )
            database_config['host'] = '127.0.0.1'
            database_config['port'] = self._ssh.local_bind_port
            database_config['autocommit'] = True

        # 创建连接池
        self._pool = PooledDB(
            creator=pymysql,
            # 其他参数根据你的应用需求调整
            mincached=1,
            maxcached=5,
            maxconnections=10,
            blocking=True,  # 如果没有可用连接，调用者将等待而不是抛出异常
            **database_config  # type: ignore
        )

    @staticmethod
    def _init_uri(uri):
        obj = re.match(
            r'^mysql://(?P<user>.+):(?P<password>.+)@(?P<host>.+):(?P<port>\d+)/(?P<db>.+?)(?:\?(?P<qs>.+))?$',
            uri
        )
        if not obj:
            raise ValueError(f'unmatch uri: {uri}')
        database_config = obj.groupdict()
        if database_config['qs']:
            qs = {k: v for k, v in (i.split('=', maxsplit=1) for i in database_config.pop('qs').split('&'))}
            database_config.update(qs)
        else:
            database_config.pop('qs')
        database_config['port'] = int(database_config['port'])
        return database_config

    @staticmethod
    def _init_ssh_uri(ssh_uri):
        obj = re.match(f'^ssh://(?P<user>.+):(?P<password>.+)@(?P<host>.+?)(?::(?P<port>[0-9]+))?$', ssh_uri)
        if not obj:
            raise ValueError(f'unmatch ssh_uri: {ssh_uri}')
        ssh_config = obj.groupdict()
        if 'port' not in ssh_config:
            ssh_config['port'] = 22
        ssh_config['port'] = int(ssh_config['port'])
        return ssh_config

    @staticmethod
    def _get_tunnel_ssh(host, port, ssh_ip, ssh_port, ssh_user, ssh_pwd):
        # private_key = paramiko.RSAKey.from_private_key_file(
        #     filename=ssh_key_path,
        #     password=ssh_pwd
        # )
        ssh_tunnel = SSHTunnelForwarder(
            ssh_address_or_host=(ssh_ip, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_pwd,
            remote_bind_address=(host, port),
            logger=_logger
        )
        ssh_tunnel.start()
        return ssh_tunnel

    def close(self):
        self._pool.close()
        if self._ssh:
            self._ssh.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        return MySQLConnection(self._pool.connection(), self.show_sql)


class MySQLConnection:

    def __init__(self, conn, show_sql: bool):
        self.conn = conn
        self._show_sql = show_sql

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def show_sql(self, cursor: DictCursor, sql: str, args: ArgsType = None):
        if self._show_sql:
            try:
                logger.debug(cursor.mogrify(sql, args), stacklevel=3)
            except TypeError as e:
                logger.error(f'[ERROR SQL] sql: {sql}, args: {args}', stacklevel=3)
                logger.exception(e, stacklevel=3)

    def select(self, sql: str, args: ArgsType = None, limit: int = 1000) -> list[dict]:
        """
        查询数据，默认查询1000行
        
        :param sql: 查询语句
        :param args: 查询参数
        :param limit: 查询行数
        :return: 查询结果
        """
        sql = sql.replace('?', '%s')
        with self.conn.cursor() as cursor:
            self.show_sql(cursor, sql, args)
            cursor.execute(sql, args)
            return cursor.fetchmany(limit)

    def select_one(self, sql: str, args: ArgsType=None) -> dict | None:
        """
        查询一条数据
        
        :param sql: 查询语句
        :param args: 查询参数
        :return: 查询结果
        """
        sql = sql.replace('?', '%s')
        with self.conn.cursor() as cursor:
            self.show_sql(cursor, sql, args)
            cursor.execute(sql, args)
            return cursor.fetchone()

    def select_all(self, sql: str, args: ArgsType = None) -> list[dict]:
        """
        查询所有数据
        
        :param sql: 查询语句
        :param args: 查询参数
        :return: 查询结果
        """
        sql = sql.replace('?', '%s')
        with self.conn.cursor() as cursor:
            self.show_sql(cursor, sql, args)
            cursor.execute(sql, args)
            return cursor.fetchall()

    def insert(self, sql: str, args: ArgsType = None) -> int:
        """
        插入数据
        
        :param sql: 插入语句
        :param args: 插入参数
        :return: 插入行数
        """
        sql = sql.lstrip()
        sql_type, _ = sql.split(maxsplit=1)
        if sql_type.upper() != 'INSERT':
            raise ValueError(f'NOT INSERT SQL: {sql}')
        sql = sql.replace('?', '%s')
        with self.conn.cursor() as cursor:
            self.show_sql(cursor, sql, args)
            cursor.execute(sql, args)
            return cursor.lastrowid

    def insert_many(self, sql: str, args: list[tuple | list] | tuple[list | tuple]) -> int:
        """
        批量插入数据
        
        :param sql: 插入语句
        :param args: 插入参数
        :return: 插入行数
        """
        sql = sql.lstrip()
        sql_type, _ = sql.split(maxsplit=1)
        if sql_type.upper() != 'INSERT':
            raise ValueError(f'NOT INSERT SQL: {sql}')
        sql = sql.replace('?', '%s')
        with self.conn.cursor() as cursor:
            for arg in args:
                self.show_sql(cursor, sql, arg)
            cursor.executemany(sql, args)
            return cursor.rowcount

    def update(self, sql: str, args: ArgsType = None) -> int:
        """
        更新数据
        
        :param sql: 更新语句
        :param args: 更新参数
        :return: 更新行数
        """
        sql = sql.lstrip()
        sql_type, _ = sql.split(maxsplit=1)
        if sql_type.upper() != 'UPDATE':
            raise ValueError(f'NOT UPDATE SQL: {sql}')
        sql = sql.replace('?', '%s')
        with self.conn.cursor() as cursor:
            self.show_sql(cursor, sql, args)
            cursor.execute(sql, args)
            return cursor.rowcount

    def delete(self, sql: str, args: ArgsType = None) -> int:
        """
        删除数据
        
        :param sql: 删除语句
        :param args: 删除参数
        :return: 删除行数
        """
        sql = sql.lstrip()
        sql_type, _ = sql.split(maxsplit=1)
        if sql_type.upper() != 'DELETE':
            raise ValueError(f'NOT DELETE SQL: {sql}')
        sql = sql.replace('?', '%s')
        with self.conn.cursor() as cursor:
            self.show_sql(cursor, sql, args)
            cursor.execute(sql, args)
            return cursor.rowcount

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()


if __name__ == '__main__':
    pass
