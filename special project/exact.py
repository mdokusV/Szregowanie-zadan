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

    def sum_time(self) -> int:
        time_sum = sum(task.processing_time for task in self.tasks_done)
        time_sum += sum(setup.processing_time for setup in self.setups_done)
        return time_sum

    def __str__(self):
        return f"machine {self.index}, tasks done: {[str(task) for task in self.tasks_done]}, setups done: {[str(setup) for setup in self.setups_done]}"


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
            best_arrangement = machines.copy()

        permutation_number += 1

    return best_arrangement, int(minimal_summed_time)


best_arrangement, minimal_summed_time = find_best()

print(*best_arrangement, sep="\n")
print(minimal_summed_time)
