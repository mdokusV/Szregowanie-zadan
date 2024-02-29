import io
import sys

input_string = """4
1 10
3 3
2 7
5 2"""
sys.stdin = io.StringIO(input_string)


size = int(input())
summ = 0
jobs = []
for i in range(size):
    job = input().split()
    job = [int(x) for x in job]

    jobs.append(job)

jobs.sort(key=lambda x: x[0] / x[1], reverse=False)
time_passed = 0
for job in jobs:
    time_passed += job[0]
    summ += job[1] * time_passed

print(summ)
