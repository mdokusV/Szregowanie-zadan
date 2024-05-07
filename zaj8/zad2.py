# 1||sum wj * Uj

import io
import sys


input_string = """4
3 4 3
2 5 4
5 6 8
4 4 10
"""
sys.stdin = io.StringIO(input_string)


class Task:
    def __init__(self, index: int, processing_time: int, value: int, due_time: int):
        self.index = index
        self.processing_time = processing_time
        self.value = value
        self.due_time = due_time

    def __str__(self):
        return f"[{self.index}] {self.processing_time} {self.value} {self.due_time}"


class Node:
    def __init__(self, time: int, value: int, level: int, items: list[Task]):
        self.potential_maximum_value = 0
        self.time = time
        self.value = value
        self.level = level
        self.items = items

    def update(self, other: "Node"):
        self.time = other.time
        self.value = other.value
        self.level = other.level
        self.items = other.items

    def search(self):
        if len(self.items) and self.time > self.items[-1].due_time:
            return

        if self.value < best_node.value and self.level == len(tasks):
            best_node.update(self)
        else:
            self.potential()
            if self.potential_maximum_value >= best_node.value:
                return
        if self.level == len(tasks):
            return

        node_left = Node(
            self.time + tasks[self.level].processing_time,
            self.value,
            self.level + 1,
            self.items + [tasks[self.level]],
        )
        node_left.search()

        node_right = Node(
            self.time,
            self.value + tasks[self.level].value,
            self.level + 1,
            self.items,
        )
        node_right.search()

    def potential(self):
        self.potential_maximum_value = self.value + sum(
            task.value
            for task in tasks[self.level :]
            if self.time + task.processing_time > task.due_time
        )


task_number = int(input())
tasks = [Task(i, 0, 0, 0) for i in range(task_number)]

for i in range(task_number):
    processing_time, value, due_time = map(int, input().split())
    tasks[i].processing_time = processing_time
    tasks[i].value = value
    tasks[i].due_time = due_time

task_sum = sum(task.value for task in tasks)
print(*tasks, sep="\n")
best_node = Node(0, task_sum, 0, [])

start_node = Node(0, 0, 0, [])
start_node.search()
print(task_sum - best_node.value)
