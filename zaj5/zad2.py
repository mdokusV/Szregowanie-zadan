import io
import sys

input_string = """3 8
2
5
4
1
7
4
7
3
"""
sys.stdin = io.StringIO(input_string)


class Machine:
    def __init__(self, index: int):
        self.index = index
        self.summed_time = 0
        self.tasks_done: list[tuple[int, int, int]] = []

    def __str__(self):
        str = f"{self.index+1}: "
        for task in self.tasks_done:
            str += f"{task[0]}[{task[1]},{task[2]}] "
        return str + "\n"


class Task:
    def __init__(self, index: int, processing_time: int):
        self.index = index
        self.processing_time = processing_time

    def __str__(self):
        return f"[{self.index}] {self.processing_time}\n"

    def __lt__(self, other):
        assert isinstance(other, Task)
        return self.processing_time > other.processing_time

    def __gt__(self, other):
        assert isinstance(other, Task)
        return self.processing_time < other.processing_time

    def __eq__(self, other):
        assert isinstance(other, Task)
        return self.processing_time == other.processing_time


machine_number, task_number = map(int, input().split())
machines = [Machine(i) for i in range(machine_number)]


tasks: list[Task] = []
for i in range(task_number):
    tasks.append(Task(i, int(input())))
complete_time_max = max(
    sum(task.processing_time for task in tasks) / machine_number,
    max(task.processing_time for task in tasks),
)
complete_time_max = int(complete_time_max)
print(complete_time_max)

time = 0
machine = machines[0]
for task in tasks:
    if time + task.processing_time <= complete_time_max:
        machine.tasks_done.append((task.index + 1, time, time + task.processing_time))

        if (
            time + task.processing_time == complete_time_max
            and machine.index + 1 < machine_number
        ):
            machine = machines[machine.index + 1]
            time = 0
        else:
            time = time + task.processing_time

    else:
        machine.tasks_done.append((task.index + 1, time, complete_time_max))
        machine = machines[machine.index + 1]
        machine.tasks_done.append(
            (task.index + 1, 0, task.processing_time - (complete_time_max - time))
        )
        time = task.processing_time - (complete_time_max - time)

print(*machines, sep="")
