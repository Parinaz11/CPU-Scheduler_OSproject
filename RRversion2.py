import threading
from queue import PriorityQueue

class Task:
    def __init__(self, name, task_type, duration):
        self.name = name
        self.task_type = task_type
        self.duration = duration
        self.resources = []
        self.state = 'Ready'  # Can either be Ready, Waiting, or Running
        self.exec_time = 0

        if task_type == 'X':
            self.resources = ['R1', 'R2']
        elif task_type == 'Y':
            self.resources = ['R2', 'R3']
        elif task_type == 'Z':
            self.resources = ['R1', 'R3']

    def getRemainingTime(self):
        return self.duration - self.exec_time

    def getTask(task_name, tasks):
        for task in tasks:
            if task.name == task_name:
                return task
        return None

def checkingForAvailableResources(tr1, tr2, mappingResources):
    r1 = mappingResources.get(tr1, -1)
    r2 = mappingResources.get(tr2, -1)

    return 0 < r1 and 0 < r2

def assignResources(tr1, tr2, mappingResources):
    r1 = mappingResources[tr1]
    r2 = mappingResources[tr2]
    mappingResources[tr1] -= 1
    mappingResources[tr2] -= 1

def waitingtoReady(mappingResources, waiting_q, ready_q):
    backToWaiting = list()
    while not waiting_q.empty():
        task = waiting_q.get()

        if task is not None:
            tr1, tr2 = task.resources[0], task.resources[1]
            resourceAvailable = checkingForAvailableResources(tr1, tr2, mappingResources)

            if resourceAvailable:
                # Put the task from waiting queue to ready queue
                ready_q.put(task)
                task.state = 'Ready'
            else:
                # Put the task back in the waiting queue
                backToWaiting.append(task)
        else:
            # Handle the case when the task is None (not found)
            print(f"Task {task.name} not found.")

    for t in backToWaiting:
        waiting_q.put(t)
    backToWaiting.clear()

def execute_task(core, quantum, mutex):
    global exit_flag, ready_q, coreTask, waiting_q, tasks, mappingResources, eventForPrint
    coreDone = [False] * 4
    current_quantum = quantum
    while not exit_flag:
        mutex.acquire()
        # If any process is in the waiting queue and is ready, put it in the ready queue
        waitingtoReady(mappingResources, waiting_q, ready_q)
        # Getting a task from the ready queue if it isn't empty
        if not ready_q.empty():
            task = ready_q.get()
            # Finding which task it was
            task.state = 'Running'
            # Checking to see if the resources for this task are available
            tr1, tr2 = task.resources[0], task.resources[1]
            resourceAvailable = checkingForAvailableResources(tr1, tr2, mappingResources)
            if resourceAvailable:
                assignResources(tr1, tr2, mappingResources)
                coreTask[core] = task.name
                current_quantum = quantum  # Reset the quantum for the new task
            else:
                # If the resources are not available, the process should go to the waiting queue
                waiting_q.put(task)
                task.state = 'Waiting'
            task.exec_time += 1

            # If the task is done, release its resources
            if task.getRemainingTime() == 0:
                tr1, tr2 = task.resources[0], task.resources[1]
                r1 = mappingResources[tr1]
                r2 = mappingResources[tr2]
                mappingResources[tr1] += 1
                mappingResources[tr2] += 1

            # Check if the time quantum is reached
            current_quantum -= 1
            if current_quantum == 0:
                # Put the task back in the ready queue
                task.duration = task.duration - quantum
                ready_q.put(task)
                task.state = 'Ready'
                current_quantum = quantum

        else:
            # When there is nothing in the ready queue
            coreDone[core] = True
            countDone = sum(1 for d in coreDone if d)
            if countDone == 4:
                eventForPrint.set()

        mutex.release()

def print_results(mutex):
    global exit_flag, coreTask, timeUnit, eventForPrint
    countDone = 0
    while not exit_flag and timeUnit < durationSum:
        # Waiting for the cores to be assigned a task so that we can print the results
        eventForPrint.wait()
        # Checking for exiting the program
        count = sum(1 for c in coreTask if c == 'Idle')
        if count == 4:
            exit_flag = True
        # Printing for each core
        for core, task in enumerate(coreTask):
            mutex.acquire()
            print(f'Core: {core + 1}, Time: {timeUnit}, Task: {task}')
            mutex.release()
            if core + 1 < len(coreTask) and timeUnit > Task.getTask(coreTask[core + 1], tasks).duration:
                coreTask[core + 1] = 'Idle'
        timeUnit += 1
        countDone = 0
        eventForPrint.clear()

mappingResources = {'R1': 0, 'R2': 1, 'R3': 2}
mutex = threading.Lock()
waiting_q = PriorityQueue()
ready_q = PriorityQueue()
timeUnit = 1
tasks = []
eventForPrint = threading.Event()
coreTask = ['Idle'] * 4
exit_flag = False
durationSum = 0
num_resources = []

def main():
    global exit_flag, timeUnit, durationSum
    # Taking input
    # Number of resources R1, R2, and R3
    num_resources = list(map(int, input("Enter the data for resources and tasks:\n").split()))
    mappingResources['R1'] = num_resources[0]
    mappingResources['R2'] = num_resources[1]
    mappingResources['R3'] = num_resources[2]
    num_tasks = int(input())
    for _ in range(num_tasks):
        task_data = input().split()
        task_name, task_type, duration = task_data[0], task_data[1], int(task_data[2])
        t = Task(task_name, task_type, duration)
        tasks.append(t)

    for t in tasks:
        durationSum += t.duration

    print(f"Resources: {num_resources}")
    print(f"Number of tasks: {num_tasks}")
    print("Task details:")

    kernel_threads = []
    for count, task in enumerate(tasks):
        ready_q.put((task.duration, task.name))  # Putting all the tasks in the ready queue and sort based on duration
        kernel_threads.append(threading.Thread(target=execute_task, args=(count, 3, mutex)))  # Creating kernel threads
        print(f"{count}) Duration: {task.duration}, Type: {task.task_type}, Name: {task.name}, State: {task.state}, Time On CPU: {task.exec_time}")

    # Creating the printing thread
    print_thread = threading.Thread(target=print_results, args=(mutex,))
    for thrd in kernel_threads:
        thrd.start()
    print_thread.start()
    # Wait for the printing thread to finish
    print_thread.join()

if __name__ == "__main__":
    print("--- Round Robin (Quantum=3) ---")
    main()
