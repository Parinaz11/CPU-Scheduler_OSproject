import threading
from queue import PriorityQueue
import time

class Task:
    def __init__(self, name, task_type, duration):
        self.name = name
        self.task_type = task_type
        self.duration = duration
        self.resources = []
        self.state = 'Ready'
        self.exec_time = 0
        self.priority = 0

        if task_type == 'X':
            self.resources = ['R1', 'R2']
            self.priority = 3
        elif task_type == 'Y':
            self.resources = ['R2', 'R3']
            self.priority = 2
        elif task_type == 'Z':
            self.resources = ['R1', 'R3']
            self.priority = 1

mutex = threading.Lock()
waiting_q = PriorityQueue()  # Priority queue for SJF scheduling
ready_q = PriorityQueue()  # Ready queue for tasks ready to be executed
timeUnit = 1
core = 1
kernel_threads = []
cores_in_use = 0
print_mutex = threading.Lock()

def SJF(ready_q):
    global core
    global cores_in_use
    global timeUnit
    global tasks
# sort ready queue according to duration time and the rest like fcfs
    duration_list = []
    while not ready_q.empty():
        task = ready_q.get()
        duration_list.append((task.priority, task))  # Use priority for sorting
    print(duration_list)
    duration_list.sort()
    print(duration_list)

    
def execute_task(core, task):
    global timeUnit
    global mutex
    global print_mutex

    print(f"Core {core}: Executing {task.name} with Duration: {task.duration} in time: {timeUnit}")

    time.sleep(task.duration)

    task.state = 'Completed'
    task.exec_time = task.duration
    print(f"Core {core}: {task.name} completed in time: {timeUnit}")

    with mutex:
        print(f"Core {core}: Releasing resources {task.resources}")

        global cores_in_use
        cores_in_use -= 1

        with print_mutex:
            print_execution_result(core, task)

def print_execution_result(core, task):
    print(f"Core {core}: {task.name} completed in time: {timeUnit}")

def print_results():
    global kernel_threads
    for thread in kernel_threads:
        thread.join()

    print("\nExecution Results:")
    for task in tasks:
        print(f"{task.name}: State: {task.state}, Execution Time: {task.exec_time}")

def main():
    global core
    num_resources = list(map(int, input("Enter the data for resources and tasks:\n").split()))
    num_tasks = int(input())
    tasks = []

    for _ in range(num_tasks):
        task_data = input().split()
        task_name, task_type, duration = task_data[0], task_data[1], int(task_data[2])
        t = Task(task_name, task_type, duration)
        tasks.append(t)

    print(f"Resources: {num_resources}")
    print(f"Number of tasks: {num_tasks}")
    print("Task details:")
    count = 1

    # for task in tasks:
    #     waiting_q.put((task.duration, task))  # Enqueue tasks with priority based on their duration

    for task in tasks: 
        ready_q.put(task)

    for task in tasks:
        print(f"{count}) Duration: {task.duration}, Type: {task.task_type}, Name: {task.name}, State: {task.state}, Time On CPU: {task.exec_time}")
        count += 1

    # Start the printing thread
    print_thread = threading.Thread(target=print_results)
    print_thread.start()

    # Start the SJF scheduling
    SJF(ready_q)

    # Wait for the printing thread to finish
    print_thread.join()

if __name__ == "__main__":
    print("---- SJF ---")
    main()