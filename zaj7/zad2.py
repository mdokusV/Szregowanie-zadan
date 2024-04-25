# plecak

import io
import sys

input_string = """6 10
3 2
4 8
2 5
4 3
1 2
3 1
"""
sys.stdin = io.StringIO(input_string)


class Task:
    def __init__(self, index: int, weight: int, value: int):
        self.index = index
        self.weight = weight
        self.value = value

    def __str__(self):
        return f"[{self.index}] weight:{self.weight} value:{self.value} \n"


task_number, knapsack_size = map(int, input().split())

tasks = [Task(i, 0, 0) for i in range(task_number)]

for i in range(task_number):
    weight, value = map(int, input().split())
    tasks[i].weight = weight
    tasks[i].value = value

dynamic_matrix = [[0 for _ in range(knapsack_size + 1)] for _ in range(task_number + 1)]

for i in range(1, task_number + 1):
    for j in range(1, knapsack_size + 1):
        current_task = tasks[i - 1]
        if current_task.weight > j:
            dynamic_matrix[i][j] = dynamic_matrix[i - 1][j]
        else:
            dynamic_matrix[i][j] = max(
                dynamic_matrix[i - 1][j],
                dynamic_matrix[i - 1][j - current_task.weight] + current_task.value,
            )

print(dynamic_matrix[-1][-1])

j = knapsack_size
items_taken = []
for i in range(task_number, 0, -1):
    if dynamic_matrix[i][j] != dynamic_matrix[i - 1][j]:
        items_taken.append(i)
        j -= tasks[i - 1].weight


items_taken.sort()
print(*items_taken, sep="\n")
