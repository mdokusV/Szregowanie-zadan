import io
import sys

input_string = """5
8 8
0 3
22 7
25 3
4 7"""
sys.stdin = io.StringIO(input_string)

class Task:
    def __init__(self, relies_time, processing_time, index):
        self.relies_time = relies_time
        self.processing_time = processing_time
        self.index = index

    def __lt__(self, other):
        assert isinstance(other, Task)
        return (self.relies_time, self.index) < (other.relies_time, other.index)

    def __gt__(self, other):
        assert isinstance(other, Task)
        return (self.relies_time, self.index) > (other.relies_time, other.index)

    def __eq__(self, other):
        assert isinstance(other, Task)
        return (self.relies_time, self.index) == (other.relies_time, other.index)

    def __str__(self):
        return f"{self.relies_time} {self.processing_time} {self.index}"


size = int(input())


relies_table: list[Task] = []
for item in range(size):
    relies_time, processing_time = map(int, input().split())
    relies_table.append(Task(relies_time, processing_time, item))

relies_table.sort()

time = 0
output = [0 for _ in range(size)]
for task in relies_table:
    time = max(time, task.relies_time)
    time += task.processing_time
    output[task.index] = time

print(*output, sep="\n")
print(time)