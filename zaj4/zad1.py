import io
import sys

input_string = """4
1 10
5 12
4 4
3 5
"""
sys.stdin = io.StringIO(input_string)


class Task:
    def __init__(self, due_time, processing_time, index):
        self.due_time = due_time
        self.processing_time = processing_time
        self.end_time = 0
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


size_tasks = int(input())
tasks: list[Task] = []
for i in range(size_tasks):
    processing_time, due_time = map(int, input().split())
    tasks.append(Task(due_time, processing_time, i))

tasks.sort()
time = 0
for task in tasks:
    task.end_time = time + task.processing_time
    time = task.end_time

print(max(task.end_time - task.due_time for task in tasks))
