import io
import sys

input_string = """6
1 1
0 3
10 3
2 2
4 1
1 2
5
1 5
2 3
3 5
2 4
2 6
"""
sys.stdin = io.StringIO(input_string)


from queue import PriorityQueue


class Task:
    def __init__(self, relies_time, processing_time, index):
        self.relies_time = relies_time
        self.processing_time = processing_time
        self.index = index
        self.topological_sort = index

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
        return f"relies_time:{self.relies_time} processing_time:{self.processing_time} index:{self.index} topological_sort:{self.topological_sort}"


class Vertex:
    def __init__(self, successors: list[int], number, index):
        self.successors = successors
        self.predecessor_number = number
        self.index: int = index
        self.visited = False

    def sort_successors(self):
        self.successors.sort()

    def __lt__(self, other):
        return self.index < other.index

    def __gt__(self, other):
        return self.index > other.index

    def __eq__(self, other):
        return self.index == other.index

    def __str__(self):
        return f"[{self.index}] successors:{self.successors}, predecessor_number:{self.predecessor_number}"


class Vertices:
    def __init__(self, vertices: list[Vertex]):
        self.vertex: list[Vertex] = vertices
        self.zero_predecessors_pq: PriorityQueue[Vertex] = PriorityQueue()
        self.to_visit = len(vertices)

    def init_priority(self):
        for vertex in self.vertex:
            if vertex.predecessor_number == 0:
                self.zero_predecessors_pq.put(vertex)

    def sort_vertex_successors(self):
        for vertex in self.vertex:
            vertex.sort_successors()

    def delete_vertex(self, index: int):
        for successor in self.vertex[index].successors:
            successor_vert = self.vertex[successor]
            successor_vert.predecessor_number -= 1
            if successor_vert.predecessor_number == 0 and not successor_vert.visited:
                self.zero_predecessors_pq.put(successor_vert)
        self.to_visit -= 1

    def __str__(self):
        return "\n".join([str(vertex) for vertex in self.vertex])


size_operation = int(input())

operations: list[Task] = []
for item in range(size_operation):
    relies_time, processing_time = map(int, input().split())
    operations.append(Task(relies_time, processing_time, item))

size_edges = int(input())

vertices = Vertices([Vertex([], 0, i) for i in range(size_operation)])
for edge in range(size_edges):
    start, end = map(int, input().split())
    vertices.vertex[start - 1].successors.append(end - 1)
    vertices.vertex[end - 1].predecessor_number += 1


vertices.sort_vertex_successors()
vertices.init_priority()


def kahn_algorithm(vertices: Vertices) -> list[int]:
    output: list[int] = []
    while vertices.to_visit > 0:
        vertex = vertices.zero_predecessors_pq.get()
        output.append(vertex.index)
        vertices.delete_vertex(vertex.index)
        vertex.visited = True

    return output


output = kahn_algorithm(vertices)


def update_relies_time_topologically(
    operations: list[Task],
    topological_order: list[int],
    vertices: Vertices,
):
    for order, index_task in enumerate(topological_order):
        operations[index_task].topological_sort = order
    for output_index in topological_order:
        predecessor = operations[output_index]
        for successor in vertices.vertex[output_index].successors:
            successor_task = operations[successor]
            successor_task.relies_time = max(
                successor_task.relies_time,
                predecessor.relies_time + predecessor.processing_time,
            )
    print(*operations, sep="\n", end="\n\n")
    operations.sort()


update_relies_time_topologically(operations, output, vertices)
print(*operations, sep="\n")


def calculate_end_time(operations: list[Task]) -> int:
    time = 0
    for task in operations:
        time = max(time, task.relies_time)
        time += task.processing_time
    return time


print(calculate_end_time(operations))
