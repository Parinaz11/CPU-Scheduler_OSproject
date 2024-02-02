# Taking input
import threading
from queue import PriorityQueue
from queue import Queue

class Task:
    def __init__(self, name, task_type, duration):
        self.name = name
        self.task_type = task_type
        self.duration = duration
        match task_type:
            case 'X':
                self.priority = 1
                self.resources = ['R1','R2']
            case 'Y':
                self.priority = 2
                self.resources = ['R2','R3']
            case 'Z':
                self.priority = 3
                self.resources = ['R1','R3']
        self.state = 'Ready'
        self.exec_time = 0
        

# Global variables
mutex = threading.Lock()
ready_q = PriorityQueue()
waiting_q = Queue()

def sjf_scheduler(core):
    print("Hey I'm core", core)


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
        kernelThread = threading.Thread(target=sjf_scheduler, args=(core,))
        kernal_threads.append(kernelThread)
        kernelThread.start()

    # Waiting for threads to finish
    for kernelThread in kernal_threads:
        kernelThread.join()


if __name__ == "__main__":
    print("---- SJF ---")
    main()
