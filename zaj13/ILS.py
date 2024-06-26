import random

RNG = random.Random()


class Param:
    def __init__(self):
        self.ITER_MAX = 200
        self.LOCAL_SEARCH = 50
        self.PerturbationStrength = 0


PARAM = Param()


class Task:

    def __init__(self, index: int):
        self.index = index
        self.processing_times: list[int] = []
        self.sum: int = 0

    def __str__(self):
        return f"{self.index}"

    def __lt__(self, other: "Task"):
        return self.sum > other.sum

    def __eq__(self, other: "Task"):
        return self.sum == other.sum

    def __gt__(self, other: "Task"):
        return self.sum < other.sum


class Order:
    def __init__(self, tasks: list[Task]):
        self.tasks = tasks
        self.sum: int = 0

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

    def copy_order(self, other: "Order"):
        for task_ind in range(len(other.tasks)):
            self.tasks[task_ind] = other.tasks[task_ind]

        self.sum = other.sum

    def perturbate(self):
        for _ in range(
            RNG.randint(2, max(len(self.tasks) // 10, 2 + PARAM.PerturbationStrength))
        ):
            take = RNG.randint(0, len(self.tasks) - 1)
            swap = RNG.randint(1, len(self.tasks) - 1)
            (
                self.tasks[take],
                self.tasks[(take + swap) % len(self.tasks)],
            ) = (
                self.tasks[(take + swap) % len(self.tasks)],
                self.tasks[take],
            )
        self.calculate_sum()

    def local_search(self):
        take = RNG.randint(0, len(self.tasks) - 1)
        swap = RNG.randint(1, len(self.tasks) - 1)
        swap_index = (take + swap) % len(self.tasks)
        (
            self.tasks[take],
            self.tasks[swap_index],
        ) = (
            self.tasks[swap_index],
            self.tasks[take],
        )
        if self in cache.cache_order:
            return
        self.calculate_sum()

    def __hash__(self) -> int:
        return hash(tuple(task.index for task in self.tasks))

    def __eq__(self, other: "Order") -> bool:
        return self.tasks == other.tasks


class Cache:
    def __init__(self):
        self.cache_order: set[Order] = set()


worker_number, task_number = map(int, input().split())

tasks = [Task(i) for i in range(task_number)]

for i in range(task_number):
    tasks[i].processing_times = list(map(int, input().split()))
    tasks[i].sum = sum(tasks[i].processing_times)

tasks.sort()

cache = Cache()

best_order = Order(tasks.copy())
best_order.calculate_sum()
new_orders = Order(tasks.copy())
local_order = Order(tasks.copy())
order_missis = 0

cache.cache_order.add(best_order)


for i in range(PARAM.ITER_MAX):
    # Generate new perturbation from best
    new_orders.copy_order(best_order)
    new_orders.perturbate()

    # if it is better then replace it and reset PerturbationStrength
    if new_orders.sum < best_order.sum:
        best_order.copy_order(new_orders)
        PARAM.PerturbationStrength = 0
        order_missis = 0

    # Local search
    for j in range(PARAM.LOCAL_SEARCH):
        local_order.copy_order(new_orders)
        local_order.local_search()

        # if already checked then skip
        if local_order in cache.cache_order:
            order_missis += 1
            continue
        cache.cache_order.add(local_order)

        # if it is better then replace it and reset PerturbationStrength
        if local_order.sum < best_order.sum or (
            local_order.sum <= best_order.sum
            and PARAM.PerturbationStrength > len(tasks) // 2
        ):
            best_order.copy_order(local_order)
            PARAM.PerturbationStrength = 0
            order_missis = 0

    # if there are to many misses then increase PerturbationStrength
    if order_missis > PARAM.LOCAL_SEARCH:
        if PARAM.PerturbationStrength < len(tasks):
            PARAM.PerturbationStrength += 1


best_order.calculate_sum()
print(best_order)
