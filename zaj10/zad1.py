# F3||C_max - druga maszyna zdominowana, alg     na zmiennych danych

import io
import sys


input_string = """5
3 1 3
3 1 2
5 2 4
4 3 6
4 1 3
"""
sys.stdin = io.StringIO(input_string)


class Task:

    def __init__(self, index: int):
        self.index = index
        self.processing_times: list[int] = []
        self.processing_time_one: int = 0
        self.processing_time_two: int = 0

    def __str__(self):
        return f"[{self.index}] {self.processing_times}"


task_number = int(input())
worker_number = 3

tasks = [Task(i) for i in range(task_number)]

for i in range(task_number):
    tasks[i].processing_times = list(map(int, input().split()))
    tasks[i].processing_time_one = (
        tasks[i].processing_times[0] + tasks[i].processing_times[1]
    )
    tasks[i].processing_time_two = (
        tasks[i].processing_times[1] + tasks[i].processing_times[2]
    )

print(*tasks, sep="\n")


first_faster: list[Task] = []
first_slower: list[Task] = []
for task in tasks:
    if task.processing_time_one < task.processing_time_two:
        first_faster.append(task)
    else:
        first_slower.append(task)


first_faster.sort(key=lambda task: task.processing_time_one)
first_slower.sort(key=lambda task: task.processing_time_two, reverse=True)

ordered_tasks = first_faster + first_slower
time_one = 0
time_two = 0

for task in ordered_tasks:
    time_one += task.processing_time_one

    time_two = max(time_one, time_two) + task.processing_time_two

print(time_two - sum(task.processing_times[1] for task in tasks))
