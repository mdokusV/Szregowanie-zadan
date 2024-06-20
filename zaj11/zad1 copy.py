# F||C_max - ILS

import copy
from dataclasses import dataclass, field
import io
from math import exp
import sys
from typing import List


input_string = """3 5
6 5 19
11 4 13
15 2 1
5 17 16
15 10 4
"""
sys.stdin = io.StringIO(input_string)


import random

RNG = random.Random()


class Param:
    def __init__(self):
        self.ITER_MAX = 200
        self.temperature = 50
        self.FREEZING = 0.875

    def update_temp(self):
        self.temperature = self.temperature * self.FREEZING


PARAM = Param()


@dataclass
class Task:

    index: int
    processing_times: list[int] = field(default_factory=list)
    sum: int = 0

    def __str__(self):
        return f"{self.index}, processing_times:{self.processing_times}"

    def __lt__(self, other: "Task"):
        return self.sum > other.sum

    def __eq__(self, other: "Task"):
        return self.sum == other.sum

    def __gt__(self, other: "Task"):
        return self.sum < other.sum


@dataclass
class Order:
    tasks: list[Task]
    sum: int = 0

    def __str__(self):
        return f"{self.sum}\n" + " ".join([str(task) for task in self.tasks])

    def calculate_sum(self) -> int:
        times_of_workers = [0 for _ in range(worker_number)]
        for task in self.tasks:
            for worker in range(worker_number):
                if worker == 0:
                    times_of_workers[worker] += task.processing_times[worker]
                else:
                    times_of_workers[worker] = (
                        max(times_of_workers[worker], times_of_workers[worker - 1])
                        + task.processing_times[worker]
                    )

        self.sum = times_of_workers[-1]
        return times_of_workers[-1]

    def copy_order(self, other: "Order"):
        self.tasks = copy.deepcopy(other.tasks)
        self.sum = other.sum

    def local_search(self, best_order: "Order") -> int:
        old_sum = self.sum

        take = RNG.randint(0, len(self.tasks) - 1)
        swap = RNG.randint(1, len(self.tasks) - 1)
        swap_index = (take + swap) % len(self.tasks)
        (
            self.tasks[take],
            self.tasks[swap_index],
        ) = (
            self.tasks[swap_index],
            self.tasks[take],
        )
        self.calculate_sum()

        if self.sum < old_sum:
            if self.sum < best_order.sum:
                best_order.copy_order(self)
            return 0

        if -exp((old_sum - self.sum) / PARAM.temperature) > RNG.random():
            if self.sum < best_order.sum:
                best_order.copy_order(self)
            return 0

        PARAM.update_temp()
        return 1

    def __hash__(self) -> int:
        return hash(tuple(task.index for task in self.tasks))

    def __eq__(self, other: "Order") -> bool:
        return self.tasks == other.tasks


worker_number, task_number = map(int, input().split())

tasks = [Task(i) for i in range(task_number)]

for i in range(task_number):
    tasks[i].processing_times = list(map(int, input().split()))
    tasks[i].sum = sum(tasks[i].processing_times)

tasks.sort()

print(*tasks, sep="\n")

best_order = Order(tasks)
best_order.calculate_sum()

order = Order(tasks)
order.calculate_sum()

missis = 0
while missis < PARAM.ITER_MAX:
    missis += order.local_search(best_order)

best_order.calculate_sum()
print(best_order)
