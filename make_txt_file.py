with open("cli.py", "r") as file:
    cli = file.read()

with open("database.py", "r") as file:
    database = file.read()

with open("taskManager.py", "r") as file:
    taskmanager = file.read()

new_file = f"{cli}\n{database}\n{taskmanager}"

with open("chatgpt4file.txt", 'w') as file:
            file.write(new_file)