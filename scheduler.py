import threading
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
kernel_threads = []

def FCFS(ready_q):
    while not ready_q.empty():
        current_task = ready_q.get()
        kernel_thread = threading.Thread(target=execute_task, args=(core, current_task))
        kernel_threads.append(kernel_thread)
        core += 1
        if core == 4:
            timeUnit += 1
            kernel_thread.start()

def execute_task(core, task):
    global timeUnit
    global mutex

    print(f"Core {core}: Executing {task.name} with Duration: {task.duration} in time : {timeUnit}")

    # Simulating task execution by sleeping for the task's duration
    import time
    time.sleep(task.duration)

    # Updating task state and execution time
    task.state = 'Completed'
    task.exec_time = task.duration
    print(f"Core {core}: {task.name} completed in time : {timeUnit}")

    # Release resources
    with mutex:
        print(f"Core {core}: Releasing resources {task.resources}")
        # Add logic to release resources if needed

def main():
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

    for priority in range(1, 4):
        for task in tasks:
            if priority == task.priority:
                ready_q.put(task)

    for task in tasks:
        print(f"{count}) Duration: {task.duration}, Type: {task.task_type}, Name: {task.name}, State: {task.state}, Time On CPU: {task.exec_time}")
        count += 1

    while not ready_q.empty():
        x = ready_q.get()
        print(f"Name: {x.name}, Type: {x.task_type}, Duration: {x.duration}, Priority: {x.priority}")

    FCFS(ready_q)

if __name__ == "__main__":
    print("---- FCFS ---")
    main()

# import threading
# from queue import PriorityQueue
# from queue import Queue

# class Task:
#     def __init__(self, name, task_type, duration):
#         self.name = name
#         self.task_type = task_type
#         self.duration = duration
#         self.resources = []
#         self.state = 'Ready'
#         self.exec_time = 0
#         self.priority = 0

#         # Setting resources and priority based on task type
#         if task_type == 'X':
#             self.resources = ['R1', 'R2']
#             self.priority = 3
#         elif task_type == 'Y':
#             self.resources = ['R2', 'R3']
#             self.priority = 2
#         elif task_type == 'Z':
#             self.resources = ['R1', 'R3']
#             self.priority = 1

# mutex = threading.Lock()
# # ready_q = PriorityQueue()
# waiting_q = Queue()
# ready_q = Queue()
# timeUnit=1
# core=1
# kernal_threads = []
# def FCFS(ready_q):

#     # while ready_q:
#     while not ready_q.empty():
#         current_task = ready_q.get()
#         kernel_thread = threading.Thread(target=execute_task, args=(core,current_task))
#         kernal_threads.append(kernel_thread)
#         core += 1
#         if core == 4:
#             timeUnit += 1
#             kernel_thread.start()
    
    

# def execute_task(core, task):
#     # Placeholder function for task execution
#     print(f"Core {core}: Executing {task.name} with Duration: {task.duration} in time : {timeUnit}")


# def main():
#     # ---Taking input---
#     num_resources = list(map(int, input("Enter the data for resources and tasks:\n").split()))
#     num_tasks = int(input())
#     tasks = []
#     for _ in range(num_tasks):
#         task_data = input().split()
#         task_name, task_type, duration = (task_data[0]), (task_data[1]), int(task_data[2])
#         t=Task(task_name,task_type,duration)
#         tasks.append(t)

#     print(f"Resources: {num_resources}")
#     print(f"Number of tasks: {num_tasks}")
#     print("Task details:")
#     count = 1
#     for priority in range(1, 4):
#         for task in tasks:
#             if priority == task.priority:
#                 ready_q.put(task)

#     for task in tasks:
        
#         print(f"{count}) Duration: {task.duration}, Type: {task.task_type}, Name: {task.name}, State: {task.state}, Time On CPU: {task.exec_time}")
#         count += 1

#     while not ready_q.empty():
#         x = ready_q.get()
#         print(f"Name: {x.name}, Type: {x.task_type}, Duration: {x.duration}, Priority: {x.priority}")

#     FCFS(ready_q)
#     # kernal_threads = []
#     # for core in range(1, 5):
#     #     kernel_thread = threading.Thread(target= execute_task, args=(core,task))
#     #     kernal_threads.append(kernel_thread)
#     #     kernel_thread.start()



# if __name__ == "__main__":
#     print("---- FCFS ---")
#     main()