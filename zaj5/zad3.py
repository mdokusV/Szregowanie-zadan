import io
import sys

input_string = """3 17
4 10 2 13 4
0
1 12
0
3 11 6 7
0
0
0
0
0
0
2 9 8
0
1 16
1 17
2 3 15
2 1 5
"""
sys.stdin = io.StringIO(input_string)


from typing import Optional
from queue import PriorityQueue


class Task:
    def __init__(self, index):
        self.index = index
        self.predecessors: list[int] = []
        self.predecessors_number = 0
        self.successor: Optional[int] = None
        self.level = 0

    def __str__(self):
        return f"{self.index}:[{self.level}] {self.successor} {self.predecessors}"

    def __lt__(self, other):
        assert isinstance(other, Task)
        return (self.level, -self.index) > (other.level, -other.index)


class Processor:
    def __init__(self, index):
        self.index = index
        self.tasks_done: list[int] = []

    def __str__(self):
        return f"{self.index+1}: {' '.join(str(x+1) for x in self.tasks_done)}"


machine_number, task_number = map(int, input().split())

no_predecessor_pq: PriorityQueue[Task] = PriorityQueue()

tasks = [Task(i) for i in range(task_number)]

root = set(range(task_number))

for i in range(task_number):
    predecessors = [x - 1 for x in map(int, input().split()[1:])]

    if len(predecessors) == 0:
        no_predecessor_pq.put(tasks[i])
    else:
        tasks[i].predecessors.extend(predecessors)
        tasks[i].predecessors_number = len(predecessors)

    for predecessor in predecessors:
        tasks[predecessor].successor = i
        root.discard(predecessor)


def level(task_number: int):
    task = tasks[task_number]
    if task.successor is None:
        task.level = 0
    else:
        task.level = tasks[task.successor].level + 1
    for predecessor in task.predecessors:
        level(predecessor)


if len(root) > 1:
    print("ERROR: too many roots")
    exit(1)


level(root.pop())

machines = [Processor(i) for i in range(machine_number)]

time = 0
while not no_predecessor_pq.empty():
    new_tasks: list[Task] = []
    for worker in machines:
        if no_predecessor_pq.empty():
            break
        new_task = no_predecessor_pq.get()
        new_tasks.append(new_task)
        worker.tasks_done.append(new_task.index)
    for task in new_tasks:
        if task.successor is None:
            continue
        successor = tasks[task.successor]
        successor.predecessors_number -= 1
        if successor.predecessors_number == 0:
            no_predecessor_pq.put(successor)
    time += 1

print(time)
print(*machines, sep="\n")
