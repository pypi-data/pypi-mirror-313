# coding=utf-8

"""
@fileName       :   pref.py
@data           :   2024/8/28
@author         :   jiangmenggui@hosonsoft.com
"""
import time
from lljz_tools.client.http_client import HTTPClient
from lljz_tools.simple_pref_test import PrefRunner, TaskSet, task, mark_task


class PullOrderTaskSet(TaskSet):
    weight = 4

    def setup_class(self):
        print('setup_class')

    def teardown_class(self):
        print('teardown_class')

    def setup(self, task_name: str):
        if task_name == 'hello_world':
            print('hello_world setup')

    def teardown(self, task_name: str):
        print('teardown')

    @task
    def hello_world(self):
        print('hello world')
        time.sleep(1)

    @task('ttt')
    def t(self):
        print('ttt')
        time.sleep(0.5)



if __name__ == '__main__':
    PrefRunner(
        '性能测试',
        virtual_users=1, user_add_interval=0.1,
        # pre_task=5,
        run_seconds=60
    ).start()
