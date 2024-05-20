# F||C_max - NEH

import io
import sys


input_string = """3 3
1 1 3
2 1 1
2 3 2
"""
sys.stdin = io.StringIO(input_string)


class Task:

    def __init__(self, index: int):
        self.index = index
        self.processing_times: list[int] = []
        self.sum: int = 0

    def __str__(self):
        return f"{self.index+1}"

    def __lt__(self, other: "Task"):
        return self.sum > other.sum

    def __eq__(self, other: "Task"):
        return self.sum == other.sum

    def __gt__(self, other: "Task"):
        return self.sum < other.sum


class Order:
    def __init__(self, tasks: list[Task]):
        self.tasks = tasks
        self.sum: int = 0

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

    def copy_other(self, other: "Order"):
        for task_ind in range(len(other.tasks)):
            self.tasks[task_ind] = other.tasks[task_ind]

        self.sum = other.sum

    def next(self, new_task_placement_order: int):
        (
            self.tasks[new_task_placement_order],
            self.tasks[new_task_placement_order + 1],
        ) = (
            self.tasks[new_task_placement_order + 1],
            self.tasks[new_task_placement_order],
        )


worker_number, task_number = map(int, input().split())

tasks = [Task(i) for i in range(task_number)]

for i in range(task_number):
    tasks[i].processing_times = list(map(int, input().split()))
    tasks[i].sum = sum(tasks[i].processing_times)

tasks.sort()


order_task = Order([])

for tasks_taken in range(task_number):
    order_task = Order([tasks[tasks_taken]] + order_task.tasks)
    order_task.calculate_sum()
    checking_order = Order(order_task.tasks.copy())
    for new_task_placement_order in range(tasks_taken):
        checking_order.next(new_task_placement_order)
        checking_order.calculate_sum()
        if checking_order.sum < order_task.sum:
            order_task.copy_other(checking_order)

order_task.calculate_sum()
print(order_task)
