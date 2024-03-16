import io
import sys

input_string = """5
1 0 1 0
2 0 1 1
2 1 0 0
2 0 1 -1
3 1 1 0
4
5 1
1 4
2 4
2 3
"""
sys.stdin = io.StringIO(input_string)


from queue import PriorityQueue
from math import inf


class Task:
    def __init__(self, processing_time: int, params: list[int], index):
        self.processing_time = processing_time
        self.index = index
        self.__params = params

    def __str__(self):
        return f"index:{self.index} processing_time:{self.processing_time} equation: {self.__params[0]}*t^2 + {self.__params[1]}*t + {self.__params[2]}"

    def cost(self, time):
        return self.__params[0] * time**2 + self.__params[1] * time + self.__params[2]


class Vertex:
    def __init__(self, successors: list[int], number, task: Task, index):
        self.predecessor = successors
        self.successor_number = number
        self.index: int = index
        self.visited = False
        self.task = task

    def sort_predecessor(self):
        self.predecessor.sort()

    def __lt__(self, other):
        return self.index < other.index

    def __gt__(self, other):
        return self.index > other.index

    def __eq__(self, other):
        return self.index == other.index

    def __str__(self):
        return f"[{self.index}] predecessor:{self.predecessor}, successor_number:{self.successor_number}"


class Vertices:
    def __init__(self, vertices: list[Vertex]):
        self.vertex: list[Vertex] = vertices
        self.zero_successor_list: list[Vertex] = []
        self.to_visit = len(vertices)

    def init_priority(self):
        for vertex in self.vertex:
            if vertex.successor_number == 0:
                self.zero_successor_list.append(vertex)

    def sort_vertex_predecessor(self):
        for vertex in self.vertex:
            vertex.sort_predecessor()

    def delete_vertex(self, index: int):
        self.zero_successor_list.remove(self.vertex[index])
        for predecessor in self.vertex[index].predecessor:
            predecessor_vert = self.vertex[predecessor]
            predecessor_vert.successor_number -= 1
            if predecessor_vert.successor_number == 0 and not predecessor_vert.visited:
                self.zero_successor_list.append(predecessor_vert)
        self.to_visit -= 1

    def __str__(self):
        return "\n".join([str(vertex) for vertex in self.vertex])


size_operation = int(input())
operations: list[Task] = []
for i in range(size_operation):
    params = list(map(int, input().split()))
    operations.append(Task(params[0], params[1:], i))

size_edges = int(input())
vertices = Vertices([Vertex([], 0, operations[i], i) for i in range(size_operation)])
for edge in range(size_edges):
    start, end = map(int, input().split())
    vertices.vertex[end - 1].predecessor.append(start - 1)
    vertices.vertex[start - 1].successor_number += 1
vertices.init_priority()

time = sum([task.processing_time for task in operations])

order_tasks: list[Task] = []
worst_village = -inf
while vertices.to_visit > 0:
    best_cost, task = inf, Task(0, [], 0)
    for vertex in vertices.zero_successor_list:
        cost = vertex.task.cost(time)
        if cost < best_cost:
            best_cost = cost
            task = vertex.task
    time -= task.processing_time
    if best_cost > worst_village:
        worst_village = best_cost

    order_tasks.append(task)
    vertices.delete_vertex(task.index)

print(worst_village)
