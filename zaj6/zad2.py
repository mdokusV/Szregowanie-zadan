# wspólcz wi dane dla maszyny 1/vi


# SPT
import io
import sys

input_string = """3 8
2 3 6
10
12
7
6
9
8
4
9
"""
sys.stdin = io.StringIO(input_string)

from queue import PriorityQueue


class Machine:
    def __init__(self, index: int, time_to_make_one_part: int):
        self.index = index
        self.summed_time = 0
        self.time_to_make_one_part = time_to_make_one_part
        self.weight = time_to_make_one_part

    def __str__(self):
        return f"[{self.index}] {self.summed_time} {self.time_to_make_one_part}\n"

    def __lt__(self, other):
        assert isinstance(other, Machine)
        return (self.weight, self.time_to_make_one_part) < (
            other.weight,
            other.time_to_make_one_part,
        )

    def __gt__(self, other):
        assert isinstance(other, Machine)
        return (self.weight, self.time_to_make_one_part) > (
            other.weight,
            other.time_to_make_one_part,
        )

    def __eq__(self, other):
        assert isinstance(other, Machine)
        return (self.weight, self.time_to_make_one_part) == (
            other.weight,
            other.time_to_make_one_part,
        )


class Task:
    def __init__(self, index: int, processing_time: int):
        self.index = index
        self.number_of_parts = processing_time
        self.finished = 0

    def __str__(self):
        return f"[{self.index}] {self.number_of_parts}\n"


machine_number, task_number = map(int, input().split())
speeds = list(map(int, input().split()))
machines = [Machine(i, speeds[i]) for i in range(machine_number)]


tasks: list[Task] = []
for i in range(task_number):
    tasks.append(Task(i, int(input())))

tasks.sort(key=lambda task: task.number_of_parts, reverse=True)

for ind, task in enumerate(tasks):
    task.index = ind

pq: PriorityQueue[Machine] = PriorityQueue()

for machine in machines:
    pq.put(machine)

for task in tasks:
    machine = pq.get()
    machine.summed_time += task.number_of_parts * machine.time_to_make_one_part
    task.finished = task.number_of_parts * machine.weight
    machine.weight += machine.time_to_make_one_part
    pq.put(machine)

print(sum(task.finished for task in tasks))
