# F||-   -    DP (uszeregowanie z permutacjami)

import io
import sys


input_string = """3 4
1 1 3
2 3 2
2 2 1
2 2 1
"""
sys.stdin = io.StringIO(input_string)


class Task:

    def __init__(self, index: int):
        self.index = index
        self.processing_times = []


worker_number, task_number = map(int, input().split())

tasks = [Task(i) for i in range(task_number)]

for i in range(task_number):
    tasks[i].processing_times = list(map(int, input().split()))


times_of_workers = [0 for _ in range(worker_number)]

for task in tasks:
    for worker in range(worker_number):
        if worker == 0:
            times_of_workers[worker] += task.processing_times[worker]
        else:
            times_of_workers[worker] = (
                max(times_of_workers[worker], times_of_workers[worker - 1])
                + task.processing_times[worker]
            )

    print(times_of_workers[-1])
