import io
import sys

input_string = """6
8 1 10
2 2 4
0 4 5
7 2 9
13 1 14
5 3 12"""
sys.stdin = io.StringIO(input_string)


class Task:
    def __init__(self, relies_time, processing_time, due_time, index):
        self.relies_time = relies_time
        self.processing_time = processing_time
        self.due_time = due_time
        self.index = index

    def __lt__(self, other):
        return self.due_time < other.due_time

    def __gt__(self, other):
        return self.due_time > other.due_time

    def __eq__(self, other):
        return self.due_time == other.due_time

    def __str__(self):
        return f"[{self.index}] relies_time:{self.relies_time} processing_time:{self.processing_time} due_time:{self.due_time} \n"

from queue import PriorityQueue

size = int(input())
relies_table: list[Task] = []
timestamps: list[int] = []
for i in range(size):
    relies_time, processing_time, due_time = map(int, input().split())
    relies_table.append(Task(relies_time, processing_time, due_time, i))
    timestamps.append(relies_time)

solution = [0 for _ in range(size)]
timestamps.sort()
relies_table.sort(key=lambda x: x.relies_time)

pq: PriorityQueue[Task] = PriorityQueue()
print(*relies_table)

while len(timestamps) >= 2:
    time = timestamps.pop(1)
    new_task = relies_table.pop(0)
    pq.put(new_task)
    current_task = pq.get()
    while current_task.relies_time < time:
        if current_task.processing_time < time - current_task.relies_time:
            time_passed = current_task.processing_time + current_task.relies_time
            delay = time_passed - current_task.due_time
            if delay < 0:
                delay = 0
            solution[current_task.index] = delay

            if not pq.empty():
                current_task = pq.get()
                current_task.relies_time = time_passed
            else:
                break
            continue

        current_task.processing_time = current_task.processing_time - (
            time - current_task.relies_time
        )
        current_task.relies_time = time
        pq.put(current_task)

pq.put(relies_table[0])
while not pq.empty():
    current_task = pq.get()
    time = time + current_task.processing_time
    delay = time_passed - current_task.due_time
    if delay < 0:
        delay = 0
    solution[current_task.index] = delay

print(max(solution))
