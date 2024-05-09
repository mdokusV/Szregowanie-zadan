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
    def __init__(self, index, processing_time_one, processing_time_two):
        self.index = index
        self.processing_time_one = processing_time_one
        self.processing_time_two = processing_time_two

    def __str__(self):
        return (
            f"[{self.index}] F:{self.processing_time_one} S:{self.processing_time_two}"
        )


task_number = int(input())

tasks = [Task(i, 0, 0) for i in range(task_number)]

for i in range(task_number):
    tasks[i].processing_time_one, tasks[i].processing_time_two = map(
        int, input().split()
    )

print(*tasks, sep="\n")


first_faster = []
first_slower = []
for task in tasks:
    if task.processing_time_one < task.processing_time_two:
        first_faster.append(task)
    else:
        first_slower.append(task)

print(first_slower, first_faster)
