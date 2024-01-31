# Read the number of resources for R1, R2, and R3
num_resources = input().split(' ')# 'Enter the number of resources for R1, R2, and R3: '
num_tasks = int(input()) # "Enter the number of tasks: "
tasks = []
for _ in range(num_tasks):
    task_data = input().split() # "Enter task details (Duration_Task, Type_Task, Name_Task): "
    duration, task_type, task_name = map(int, task_data)
    tasks.append((duration, task_type, task_name))

print(f"Number of resources: {num_resources}")
print(f"Number of tasks: {num_tasks}")
print("Task details:")
for task in tasks:
    print(f"Duration: {task[0]}, Type: {task[1]}, Name: {task[2]}")
