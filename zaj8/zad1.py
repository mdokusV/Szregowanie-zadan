# plecak

import io
import sys


input_string = """4 20
10 20
5 15
6 6
9 18
"""
sys.stdin = io.StringIO(input_string)


class Task:
    def __init__(self, index: int, processing_time: int, value: int):
        self.index = index
        self.processing_time = processing_time
        self.value = value

    def __str__(self):
        return f"[{self.index}] {self.processing_time} {self.value}"

    def __lt__(self, other: "Task"):
        return self.value / self.processing_time > other.value / other.processing_time

    def __gt__(self, other: "Task"):
        return self.value / self.processing_time < other.value / other.processing_time

    def __eq__(self, other: "Task"):
        return self.value / self.processing_time == other.value / other.processing_time


class Node:
    def __init__(self, weight: int, value: int, level: int, items: list[Task]):
        self.potential_maximum_value = 0
        self.weight = weight
        self.value = value
        self.level = level
        self.items = items

    def update(self, other: "Node"):
        self.weight = other.weight
        self.value = other.value
        self.level = other.level
        self.items = other.items

    def search(self):
        if self.weight > max_weight:
            return
        if self.value > best_node.value:
            best_node.update(self)
        else:
            self.potential()
            if self.potential_maximum_value <= best_node.value:
                return
        if self.level == len(tasks):
            return

        node_left = Node(
            self.weight + tasks[self.level].processing_time,
            self.value + tasks[self.level].value,
            self.level + 1,
            self.items + [tasks[self.level]],
        )
        node_left.search()

        node_right = Node(self.weight, self.value, self.level + 1, self.items)
        node_right.search()

    def potential(self):
        self.potential_maximum_value += self.value
        iterator = self.level
        weight = self.weight
        partial_piece: Task | None = None
        while True:
            if iterator == len(tasks):
                return
            current_task = tasks[iterator]
            if weight + current_task.processing_time > max_weight:
                partial_piece = current_task
                break
            self.potential_maximum_value += current_task.value
            weight += current_task.processing_time
            iterator += 1

        # deal with partial piece
        self.potential_maximum_value += (
            partial_piece.value * (max_weight - weight) / partial_piece.processing_time
        )


task_number, max_weight = map(int, input().split())
tasks = [Task(i, 0, 0) for i in range(task_number)]

for i in range(task_number):
    processing_time, value = map(int, input().split())
    tasks[i].processing_time = processing_time
    tasks[i].value = value
tasks.sort()

print(*tasks, sep="\n")

best_node = Node(0, 0, 0, [])

start_node = Node(0, 0, 0, [])
start_node.search()
print(best_node.value)
