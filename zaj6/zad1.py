# SPT
import io
import sys

input_string = """3 7
6
2
4
3
2
6
4
"""
sys.stdin = io.StringIO(input_string)


class Machine:
    def __init__(self, index: int):
        self.index = index
        self.summed_time = 0


class Task:
    def __init__(self, index: int, processing_time: int):
        self.index = index
        self.processing_time = processing_time
        self.finished = 0

    def __str__(self):
        return f"[{self.index}] {self.processing_time}\n"

    def __lt__(self, other):
        assert isinstance(other, Task)
        return self.processing_time < other.processing_time

    def __gt__(self, other):
        assert isinstance(other, Task)
        return self.processing_time > other.processing_time

    def __eq__(self, other):
        assert isinstance(other, Task)
        return self.processing_time == other.processing_time


machine_number, task_number = map(int, input().split())
machines = [Machine(i) for i in range(machine_number)]


tasks: list[Task] = []
for i in range(task_number):
    tasks.append(Task(i, int(input())))
tasks.sort()

machine_ind = 0
for task in tasks:
    machine = machines[machine_ind]
    machine.summed_time += task.processing_time
    task.finished = machine.summed_time
    machine_ind = (machine_ind + 1) % machine_number

print(sum(task.finished for task in tasks))
