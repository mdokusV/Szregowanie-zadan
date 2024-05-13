class Task:
    def __init__(self, index: int, processing_time: int):
        self.index = index
        self.processing_time = processing_time
        self.setups: list[Setup] = []


class Setup:
    def __init__(self, index: int, processing_time: int):
        self.index = index
        self.processing_time = processing_time
        self.tasks: list[Task] = []


task_number, machine_number = 3, 2


tasks = [Task(i, 1) for i in range(task_number)]

setups = [Setup(i, 1) for i in range(machine_number)]
