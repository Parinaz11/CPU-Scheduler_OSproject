import threading
from queue import Queue
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
waiting_q = Queue()
ready_q = Queue()
timeUnit = 1
core = 1
tasks = []
cores_in_use = 0

# New lock for resource synchronization
resource_lock = threading.Lock()
resources = {'R1': 1, 'R2': 1, 'R3': 1}  # Initial number of available resources

def SJF(ready_q):
    global core
    global cores_in_use
    global timeUnit

    while True:
        mutex.acquire()
        duration_list = sorted([(task.duration, task) for task in ready_q.queue])
        mutex.release()

        mutex.acquire()
        if cores_in_use < 4 and duration_list:  # Check available cores and tasks
            cores_in_use += 1
            current_task = duration_list.pop(0)[1]  # Pop the task with the shortest duration
            mutex.release()

            kernel_thread = threading.Thread(target=execute_task, args=(core, current_task))
            kernel_thread.start()  # Start the new thread
            core += 1

            if core == 5:
                timeUnit += 1
                core = 1
        else:
            mutex.release()
            break

def execute_task(core, task):
    global timeUnit
    global resources

    # Acquire resources
    with resource_lock:
        resources_available = all(resources[resource] > 0 for resource in task.resources)

        if resources_available:
            for resource in task.resources:
                resources[resource] -= 1

            print(f"Core {core}: {task.name} acquired resources {task.resources} in time: {timeUnit}")
        else:
            waiting_q.put(task)
            return

    print(f"Core {core}: Executing {task.name} with Duration: {task.duration} in time: {timeUnit}")

    time.sleep(task.duration)

    # Release resources
    with resource_lock:
        for resource in task.resources:
            resources[resource] += 1

        print(f"Core {core}: Releasing resources {task.resources} in time: {timeUnit + task.exec_time}")

    task.state = 'Completed'
    task.exec_time = task.duration

    with mutex:
        global cores_in_use
        cores_in_use -= 1

    SJF(waiting_q)

def print_results():
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()

    print("\nExecution Results:")
    for task in tasks:
        print(f"{task.name}: State: {task.state}, Execution Time: {task.exec_time}")

def main():
    global core

    num_resources = list(map(int, input("Enter the data for resources and tasks:\n").split()))
    resources["R1"]=num_resources[0]
    resources["R2"]=num_resources[1]
    resources["R3"]=num_resources[2]
    num_tasks = int(input())

    for _ in range(num_tasks):
        task_data = input().split()
        task_name, task_type, duration = task_data[0], task_data[1], int(task_data[2])
        t = Task(task_name, task_type, duration)
        tasks.append(t)

    print(f"Resources: {num_resources}")
    print(f"Number of tasks: {num_tasks}")
    print("Task details:")
    count = 1

    for task in tasks: 
        ready_q.put(task)

    for task in tasks:
        print(f"{count}) Duration: {task.duration}, Type: {task.task_type}, Name: {task.name}, State: {task.state}")
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
