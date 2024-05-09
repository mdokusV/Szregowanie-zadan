# O2||C_max  -  wzór z wykładu

import io
import sys


input_string = """5
2 4
3 1
4 2
5 3
1 5
"""
sys.stdin = io.StringIO(input_string)

task_number = int(input())

tasks = [[0 for _ in range(task_number)], [0 for _ in range(task_number)]]

for i in range(task_number):
    processing_time_one, processing_time_two = map(int, input().split())
    tasks[0][i] = processing_time_one
    tasks[1][i] = processing_time_two

maximum = max(
    sum(tasks[0]),
    sum(tasks[1]),
    max(tasks[0][i] + tasks[1][i] for i in range(task_number)),
)

print(maximum)
