# Taking input
import threading
from queue import PriorityQueue
from queue import Queue

class Task:
    def __init__(self, name, task_type, duration):
        self.name = name
        self.task_type = task_type
        self.duration = duration
        self.resources = []
        self.state = 'Ready'
        self.exec_time = 0
        self.priority = 0

        # Setting resources and priority based on task type
        if task_type == 'X':
            self.resources = ['R1', 'R2']
            self.priority = 1
        elif task_type == 'Y':
            self.resources = ['R2', 'R3']
            self.priority = 2
        elif task_type == 'Z':
            self.resources = ['R1', 'R3']
            self.priority = 3


# Global variables
mutex = threading.Lock()
ready_q = PriorityQueue()
waiting_q = Queue()

def sjf_scheduler(core):
    global ready_q
    global waiting_q

    while True:
        with mutex:
            if not ready_q.empty():
                _, task = ready_q.get()
            else:
                task = None

        if task:
            print(f"Core {core}: Executing Task {task.name}")
            execute_task(core, task)
            task.exec_time += 1

            with mutex:
                if task.exec_time < task.duration:
                    ready_q.put(task)
                else:
                    task.state = "Finished"
            # Simulating time passing
            # You can adjust the sleep time based on your requirements
            time.sleep(1)
        else:
            with mutex:
                print(f"Core {core}: Time - Idle")
            # Simulating idle time
            # You can adjust the sleep time based on your requirements
            time.sleep(1)

def execute_task(core, task):
    # Placeholder function for task execution
    print(f"Core {core}: Executing {task} with Duration: {task.duration}")

def main():
    num_resources = list(map(int, input("Enter the data for resources and tasks:\n").split()))
    num_tasks = int(input())
    tasks = []
    for _ in range(num_tasks):
        task_data = input().split()
        task_name, task_type, duration = (task_data[0]), (task_data[1]), int(task_data[2])
        t = Task(task_name, task_type, duration)
        tasks.append(t)

    print(f"Resources: {num_resources}")
    print(f"Number of tasks: {num_tasks}")
    print("Task details:")
    count = 1
    # Putting all the tasks in ready queue
    for task in tasks:
        ready_q.put((task.priority, task.name))
        print(f"{count}) Duration: {task.duration}, Type: {task.task_type}, Name: {task.name}, State: {task.state}, Time On CPU: {task.exec_time}")
        count += 1

    kernal_threads = []
    for core in range(1, 5):
        kernel_thread = threading.Thread(target = sjf_scheduler, args = (core,))
        kernal_threads.append(kernel_thread)
        kernel_thread.start()

    # Waiting for threads to finish
    for kernel_thread in kernal_threads:
        kernel_thread.join()

if __name__ == "__main__":
    print("---- SJF ---")
    main()