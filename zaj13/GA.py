import copy
from dataclasses import dataclass, field
import random
from typing import List, Set

RNG = random.Random()


class Param:
    def __init__(self):
        self.MAX_EPOCHE = 50
        self.MAX_OFFSPRING = 100
        self.MAX_MUTATION = 50
        self.MAX_POPULATION = 100


PARAM = Param()


@dataclass
class Task:

    index: int
    processing_times: List[int] = field(default_factory=list)

    def __str__(self):
        return f"{self.index}"


@dataclass
class Order:
    tasks: List[Task] = field(default_factory=list)
    sum: int = 0

    def __str__(self):
        return f"{self.sum}\n" + " ".join([str(task) for task in self.tasks])

    def calculate_sum(self) -> int:
        times_of_workers = [0 for _ in range(worker_number)]
        for task in self.tasks:
            for worker in range(worker_number):
                if worker == 0:
                    times_of_workers[worker] += task.processing_times[worker]
                else:
                    times_of_workers[worker] = (
                        max(times_of_workers[worker], times_of_workers[worker - 1])
                        + task.processing_times[worker]
                    )

        self.sum = times_of_workers[-1]
        return times_of_workers[-1]

    def mutate(self) -> "Order":
        global RNG

        mutated_order = copy.deepcopy(self)
        take = RNG.randint(0, len(mutated_order.tasks) - 1)
        swap = RNG.randint(1, len(mutated_order.tasks) - 1)
        swap_index = (take + swap) % len(mutated_order.tasks)
        (
            mutated_order.tasks[take],
            mutated_order.tasks[swap_index],
        ) = (
            mutated_order.tasks[swap_index],
            mutated_order.tasks[take],
        )
        mutated_order.calculate_sum()

        return mutated_order

    def __eq__(self, other: "Order") -> bool:
        return self.sum == other.sum

    def __lt__(self, other: "Order") -> bool:
        return self.sum < other.sum

    def __hash__(self) -> int:
        return hash(tuple(task.index for task in self.tasks))


class Population:
    orders: Set[Order] = set()
    best: Order | None = None

    def generate_first_population(self, tasks: List[Task]):
        for _ in range(PARAM.MAX_POPULATION):
            order = Order(tasks[:])
            random.shuffle(order.tasks)
            order.calculate_sum()
            self.orders.add(order)

    def produce_children(self, mother: "Order", father: "Order"):
        global RNG
        separation_point = RNG.randint(
            len(mother.tasks) // 4, len(mother.tasks) * 3 // 4
        )

        # create first child
        child_one_tasks = mother.tasks[:separation_point]
        used_tasks = set(task.index for task in child_one_tasks)
        child_one_tasks.extend(
            task for task in father.tasks if task.index not in used_tasks
        )
        child_one = Order(child_one_tasks)
        child_one.calculate_sum()

        # create second child
        child_two_tasks = father.tasks[:separation_point]
        used_tasks = set(task.index for task in child_two_tasks)
        child_two_tasks.extend(
            task for task in mother.tasks if task.index not in used_tasks
        )
        child_two = Order(child_two_tasks)
        child_two.calculate_sum()

        self.orders.update([child_one, child_two])

    def run(self):
        global RNG
        for epoche in range(PARAM.MAX_EPOCHE):

            # create new children
            for _ in range(PARAM.MAX_OFFSPRING // 2):
                parents = RNG.sample(list(self.orders), 2)
                self.produce_children(parents[0], parents[1])

            # mutate
            for _ in range(PARAM.MAX_MUTATION):
                new_mutated = list(self.orders)[
                    RNG.randint(0, len(self.orders) - 1)
                ].mutate()
                self.orders.add(new_mutated)

            if len(self.orders) > PARAM.MAX_POPULATION:
                self.orders = set(sorted(self.orders)[: PARAM.MAX_POPULATION])

            # self.show_top()

    def show_top(self, n: int = 5):
        for order in sorted(self.orders)[:n]:
            print(order)

    def show_best(self):
        print(sorted(self.orders)[0])


worker_number, task_number = map(int, input().split())

tasks = [Task(i) for i in range(task_number)]

for i in range(task_number):
    tasks[i].processing_times = list(map(int, input().split()))

population = Population()
population.generate_first_population(tasks)
population.run()
# population.show_top(len(population.orders))
population.show_best()
