import io
import sys

input_string = """5
4 5
5 11
6 8
2 2
3 10
"""
sys.stdin = io.StringIO(input_string)


from queue import PriorityQueue


class Task:
    def __init__(self, due_time, processing_time, index):
        self.due_time = due_time
        self.processing_time = processing_time
        self.index = index

    def __lt__(self, other):
        assert isinstance(other, Task)
        return (self.due_time, self.index) < (other.due_time, other.index)

    def __gt__(self, other):
        assert isinstance(other, Task)
        return (self.due_time, self.index) > (other.due_time, other.index)

    def __eq__(self, other):
        assert isinstance(other, Task)
        return (self.due_time, self.index) == (other.due_time, other.index)

    def __str__(self):
        return f"{self.due_time} {self.processing_time} {self.index}"


class PQ_task:
    def __init__(self, task: Task):
        self.task = task

    def __lt__(self, other):
        assert isinstance(other, PQ_task)
        return self.task.processing_time > other.task.processing_time

    def __gt__(self, other):
        assert isinstance(other, PQ_task)
        return self.task.processing_time < other.task.processing_time

    def __eq__(self, other):
        assert isinstance(other, PQ_task)
        return self.task.processing_time == other.task.processing_time

    def __str__(self):
        return f"{self.task.due_time} {self.task.processing_time} {self.task.index}"


size_tasks = int(input())
tasks: list[Task] = []
for i in range(size_tasks):
    processing_time, due_time = map(int, input().split())
    tasks.append(Task(due_time, processing_time, i))

tasks.sort()


pq: PriorityQueue[PQ_task] = PriorityQueue()
number_of_delays = 0
time = 0
for task in tasks:
    pq.put(PQ_task(task))
    time += task.processing_time
    if time > task.due_time:
        number_of_delays += 1
        out_task = pq.get()
        time -= out_task.task.processing_time


print(size_tasks - number_of_delays)
