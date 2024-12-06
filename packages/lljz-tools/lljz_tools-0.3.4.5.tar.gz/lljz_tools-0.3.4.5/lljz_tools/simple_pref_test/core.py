# coding=utf-8

"""
@fileName       :   core.py
@data           :   2024/8/27
@author         :   jiangmenggui@hosonsoft.com
"""
import queue
import time
from collections import defaultdict
from typing import NamedTuple, Any, Callable, TypeVar, cast


class TaskResult(NamedTuple):
    name: str
    start: float
    end: float
    message: str = ""
    success: bool = True

    @property
    def use_time(self):
        return self.end - self.start


class TaskResultSet:
    result_data: queue.Queue[TaskResult] = queue.Queue()
    start_time: float = 0.0
    end_time: float = 0.0

    @classmethod
    def put(cls, task_result: TaskResult):
        cls.result_data.put(task_result)


def strf_time(t: float | int) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))


T = TypeVar('T')
CollectionType = TypeVar('CollectionType', int, list)


def get_init_collection(coll_type: Callable[[], CollectionType]) -> dict[str, defaultdict[str, CollectionType]]:
    start = int(TaskResultSet.start_time)
    end = int(TaskResultSet.end_time)
    return {
        strf_time(i): defaultdict(coll_type)
        for i in range(start, end + 1)
    }


def init_result():
    result: dict[str, dict[str, Any]] = {}
    rps = get_init_collection(int)
    qps = get_init_collection(int)
    response = get_init_collection(list)

    while not TaskResultSet.result_data.empty():
        row = TaskResultSet.result_data.get()
        t1 = strf_time(row.start)
        t2 = strf_time(row.end)
        
        if t2 not in rps:
            rps[t2] = defaultdict(int)
        if t1 not in qps:
            qps[t1] = defaultdict(int)
        if t2 not in response:
            response[t2] = defaultdict(list)

        qps[t1][row.name] += 1
        response[t2][row.name].append(row.use_time)
        if row.success:
            rps[t2][row.name + '(成功)'] += 1
        else:
            rps[t2][row.name + '(失败)'] += 1

        if row.name not in result:
            result[row.name] = {
                "NAME": row.name,
                "START_TIME": row.start,
                "END_TIME": row.end,
                "USE_TIME": [row.use_time],
                "SUCCESS": int(bool(row.success))
            }
        else:
            result[row.name]['START_TIME'] = min(result[row.name]['START_TIME'], row.start)
            result[row.name]['END_TIME'] = max(result[row.name]['END_TIME'], row.end)
            result[row.name]['USE_TIME'].append(row.use_time)
            result[row.name]['SUCCESS'] += int(bool(row.success))

    table_data = []
    for value in result.values():
        use_time = sorted(value["USE_TIME"])
        duration = TaskResultSet.end_time - TaskResultSet.start_time
        table_data.append({
            "任务名称": value['NAME'],
            "执行次数": len(use_time),
            "错误次数": len(use_time) - value['SUCCESS'],
            "成功率": f"{value['SUCCESS'] / len(use_time):.4%}",
            "中位数响应": f"{int(use_time[int(len(use_time) * 0.5)] * 1000)}ms",
            "90%响应": f"{int(use_time[int(len(use_time) * 0.9)] * 1000)}ms",
            "95%响应": f"{int(use_time[int(len(use_time) * 0.95)] * 1000)}ms",
            "平均响应": f"{int(sum(value['USE_TIME']) * 1000 / len(value['USE_TIME']))}ms",
            "最小响应": f"{int(use_time[0] * 1000)}ms",
            "最大响应": f"{int(use_time[-1] * 1000)}ms",
            "吞吐量（RPS）": f'{value["SUCCESS"] / duration:.2f}/s'
        })

    return table_data, rps, qps, response


if __name__ == '__main__':
    pass
