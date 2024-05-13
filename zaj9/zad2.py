# F2||C_max  -  alg Johnsona

import io
import sys


input_string = """5
2 3
3 1
5 2
3 4
1 3
"""
sys.stdin = io.StringIO(input_string)


class Task:

    def __init__(self, index: int, processing_time_one: int, processing_time_two: int):
        self.index = index
        self.processing_time_one = processing_time_one
        self.processing_time_two = processing_time_two
        self.finished_one: int = 0
        self.finished_two: int = 0

    def __str__(self):
        return f"{self.index+1} {self.finished_one} {self.finished_two}"


task_number = int(input())

tasks = [Task(i, 0, 0) for i in range(task_number)]

for i in range(task_number):
    tasks[i].processing_time_one, tasks[i].processing_time_two = map(
        int, input().split()
    )


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
    task.finished_one = time_one

    time_two = max(time_one, time_two) + task.processing_time_two
    task.finished_two = time_two

    print(task)
