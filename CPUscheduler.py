# ---Taking input---
num_resources = list(map(int, input("Enter the data for resources and tasks:\n").split()))
num_tasks = int(input())
tasks = []
for _ in range(num_tasks):
    task_data = input().split()
    duration, task_type, task_name = (task_data[0]), (task_data[1]), int(task_data[2])
    tasks.append((duration, task_type, task_name))

print(f"Resources: {num_resources}")
print(f"Number of tasks: {num_tasks}")
print("Task details:")
count = 1
for task in tasks:
    print(f"{count}) Duration: {task[0]}, Type: {task[1]}, Name: {task[2]}")
    count += 1

for task in tasks:
    print(f"{count}) Duration: {task[0]}, Type: {task[1]}, Name: {task[2]}")
    count += 1
>>>>>>> bff5d5fca9a528d0c6903145a8134d385671f8ff


