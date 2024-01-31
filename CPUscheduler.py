# Read the number of resources for R1, R2, and R3
num_resources = list(map(int, input("Enter the number of resources for R1, R2, and R3: ").split()))

# Read the number of tasks
num_tasks = int(input("Enter the number of tasks: "))

# Read task details
tasks = []
for _ in range(num_tasks):
    task_data = input("Enter task details (Duration_Task, Type_Task, Name_Task): ").split()
    duration, task_type, task_name = map(int, task_data)
    tasks.append((duration, task_type, task_name))

# Print the input data
print(f"Number of resources: {num_resources}")
print(f"Number of tasks: {num_tasks}")
print("Task details:")
for task in tasks:
    print(f"Duration: {task[0]}, Type: {task[1]}, Name: {task[2]}")
