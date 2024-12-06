# coding=utf-8

"""
@fileName       :   runner.py
@data           :   2024/8/27
@author         :   jiangmenggui@hosonsoft.com
"""
import datetime
import json
import os.path
import queue
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional, cast

from jinja2 import Environment, FileSystemLoader, select_autoescape

from lljz_tools.color import Color
from lljz_tools.console_table import ConsoleTable
from lljz_tools.simple_pref_test._task import find_tasks, TaskGroup, TaskSet, _TaskSetFunction
from lljz_tools.simple_pref_test.core import TaskResultSet, init_result, strf_time


class PrefRunner:

    def __init__(
            self,
            __name: str = '性能测试', /, *,
            virtual_users: Optional[int] = 1,
            user_add_interval: Optional[float] = 0.1,
            pre_task: Optional[float] = None,
            run_seconds: Optional[float] = 10,
            save_directory: Optional[str] = None,
    ):
        assert pre_task is not None or (virtual_users is not None and user_add_interval is not None)
        assert pre_task is None or (isinstance(pre_task, (float, int)) and pre_task > 0)
        assert virtual_users is None or (isinstance(virtual_users, int) and virtual_users > 0)
        assert user_add_interval is None or (isinstance(user_add_interval, (float, int)) and user_add_interval >= 0)
        self.name = __name
        self.save_directory = save_directory or os.path.abspath(f'./pref_test_result/{self.name}')
        self.run_seconds = float(run_seconds) if run_seconds is not None else 10.0
        self.virtual_users = virtual_users
        self.user_add_interval = user_add_interval
        self.pre_task = pre_task
        max_workers = max(10, virtual_users or 0)
        if pre_task:
            max_workers = max(max_workers, int(pre_task))
        self.pool = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks = find_tasks()
        self.running = True

    def _run_with_thread_num(self):
        """按照固定线程数启动"""

        def run():
            group = TaskGroup(self.tasks)
            while True:
                task_set = group.get()
                for task in task_set.tasks:
                    if time.time() - TaskResultSet.start_time > self.run_seconds:
                        group.teardown_all()
                        return

                    task_name = getattr(task, 'name', task.__name__)
                    task_set.setup(task_name)
                    task()
                    task_set.teardown(task_name)

        if self.virtual_users is not None:
            for _ in range(self.virtual_users):
                self.pool.submit(run)
                if self.user_add_interval is not None:
                    time.sleep(float(self.user_add_interval))

    def _run_with_pre_task(self):
        """按照每秒启动的线程数启动"""
        group_queue: queue.Queue[TaskGroup] = queue.Queue()
        k = 1
        if self.pre_task is not None:
            pre_task = float(self.pre_task)
            while pre_task > 10:
                pre_task = pre_task / 10
                k = k * 10
            interval = 1 / pre_task

            def run():
                nonlocal group_queue
                if group_queue.empty():
                    group = TaskGroup(self.tasks)
                else:
                    group = group_queue.get()
                task_set = group.get()
                for task in task_set.tasks:
                    if time.time() - TaskResultSet.start_time > self.run_seconds:
                        group.teardown_all()
                        return
                    task_name = getattr(task, 'name', task.__name__)
                    task_set.setup(task_name)
                    task()
                    task_set.teardown(task_name)
                group_queue.put(group)

            while time.time() - TaskResultSet.start_time < self.run_seconds and self.running:
                for _ in range(k):
                    self.pool.submit(run)
                time.sleep(interval)

    def run_task(self):
        if self.pre_task:
            self._run_with_pre_task()
        else:
            self._run_with_thread_num()

    def print_start_info(self):
        print(f"开始测试：{Color.green(self.name)}")
        if self.pre_task:
            print(
                f"{Color.yellow('==========测试任务启动参数==========')}\n"
                f"   {Color.thin_magenta('每秒任务数')} : {self.pre_task}\n"
                f"     {Color.thin_magenta('运行时间')} : {self.run_seconds}s\n"
                f"     {Color.thin_magenta('任务总数')} : {len(set(self.tasks))}\n"
                f"     {Color.thin_magenta('启动时间')} : {strf_time(TaskResultSet.start_time)}\n"
                f"{Color.yellow('====================================')}\n"
            )
        else:
            print(
                f"{Color.yellow('==========测试任务启动参数==========')}\n"
                f"   {Color.thin_magenta('并发线程数')} : {self.virtual_users}\n"
                f" {Color.thin_magenta('线程启动间隔')} : {self.user_add_interval}s\n"
                f"     {Color.thin_magenta('运行时间')} : {self.run_seconds}s\n"
                f"     {Color.thin_magenta('任务总数')} : {len(set(self.tasks))}\n"
                f"     {Color.thin_magenta('启动时间')} : {strf_time(TaskResultSet.start_time)}\n"
                f"{Color.yellow('====================================')}\n"
            )

    def start(self):
        TaskResultSet.start_time = time.time()
        self.print_start_info()
        try:
            self.run_task()
            self.pool.shutdown(wait=True)
        finally:
            end_time = TaskResultSet.end_time = time.time()
            table_data, rps, qps, response = init_result()
            table = ConsoleTable(table_data, caption="性能测试结果")
            print(table)
            print(f'\n\n{Color.green("测试完成！")}[完成时间：{Color.thin_cyan(strf_time(end_time))}]')
            file = self.save_to_html(table_data, rps, qps, response)
            print(f'结果保存至：{Color.thin_blue(file)}')

    def save_to_html(self, table, rps, qps, response):
        def get_avg(data):
            return int(sum(data) / len(data) * 1000)

        def init_table_data(table_data):
            return {"header": list(table_data[0].keys()), "rows": [list(row.values()) for row in table_data]}

        def init_data(data, func):
            tps = sorted(data.items())
            keys = set()
            for _, v in tps:
                for k in v:
                    keys.add(k)
            values = {k: [] for k in keys}
            for _, v in tps:
                for k in keys:
                    values[k].append(func(k, v))
            return json.dumps({
                'keys': [k.split(' ')[1] for k, v in tps],
                "values": [{"name": k, "data": v} for k, v in values.items()]
            }, ensure_ascii=False)

        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
        filename = f'{self.name}_{datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")}.html'
        file = os.path.join(self.save_directory, filename)
        source = Path(__file__).parent.parent / 'source'
        env = Environment(
            loader=FileSystemLoader(source),
            autoescape=select_autoescape(['html', 'xml'])
        )
        with open(source / 'echart.js', 'r', encoding='u8') as f:
            echart_js = f.read()
        template = env.get_template('result.html')
        run_arguments = [
            f"并发线程数 : {self.virtual_users}",
            f"线程启动间隔 : {self.user_add_interval}s"
        ]

        context = {
            "echartJs": echart_js,
            "title": self.name,
            'arguments': [
                *run_arguments,
                f"运行时间 : {self.run_seconds}s",
                f"任务总数 : {len(set(self.tasks))}",
                f"启动时间 : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(TaskResultSet.start_time))}",
                f"结束时间 : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(TaskResultSet.end_time))}"],
            "table": init_table_data(table),
            "rpsData": init_data(rps, lambda k, v: v.get(k, 0)),
            "qpsData": init_data(qps, lambda k, v: v.get(k, 0)),
            "responseData": init_data(response, lambda k, v: get_avg(v.get(k, [0])))
        }
        with open(file, 'w', encoding='u8') as f:
            f.write(template.render(context))
        return file


if __name__ == '__main__':
    pass
