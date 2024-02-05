import threading
from queue import Queue
import time

class Task:
    def __init__(self, name, task_type, duration):
        self.name = name
        self.task_type = task_type
        self.duration = duration
        self.resources = []
        self.state = 'Ready' # Can either be Ready, Waiting or Running 
        self.exec_time = 0
        self.priority = 0
        self.doneOrRunning = False

        if task_type == 'X':
            self.resources = ['R1', 'R2']
            self.priority = 3
        elif task_type == 'Y':
            self.resources = ['R2', 'R3']
            self.priority = 2
        elif task_type == 'Z':
            self.resources = ['R1', 'R3']
            self.priority = 1

    def getRemainingTime():
        return self.duration - self.exec_time 

    def getTask(task_name):
        if self.name == task_name: return self
        return None

mappingResources = {'R1': 0, 'R2': 1, 'R3': 2}
mutex = threading.Lock()
waiting_q = PriorityQueue()  # Priority queue for SJF scheduling
ready_q = PriorityQueue()  # Ready queue for tasks ready to be executed with their priority being duration
timeUnit = 1
core = 1
tasks = []
cores_in_use = 0
print_mutex = threading.Lock()
eventForPrint = threading.Event()
# coreTask is Idle or is equal to the name of the task it's doing, and cores are not assigned to a task at first
coreTask = ['Idle'] * 4
coreAssigned = [False] * 4
# To determine whether the threads should stop their job
exit_flag = False 

def checkingForAvilableResources(tr1, tr2):
    r1 = mappingResources.get(tr1)
    r2 = mappingResources.get(tr2)
    return (num_resources[r1] > 0 and num_resources[r2] > 0)

def assignResources(tr1, tr2):
    r1 = mappingResources.get(tr1)
    r2 = mappingResources.get(tr2)
    num_resources[r1] -= 1
    num_resources[r2] -= 1

def waitingtoReady():
    backToWaiting = list()
    while not waiting_q.empty():
        t_duration, t_name = waiting_q.get()[1]
        task = Task.getTask(t_name)
        tr1, tr2 = task.resources[0], task.resources[1]
        resourceAvilable = checkingForAvilableResources(tr1, tr2)
        if resourceAvilable:
            # Put the tast from waiting queue to ready queue
            ready_q.put((t_duration, t_name))
        else:
            # Put the tast back in the waiting queue
            backToWaiting.append((t_duration, t_name))
    for t in backToWaiting:
        waiting_q.put(t)
    backToWaiting.clear()
    
def execute_task(core):
    task = None
    gotResource = False
    while not exit_flag:
        coreAssigned[core] = False
        mutex.acquire()
        # If any process is in the waiting queue and is ready, put it in the ready queue
        waitingtoReady()
        # Getting a task from the ready queue if it isn't empty
        if ready_q:
            task_name = ready_q.get()
            task = Task.getTask(task_name)
            task.state = 'Running'
            # Checking to see if the resources for this task are available
            tr1, tr2 = task.resources[0], task.resources[1]
            resourceAvilable = checkingForAvilableResources(tr1, tr2)
            if resourceAvilable:
                assignResources(tr1, tr2)
                coreTask[core] = task.name
                gotResource = True
            else:
                # If the resources are not available the process should go to the waiting queue
                waiting_q.put((task.duration, task.name))
                task.state = 'Waiting'
            task.exec_time += 1

        # If the task is done, release it's resources
        if task.remaining_time < 0 and gotResource:
            tr1, tr2 = task.resources[0], task.resources[1]
            r1 = mappingResources.get(tr1)
            r2 = mappingResources.get(tr2)
            num_resources[r1] += 1
            num_resources[r2] += 1
            gotResource = False



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

        with print_mutex:
            print_execution_result(core, task)

def print_results():
    while not exit_flag:
        # Waiting for the cores to be assigned a task so that we can print the results
        eventForPrint.wait()
        # Printing for each core
        for core in range(4):
            task = coreTask[i]
            print(f'Core: {core}, Time: {timeUnit}, Task: {task}')
        timeUnit += 1
        eventForPrint.clear()
    
def main():
    # Taking input
    # Number of resources R1, R2 and R3
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
        ready_q.put((task.duration, task.name)) # Putting all the tasks in the ready queue and sort based on duration
        kernel_threads.append(threading.Thread(target=execute_task, args=(count,))) # Creating kernel threads
        print(f"{count}) Duration: {task.duration}, Type: {task.task_type}, Name: {task.name}, State: {task.state}, Time On CPU: {task.exec_time}")
        count += 1

    # Creating the printing thread
    print_thread = threading.Thread(target = print_results)
    for thrd in kernel_threads:
        thrd.start()
    print_thread.start()
    # Wait for the printing thread to finish
    print_thread.join()

if __name__ == "__main__":
    print("--- SJF ---")
    main()
