import copy
import random

import scipy
from sympy import Integer


MAX_TIME = 10
RANDOM_CONNECTION = True

class Task:
    def __init__(self, index: int, processing_time: int):
        self.index = index
        self.processing_time = processing_time
        self.setups: list[Setup] = []
        self.required_importance = 0.0

    def __str__(self):
        return f"task {self.index}, processing: {self.processing_time}, required: {self.required_importance}, setups: {sorted([str(setup.index) for setup in self.setups])}"


class Setup:
    def __init__(self, index: int, processing_time: int):
        self.index = index
        self.processing_time = processing_time
        self.tasks: list[Task] = []
        self.importance = 0.0

    def __str__(self):
        return f"setup {self.index}, processing: {self.processing_time},  importance: {self.importance}, tasks: {sorted([str(task.index) for task in self.tasks])}"

    def __hash__(self):
        return self.index

    def __eq__(self, other: "Setup"):
        return self.index == other.index


class Machine:
    def __init__(self, index: int):
        self.index = index
        self.time = 0
        self.tasks_done: list[Task] = []
        self.setups_done: set[Setup] = set()
        self.summed_processing: int = 0

    def sum_time(self) -> int:
        time_sum = sum(task.processing_time for task in self.tasks_done)
        time_sum += sum(setup.processing_time for setup in self.setups_done)
        self.summed_processing = time_sum
        return time_sum

    def copy_order(self, other: "Machine"):
        self.tasks_done = copy.deepcopy(other.tasks_done)
        self.setups_done = copy.deepcopy(other.setups_done)
        self.summed_processing = other.summed_processing

    def __str__(self):
        return f"machine {self.index}, summed time: {self.summed_processing}, tasks done: {sorted([str(task.index) for task in self.tasks_done])}, setups done: {sorted([str(setup.index) for setup in self.setups_done])}"


task_number, setup_number, machine_number = 10, 10, 3


def random_connection(task_number, setup_number):
    connection_matrix = [[0 for _ in range(setup_number)] for _ in range(task_number)]
    for row in connection_matrix:
        random_len = random.randint(1, len(row))
        places_for_one = random.sample(range(len(row)), random_len)
        for place in places_for_one:
            row[place] = 1
    return connection_matrix


if RANDOM_CONNECTION:
    connection_matrix = random_connection(task_number, setup_number)
else:
    connection_matrix = [
        [0, 1, 1],
        [1, 1, 1],
        [1, 0, 0],
    ]


tasks = [Task(i, random.randint(1, MAX_TIME)) for i in range(task_number)]

setups = [Setup(i, random.randint(1, MAX_TIME)) for i in range(setup_number)]

machines = [Machine(i) for i in range(machine_number)]

for task_ind, task_con in enumerate(connection_matrix):
    for (
        set_ind,
        set_con,
    ) in enumerate(task_con):
        if set_con:
            tasks[task_ind].setups.append(setups[set_ind])
            setups[set_ind].tasks.append(tasks[task_ind])


for setup in setups:
    setup.importance = (
        scipy.stats.pmean(
            [task.processing_time for task in setup.tasks],
            3,
        )
        * setup.processing_time
    )

for task in tasks:
    task.required_importance = sum(setup.importance for setup in task.setups)

print(*tasks, sep="\n", end="\n\n")
print(*setups, sep="\n", end="\n\n")


def get_permutation(n: int, base: int):
    binary_list = [not (bool(int(i))) for i in list(bin(n)[2:].zfill(len(tasks)))]
    return [tasks[i] for i, v in enumerate(binary_list) if v == True], [
        tasks[i] for i, v in enumerate(binary_list) if v == False
    ]


def find_best() -> tuple[list[Machine], int]:
    permutation_number = 0
    half_permutations = 2 ** (len(tasks) - 1)

    minimal_summed_time = float("inf")
    best_arrangement = [Machine(i) for i in range(machine_number)]

    times = [0 for _ in range(machine_number)]
    while permutation_number <= half_permutations:
        task_to_machines = get_permutation(permutation_number)
        for machine_ind, machine in enumerate(machines):
            machine.setups_done.clear()
            machine.tasks_done.clear()

            machine.tasks_done.extend(task_to_machines[machine_ind])
            machine.setups_done.update(
                setup for task in task_to_machines[machine_ind] for setup in task.setups
            )

            times[machine_ind] = machine.sum_time()

            # print(
            #     f"""
            #         machine {machine_ind}
            #         tasks: {[task.index for task in machine.tasks_done]}
            #         setups {[setup.index for setup in machine.setups_done]}
            #     """
            # )
        if max(times) < minimal_summed_time:
            minimal_summed_time = max(times)
            for i, machine in enumerate(best_arrangement):
                machine.copy_order(machines[i])

        permutation_number += 1

    return best_arrangement, int(minimal_summed_time)


best_arrangement, minimal_summed_time = find_best()

print()
print(*best_arrangement, sep="\n")
print(minimal_summed_time)
