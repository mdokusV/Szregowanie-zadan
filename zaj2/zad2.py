import io
import sys

input_string = """7 7
3
5
1
2
7
4
3
5 1
1 4
1 2
3 6
6 4
3 7
7 2"""
sys.stdin = io.StringIO(input_string)


class Task:
    def __init__(self, processing_time, index):
        self.processing_time = processing_time
        self.index = index

    def __str__(self):
        return f"{self.processing_time} {self.index}"


class Vertex:
    def __init__(self, successors, number):
        self.successors = successors
        self.predecessor_number = number

    def __str__(self):
        return f"successors: {self.successors}, predecessor_number:{self.predecessor_number}"


size_operation, size_edges = map(int, input().split())
print(size_operation, size_edges)

operations: list[Task] = []
for item in range(size_operation):
    processing_time = int(input())
    operations.append(Task(processing_time, item))

successors: list[Vertex] = [Vertex([], 0) for _ in range(size_operation)]
for edge in range(size_edges):
    start, end = map(int, input().split())
    successors[start - 1].successors.append(end - 1)
    successors[start - 1].predecessor_number += 1

for task in operations:
    print(task.processing_time)

for vertex in successors:
    print(vertex)
