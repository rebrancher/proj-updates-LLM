from rich.console import Console
from taskManager import TaskManager

class CLI:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.console = Console()

    def run_cli(self):
        while True:
            self.console.print("\nWelcome to the task manager, select from the menu below:\n", style="bold blue")
            self.console.print("1. Create Master Task")
            self.console.print("2. List Master Tasks")
            self.console.print("3. Add Task Update")
            self.console.print("4. View Task Updates")
            self.console.print("5. Add Highlight to a Task")
            self.console.print("6. View Task Highlights")
            self.console.print("7. Exit\n", style="bold red")
            choice = input("Enter your choice: ")

            if choice == '1':
                task_name = input("\nEnter the name of the new Master Task, press c to cancel: ")
                if task_name == "c":
                    continue
                self.task_manager.create_master_task(task_name)

            elif choice == '2':
                self.task_manager.list_master_tasks()

            elif choice == '3':
                master_task_id, _ = self.task_manager.select_master_task()
                if master_task_id:
                    self.task_manager.add_task_update(master_task_id)

            elif choice == '4':
                master_task_id, task_name = self.task_manager.select_master_task()
                if master_task_id:
                    self.task_manager.list_updates(master_task_id)

            elif choice == '5':
                self.task_manager.add_highlight()

            elif choice == '6':
                master_task_id, task_name = self.task_manager.select_master_task()
                if master_task_id:
                    self.task_manager.get_highlights(master_task_id)

            elif choice == '7':
                print("\nExiting...\n")
                break

            else:
                print("\nInvalid choice. Please enter a number between 1 and 7.\n")


if __name__ == "__main__":
    task_manager = TaskManager('task.db')
    cli = CLI(task_manager)
    cli.run_cli()