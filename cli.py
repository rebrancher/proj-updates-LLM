import os

class CLI:
    def __init__(self, task_manager):
        self.task_manager = task_manager

    def run_cli(self):
        while True:
            print("\nWelcome to the task manager, select from the menu below:\n")
            print("1. Create Master Task")
            print("2. List Master Tasks")
            print("3. Add Task Update")
            print("4. View Task Updates")
            print("5. Exit\n")
            choice = input("Enter your choice: ")

            if choice == '1':
                task_name = input("\nEnter the name of the new Master Task: ")
                self.task_manager.create_master_task(task_name)

            elif choice == '2':
                self.task_manager.list_master_tasks()

            elif choice == '3':
                task_id, _ = self.task_manager.select_master_task()
                if task_id:
                    update_text = input("\nEnter your task update (max 300 chars): ")
                    self.task_manager.add_task_update(task_id, update_text)

            elif choice == '4':
                task_id, task_name = self.task_manager.select_master_task()
                if task_id:
                    self.task_manager.get_task_updates(task_id, task_name)

            elif choice == '5':
                print("\nExiting...\n")
                break

            else:
                print("\nInvalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    from taskManager import TaskManager
    task_manager = TaskManager('task.db')
    cli = CLI(task_manager)
    cli.run_cli()
