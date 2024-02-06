import threading
from queue import Queue
from queue import PriorityQueue

class Task:
    
    global tasks
    def __init__(self, name, task_type, duration):
        self.name = name
        self.task_type = task_type
        self.resources = list()
        self.state = 'Ready' # Can either be Ready, Waiting or Running 
        self.exec_time = 0
        self.priority = 0
        self.priorityOverTime = 0
        self.duration = duration
        self.doneOrRunning = False
        self.waiting_time = 0  # to track of waiting time for starvation (aging)
        if task_type == 'X':
            self.resources = ['R1', 'R2']
            self.priority = 3
        elif task_type == 'Y':
            self.resources = ['R2', 'R3']
            self.priority = 2
        elif task_type == 'Z':
            self.resources = ['R1', 'R3']
            self.priority = 1

    def getPriorityForSJF(self):
        return self.duration - self.priorityOverTime

    def getRemainingTime(self):
        return self.duration - self.exec_time 

    def getTask(task_name):
        for task in tasks:
            if task.name == task_name:
                return task
        return None

def checkingForAvailableResources(tr1, tr2):
    global num_resources, mappingResources
    r1 = mappingResources.get(tr1)
    r2 = mappingResources.get(tr2)
    return (num_resources[r1] > 0 and num_resources[r2] > 0)

def assignResources(tr1, tr2):
    global num_resources, mappingResources
    r1 = mappingResources.get(tr1)
    r2 = mappingResources.get(tr2)
    num_resources[r1] -= 1
    num_resources[r2] -= 1

def waitingtoReady():
    global waiting_q, ready_q
    backToWaiting = list()
    while not waiting_q.empty():
        t_p, t_name = waiting_q.get()
        task = Task.getTask(t_name)
        tr1, tr2 = task.resources[0], task.resources[1]
        resourceAvilable = checkingForAvailableResources(tr1, tr2)
        if resourceAvilable:
            # Put the tast from waiting queue to ready queue
            ready_q.put((t_p, t_name))
            task.state = 'Ready'
        else:
            # Put the tast back in the waiting queue
            backToWaiting.append((task.getPriorityForSJF(), t_name))
    for t in backToWaiting:
        waiting_q.put(t)
    backToWaiting.clear()
    
def execute_task(core):
    global coreDone, mutex, ready_q, coreTask, waiting_q, tasks
    gotResource = False
    coreDone[core] = False
    while not exit_event.is_set():
        mutex.acquire()
        # If any process is in the waiting queue and is ready, put it in the ready queue
        waitingtoReady()
        # Getting a task from the ready queue if it isn't empty
        if not ready_q.empty():
            task_name = ready_q.get()[1]
            # Finding which task it was
            task = Task.getTask(task_name)
            task.state = 'Running'
            # Checking to see if the resources for this task are available
            tr1, tr2 = task.resources[0], task.resources[1]
            resourceAvilable = checkingForAvailableResources(tr1, tr2)
            if resourceAvilable:
                assignResources(tr1, tr2)
                coreTask[core] = task.name
                gotResource = True
            else:
                # If the resources are not available the process should go to the waiting queue
                waiting_q.put((task.getPriorityForSJF(), task.name))
                task.state = 'Waiting'
                task.waiting_time += 1
                if task.waiting_time >= 3: # If the task waited more than 3 rounds, its priority goes up
                    task.priorityOverTime += 1
            task.exec_time += 1

            # If the task is done, release its resources
            if task.getRemainingTime() <= 0 and gotResource:
                tr1, tr2 = task.resources[0], task.resources[1]
                r1 = mappingResources.get(tr1)
                r2 = mappingResources.get(tr2)
                num_resources[r1] += 1
                num_resources[r2] += 1
                gotResource = False

        else:
            # When there is nothing in the ready queue
            coreDone[core] = True
            countDone = 0
            for d in coreDone:
                if d: countDone += 1
            if countDone == 4:
                eventForPrint.set()

        mutex.release()

def print_results():
    global countDone, eventForPrint, coreTask, countDone, timeUnit
    while not exit_event.is_set() and timeUnit < 20:
        # Waiting for the cores to be assigned a task so that we can print the results
        eventForPrint.wait()
        eventForPrint.clear()
        # Printing for each core
        for core in range(4):
            task = coreTask[core]
            print(f'Core: {core+1}, Time: {timeUnit}, Task: {task}')
        timeUnit += 1
        countDone = 0
        eventForPrint.clear()

mappingResources = {'R1': 0, 'R2': 1, 'R3': 2}
mutex = threading.Lock()
waiting_q = PriorityQueue()  # Priority queue for SJF scheduling
ready_q = PriorityQueue() # Ready queue for tasks ready to be executed with their priority being duration
timeUnit = 1
tasks = []
print_mutex = threading.Lock()
eventForPrint = threading.Event()
# coreTask is Idle or is equal to the name of the task it's doing, and cores are not assigned to a task at first
coreTask = ['Idle'] * 4
coreDone = [False] * 4
# To determine whether the threads should stop their job
exit_flag = False 
countDone = 0
num_resources = list()
exit_event = threading.Event()

def main():
    global tasks, num_resources
    # Number of resources R1, R2 and R3
    num_resources = list(map(int, input("Enter the data for resources and tasks:\n").split()))
    num_tasks = int(input())
    for _ in range(num_tasks):
        task_data = input().split()
        task_name, task_type, duration = task_data[0], task_data[1], int(task_data[2])
        t = Task(task_name, task_type, duration)
        tasks.append(t)

    print(f"Resources: {num_resources}")
    print(f"Number of tasks: {num_tasks}")
    print("Task details:")

    kernel_threads = list()
    for i in range(num_tasks):
        gp = int(tasks[i].getPriorityForSJF())
        ready_q.put((gp, tasks[i].name)) # Putting all the tasks in the ready queue and sort based on duration
        kernel_threads.append(threading.Thread(target=execute_task, args=(i % 4,))) # Creating kernel threads
        print(f"{i+1}) Duration: {tasks[i].duration}, Type: {tasks[i].task_type}, Name: {tasks[i].name}, State: {tasks[i].state}, Time On CPU: {tasks[i].exec_time}")

    # Creating the printing thread
    print_thread = threading.Thread(target = print_results)
    for thrd in kernel_threads:
        thrd.start()
    print_thread.start()
    print_thread.join()

    # Signaling threads to exit
    exit_event.set()

    for thrd in kernel_threads:
        thrd.join()

if __name__ == "__main__":
    print("--- SJF ---")
    main()
