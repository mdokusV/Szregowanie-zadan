import random

MAX_TIME = 10

class Task:
    def __init__(self, index: int, processing_time: int):
        self.index = index
        self.processing_time = processing_time
        self.setups: list[Setup] = []

    def __str__(self):
        return f"task {self.index}, processing time: {self.processing_time}, setups: {[str(setup) for setup in self.setups]}"


class Setup:
    def __init__(self, index: int, processing_time: int):
        self.index = index
        self.processing_time = processing_time
        self.tasks: list[Task] = []

    def __str__(self):
        return f"setup {self.index}, processing time: {self.processing_time}"

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


task_number, setup_number, machine_number = 3, 2, 2

connection_matrix = [
    [random.choice([0, 1]) for _ in range(setup_number)] for _ in range(task_number)
]


tasks = [Task(i, random.randint(1, MAX_TIME)) for i in range(task_number)]

setups = [Setup(i, random.randint(1, MAX_TIME)) for i in range(machine_number)]

machines = [Machine(i) for i in range(machine_number)]

for task_ind, task_con in enumerate(connection_matrix):
    for (
        set_ind,
        set_con,
    ) in enumerate(task_con):
        if set_con:
            tasks[task_ind].setups.append(setups[set_ind])
            setups[set_ind].tasks.append(tasks[task_ind])

print(*tasks, sep="\n")


def get_permutation(n):
    binary_list = [not (bool(int(i))) for i in list(bin(n)[2:].zfill(len(tasks)))]
    return [tasks[i] for i, v in enumerate(binary_list) if v == True], [
        tasks[i] for i, v in enumerate(binary_list) if v == False
    ]


def find_best():
    permutation_number = 0
    half_permutations = 2 ** (len(tasks) - 1)

    miniman_summed_time = float("inf")

    while permutation_number <= half_permutations:
        task_to_machines = get_permutation(permutation_number)
        print(f"permutation number: {permutation_number}")
        for machine_ind, machine in enumerate(machines):
            machine.setups_done.clear()
            machine.tasks_done.clear()

            machine.tasks_done.extend(task_to_machines[machine_ind])
            machine.setups_done.update(
                setup for task in task_to_machines[machine_ind] for setup in task.setups
            )

            # print(
            #     f"""
            #         machine {machine_ind}
            #         tasks: {[task.index for task in machine.tasks_done]}
            #         setups {[setup.index for setup in machine.setups_done]}
            #     """
            # )
        permutation_number += 1


find_best()
