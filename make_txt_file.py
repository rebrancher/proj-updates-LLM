with open("cli.py", "r") as file:
    cli = file.read()

with open("database.py", "r") as file:
     database = file.read()

with open("taskManager.py", "r") as file:
    taskmanager = file.read()

with open("DisplayManager.py", "r") as file:
    displaymanager = file.read()

new_file = f"cli.py:\n{cli}\ntaskmanager.py\n{taskmanager}displaymanager.py\n{displaymanager}\ndatabase.py\n"
file1 = f"cli.py:\n{cli}\ntaskmanager.py\n{taskmanager}"
file2 = f"\ndisplaymanager.py\n{displaymanager}\ndatabase.py\n{database}"

with open("chatgpt4file.txt", 'w') as file:
            file.write(new_file)
with open("chatgpt4file1.txt", 'w') as file:
            file.write(file1)
with open("chatgpt4file2.txt", 'w') as file:
            file.write(file2)