# 1||sum(wiUi)

import io
import sys

input_string = """7
2 3 2
4 4 4
3 2 5
1 4 7
2 1 9
4 3 10
1 2 13
"""
sys.stdin = io.StringIO(input_string)


class Task:
    def __init__(self, index: int, processing_time: int, weight: int, due_time: int):
        self.index = index
        self.processing_time = processing_time
        self.weight = weight
        self.due_time = due_time

    def __str__(self):
        return f"[{self.index}] weight:{self.processing_time} value:{self.weight} due_time:{self.due_time}"


task_number = int(input())

tasks = [Task(i, 0, 0, 0) for i in range(task_number)]

for j in range(task_number):
    processing_time, weight, due_time = map(int, input().split())
    tasks[j].processing_time = processing_time
    tasks[j].weight = weight
    tasks[j].due_time = due_time

max_due_time = max(task.due_time for task in tasks)

dynamic_matrix = [[0 for _ in range(max_due_time + 1)] for _ in range(task_number + 1)]

for j in range(1, task_number + 1):
    for t in range(max_due_time + 1):
        current_task = tasks[j - 1]
        if t == 0:
            dynamic_matrix[j][t] = sum(task.weight for task in tasks[:j])
        elif t <= current_task.due_time:
            if t >= current_task.processing_time:
                dynamic_matrix[j][t] = min(
                    dynamic_matrix[j - 1][t - current_task.processing_time],
                    dynamic_matrix[j - 1][t] + current_task.weight,
                )
            else:
                dynamic_matrix[j][t] = dynamic_matrix[j - 1][t] + current_task.weight
        else:
            dynamic_matrix[j][t] = dynamic_matrix[j][current_task.due_time]

print(dynamic_matrix[-1][-1])

time = max_due_time
items_taken = []
for j in range(task_number, 1, -1):
    current_task = tasks[j - 1]
    time = min(time, current_task.due_time)
    if dynamic_matrix[j][time] != dynamic_matrix[j - 1][time] + current_task.weight:
        items_taken.append(current_task.index + 1)
        time -= current_task.processing_time

items_taken.sort()
print(*items_taken, sep="\n")
