import io
import sys

input_string = """6
2 4
4 1
8 2
9 3
11 1
12 1"""
sys.stdin = io.StringIO(input_string)

size = int(input())

from queue import PriorityQueue

pq = PriorityQueue()

relies_table = []
timestamps = []
for i in range(size):
    for line in input().splitlines():
        relies_time, processing_time = map(int, line.split())
        relies_table.append((relies_time, processing_time))
        timestamps.append(relies_time)

print(relies_table)
pq.put(relies_table.pop(0))
time = 0
while pq.qsize() > 0:
    processing = pq.get()
    was_processed = relies_table[i + 1][0]
