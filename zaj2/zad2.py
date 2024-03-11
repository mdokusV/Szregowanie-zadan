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


from queue import PriorityQueue


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

    def __lt__(self, other):
        return self.index < other.index

    def __gt__(self, other):
        return self.index > other.index

    def __eq__(self, other):
        return self.index == other.index

    def __str__(self):
        return f"[{self.index}] successors: {self.successors}, predecessor_number:{self.predecessor_number}"


class Vertices:
    def __init__(self, vertices: list[Vertex]):
        self.vertex: list[Vertex] = vertices
        self.zero_predecessors_pq: PriorityQueue = PriorityQueue()

        def init_priority(self):
            for vertex in self.vertex:
                if vertex.predecessor_number == 0:
                    self.zero_predecessors_pq.put(vertex)

        init_priority(self)

    def delete_vertex(self, index: int):
        for successor in self.vertex[index].successors:
            self.vertex[successor].predecessor_number -= 1
        self.vertex = self.vertex[:index] + self.vertex[index + 1 :]

    def __str__(self):
        return "\n".join([str(vertex) for vertex in self.vertex])


size_operation, size_edges = map(int, input().split())

operations: list[Task] = []
for item in range(size_operation):
    processing_time = int(input())
    operations.append(Task(processing_time, item))

vertices = Vertices([Vertex([], 0, i) for i in range(size_operation)])
for edge in range(size_edges):
    start, end = map(int, input().split())
    vertices.vertex[start - 1].successors.append(end - 1)
    vertices.vertex[start - 1].predecessor_number += 1

print(vertices)


def kahn_algorithm(vertices: Vertices) -> list[int]:
    output: list[int] = []
    while len(vertices.vertex) > 0:
        vertix = vertices.zero_predecessors_pq.get()
    return output


output = kahn_algorithm(vertices)
print(*output, sep="\n")

print(sum([task.processing_time for task in operations]))
