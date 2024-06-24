import io
import sys


input_string = """10 10
70 60 50 52 98 75 27 78 9 3 
33 41 2 31 14 69 10 21 63 52 
69 15 66 6 84 89 84 58 86 89 
91 100 17 32 92 25 3 17 13 80 
54 83 57 42 85 92 8 53 24 39 
20 96 10 49 64 6 8 75 76 60 
13 99 81 36 96 98 94 27 46 81 
19 69 13 18 94 60 44 28 28 50 
91 58 25 71 73 21 13 22 68 49 
24 10 33 65 33 37 49 37 40 72 
"""
sys.stdin = io.StringIO(input_string)


from math import exp
import copy
from dataclasses import dataclass, field
import random
from typing import List

RNG = random.Random()


class Param:
    def __init__(self):
        self.ITER_MAX = 1000
        self.TEMPERATURE_START = 17
        self.temperature = self.TEMPERATURE_START
        self.FREEZING = 0.875

    def update_temp(self):
        self.temperature = self.temperature * self.FREEZING


PARAM = Param()


@dataclass
class Task:

    index: int
    processing_times: List[int] = field(default_factory=list)
    sum: int = 0

    def __str__(self):
        return f"{self.index}"

    def __lt__(self, other: "Task"):
        return self.sum > other.sum

    def __eq__(self, other: "Task"):
        return self.sum == other.sum

    def __gt__(self, other: "Task"):
        return self.sum < other.sum


@dataclass
class Order:
    tasks: List[Task]
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
            print([task.index for task in order.tasks], order.sum, missis)
            if self.sum < best_order.sum:
                PARAM.temperature = PARAM.TEMPERATURE_START
                best_order.copy_order(self)
                return -missis
            return 0

        if exp((old_sum - self.sum) / PARAM.temperature) > RNG.random():
            print([task.index for task in order.tasks], order.sum, missis)
            if self.sum < best_order.sum:
                best_order.copy_order(self)
            return 1

        (
            self.tasks[take],
            self.tasks[swap_index],
        ) = (
            self.tasks[swap_index],
            self.tasks[take],
        )
        self.sum = old_sum
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


best_order = Order(tasks)
best_order.calculate_sum()

order = Order(tasks)
order.calculate_sum()

missis = 0
while missis < PARAM.ITER_MAX:
    missis += order.local_search(best_order)

best_order.calculate_sum()
print(best_order)
