# EDD wypełnienie slotów

import io
import sys

input_string = """2 12
7 1
4 4
8 4
8 2
1 3
8 3
7 4
3 1
4 2
5 1
2 1
6 2
"""
sys.stdin = io.StringIO(input_string)


from queue import PriorityQueue


class Task:
    def __init__(self, index: int, deadline: int, weight: int):
        self.index = index
        self.deadline = deadline
        self.weight = weight

    def __str__(self):
        return f"[{self.index}] deadline:{self.deadline} weight:{self.weight} \n"

    def __lt__(self, other):
        assert isinstance(other, Task)
        return self.weight < other.weight

    def __gt__(self, other):
        assert isinstance(other, Task)
        return self.weight > other.weight

    def __eq__(self, other):
        assert isinstance(other, Task)
        return self.weight == other.weight


machine_number, task_number = map(int, input().split())

tasks: list[Task] = []
for i in range(task_number):
    weight, deadline = map(int, input().split())
    tasks.append(Task(i, deadline, weight))
tasks.sort(key=lambda task: (task.deadline, -task.weight))
pq: PriorityQueue[Task] = PriorityQueue()

time = 0
machines_used = 0
late_tasks_sum = 0
for task in tasks:
    if time >= task.deadline:
        if pq.queue[0].weight < task.weight:
            bad_task = pq.get()
            late_tasks_sum += bad_task.weight
            pq.put(task)
        else:
            late_tasks_sum += task.weight

    else:
        pq.put(task)
        machines_used += 1
        if machines_used % machine_number == 0:
            machines_used = 0
            time += 1
print(late_tasks_sum)
