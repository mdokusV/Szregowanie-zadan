# P2||Cmax

import io
import sys

input_string = """6
4
2
2
4
6
4
"""
sys.stdin = io.StringIO(input_string)

from pprint import pprint


class Task:
    def __init__(self, index: int, processing_time: int):
        self.index = index
        self.processing_time = processing_time

    def __str__(self):
        return f"[{self.index}] {self.processing_time}\n"


def show_true_false_table(true_false_table):
    pprint([[int(x) for x in row] for row in true_false_table])


task_number = int(input())
tasks = [Task(i, int(input())) for i in range(task_number)]

allowed_size = sum(task.processing_time for task in tasks) // 2

dynamic_matrix = [
    [False for _ in range(allowed_size + 1)] for _ in range(task_number + 1)
]
for i in range(len(dynamic_matrix)):
    dynamic_matrix[i][0] = True

for i in range(1, task_number + 1):
    for j in range(1, allowed_size + 1):
        dynamic_matrix[i][j] = dynamic_matrix[i - 1][j]
        if j >= tasks[i - 1].processing_time:
            dynamic_matrix[i][j] = (
                dynamic_matrix[i][j]
                or dynamic_matrix[i - 1][j - tasks[i - 1].processing_time]
            )

procedure_one_end_max = max(
    j for j in range(1, allowed_size + 1) if dynamic_matrix[-1][j]
)

procedure_two_end_max = (
    sum(task.processing_time for task in tasks) - procedure_one_end_max
)
print(f"{procedure_one_end_max} {procedure_two_end_max}")
