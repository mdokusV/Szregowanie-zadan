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
7 2
"""
sys.stdin = io.StringIO(input_string)


class Task:
    def __init__(self, processing_time, index):
        self.processing_time = processing_time
        self.index = index

    def __str__(self):
        return f"processing_time: {self.processing_time}, index:{self.index}"


class Vertex:

    def __init__(self, successors, number, index):
        self.successors: list[int] = successors
        self.predecessor_number = number
        self.index = index
        self.visited = False

    def __str__(self):
        return f"[{self.index}] successors: {self.successors}, predecessor_number:{self.predecessor_number}"


size_operation, size_edges = map(int, input().split())

operations: list[Task] = []
for item in range(size_operation):
    processing_time = int(input())
    operations.append(Task(processing_time, item))

vertices: list[Vertex] = [Vertex([], 0, i) for i in range(size_operation)]
for edge in range(size_edges):
    start, end = map(int, input().split())
    vertices[start - 1].successors.append(end - 1)
    vertices[start - 1].predecessor_number += 1


def dfs(vertices: list[Vertex]) -> list[int]:
    output: list[int] = []

    def dfs_visit(vertex: Vertex):
        vertex.visited = True
        for successor in vertex.successors[::-1]:
            if not vertices[successor].visited:
                dfs_visit(vertices[successor])
        output.append(vertex.index + 1)

    for vertex in vertices[::-1]:
        if not vertex.visited:
            dfs_visit(vertex)
    return list(reversed(output))


output = dfs(vertices)
print(*output, sep="\n")

print(sum([task.processing_time for task in operations]))
