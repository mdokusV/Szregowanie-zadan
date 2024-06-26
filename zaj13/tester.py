# tester.py

import subprocess
import time
import concurrent.futures
import random
import logging
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
sizes = [5, 10, 15, 20]
num_instances = 10


def generate_test_instance(task_number, worker_number):
    processing_times = [
        [random.randint(1, 100) for _ in range(worker_number)]
        for _ in range(task_number)
    ]
    input_string = f"{task_number} {worker_number}\n"
    input_string += "\n".join(" ".join(map(str, times)) for times in processing_times)
    return input_string


def run_algorithm(script_name, input_data):
    start_time = time.time()
    process = subprocess.Popen(
        ["python3", script_name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate(input=input_data.encode())
    end_time = time.time()
    if process.returncode != 0:
        logging.error(f"Error running {script_name}: {stderr.decode()}")
    return stdout.decode(), end_time - start_time


def run_tests() -> dict[str, dict[int, list[tuple[float, float]]]]:
    results: dict[str, dict[int, list[tuple[float, float]]]] = {
        "GA": {},
        "ILS": {},
        "SA": {},
    }

    for size in sizes:
        results["GA"][size] = []
        results["ILS"][size] = []
        results["SA"][size] = []
        logging.info(f"Running tests for size: {size}")
        for _ in range(num_instances):
            input_data = generate_test_instance(size, size)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_ga = executor.submit(run_algorithm, "GA.py", input_data)
                future_ils = executor.submit(run_algorithm, "ILS.py", input_data)
                future_sa = executor.submit(run_algorithm, "SA.py", input_data)

                ga_output, ga_time = future_ga.result()
                ils_output, ils_time = future_ils.result()
                sa_output, sa_time = future_sa.result()

                ga_result = int(ga_output.split("\n")[0])
                ils_result = int(ils_output.split("\n")[0]) / ga_result
                sa_result = int(sa_output.split("\n")[0]) / ga_result
                ga_result = 1.0

                results["GA"][size].append((ga_time, ga_result))
                results["ILS"][size].append((ils_time, ils_result))
                results["SA"][size].append((sa_time, sa_result))

    return results


def calculate_average_results(
    results: dict[str, dict[int, list[tuple[float, float]]]]
) -> dict[str, dict[int, tuple[float, float]]]:
    averaged_results: dict[str, dict[int, tuple[float, float]]] = {
        "GA": {},
        "ILS": {},
        "SA": {},
    }

    for size in sizes:
        for algo in averaged_results.keys():
            times = [time for time, _ in results[algo][size]]
            qualities = [quality for _, quality in results[algo][size]]
            avg_time = sum(times) / len(times)
            avg_quality = sum(qualities) / len(qualities)
            averaged_results[algo][size] = (avg_time, avg_quality)

    return averaged_results


def plot_execution_time(results: dict[str, dict[int, tuple[float, float]]]):
    ga_times = [avg_time for avg_time, _ in results["GA"].values()]
    ils_times = [avg_time for avg_time, _ in results["ILS"].values()]
    sa_times = [avg_time for avg_time, _ in results["SA"].values()]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sizes, ga_times, marker="o", label="Genetic Algorithm", color="r")
    ax.plot(sizes, ils_times, marker="o", label="Iterated Local Search", color="g")
    ax.plot(sizes, sa_times, marker="o", label="Simulated Annealing", color="b")
    ax.set_xlabel("Input Size")
    ax.set_ylabel("Average Execution Time (seconds)")
    ax.set_title("Average Execution Time by Input Size")
    ax.legend()
    ax.grid(True)
    return fig


def plot_quality(results: dict[str, dict[int, tuple[float, float]]]):
    ga_quality = [avg_quality for _, avg_quality in results["GA"].values()]
    ils_quality = [avg_quality for _, avg_quality in results["ILS"].values()]
    sa_quality = [avg_quality for _, avg_quality in results["SA"].values()]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sizes, ga_quality, marker="o", label="Genetic Algorithm", color="r")
    ax.plot(sizes, ils_quality, marker="o", label="Iterated Local Search", color="g")
    ax.plot(sizes, sa_quality, marker="o", label="Simulated Annealing", color="b")
    ax.set_xlabel("Input Size")
    ax.set_ylabel("Quality (Relative to GA)")
    ax.set_title("Solution Quality by Input Size")
    ax.legend()
    ax.grid(True)
    return fig


def generate_report(averaged_results: dict[str, dict[int, tuple[float, float]]]):
    fig_time = plot_execution_time(averaged_results)
    img_buffer_time = BytesIO()
    fig_time.savefig(img_buffer_time, format="png")
    img_buffer_time.seek(0)

    fig_quality = plot_quality(averaged_results)
    img_buffer_quality = BytesIO()
    fig_quality.savefig(img_buffer_quality, format="png")
    img_buffer_quality.seek(0)

    c = canvas.Canvas("report.pdf", pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 50, "Comparative Analysis of Scheduling Algorithms")
    c.drawString(100, height - 70, "Execution Time and Solution Quality")

    y = height - 100

    # Draw the execution time plot image
    c.drawImage(ImageReader(img_buffer_time), 100, y - 300, width=400, height=300)
    y -= 320

    # Draw the quality plot image
    c.drawImage(ImageReader(img_buffer_quality), 100, y - 300, width=400, height=300)

    c.showPage()
    c.save()


def main():
    results = run_tests()
    averaged_results = calculate_average_results(results)
    generate_report(averaged_results)
    logging.info("Report generated successfully.")


if __name__ == "__main__":
    main()
