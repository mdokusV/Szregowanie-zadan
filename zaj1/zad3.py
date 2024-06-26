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


class Task:
    def __init__(self, relies_time, processing_time, index):
        self.relies_time = relies_time
        self.processing_time = processing_time
        self.index = index

    def __lt__(self, other):
        return (self.processing_time, self.index) < (other.processing_time, other.index)

    def __gt__(self, other):
        return (self.processing_time, self.index) > (other.processing_time, other.index)

    def __eq__(self, other):
        return (self.processing_time, self.index) == (
            other.processing_time,
            other.index,
        )

    def __str__(self):
        return f"{self.relies_time} {self.processing_time} {self.index}"


from queue import PriorityQueue


relies_table: list[Task] = []
timestamps = []
for i in range(size):
    relies_time, processing_time = map(int, input().split())
    relies_table.append(Task(relies_time, processing_time, i))
    timestamps.append(relies_time)

solution = [0 for _ in range(size)]

pq: PriorityQueue[Task] = PriorityQueue()


while len(timestamps) >= 2:
    time = timestamps.pop(1)
    new_task = relies_table.pop(0)
    pq.put(new_task)
    current_task = pq.get()
    while current_task.relies_time < time:
        if current_task.processing_time < time - current_task.relies_time:
            time_passed = current_task.processing_time + current_task.relies_time
            solution[current_task.index] = time_passed

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
    solution[current_task.index] = time

for i in solution:
    print(i)
print(solution)
