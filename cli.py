from rich.console import Console
from taskManager import TaskManager

class CLI:
    #init, starts a task_manager instance and a console class?
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.console = Console()

    def run_cli(self):
        #Main menu, should see if its worth creating a menu type object taht can just
        #take in inputs 

        while True:
            self.task_manager.clear_screen()

            

            self.console.print("Task Manager\n", style="bold blue")
            self.console.print("Tasks added yesterday: ", style="bold green")
            self.console.print("Meta commands:\n ", style="bold yellow")
            moveOn = input("Press h to continue, press c to exit: ")
            if moveOn == 'h':
                master_task_id, _ = self.task_manager.select_master_task()
                if master_task_id:
                    self.task_manager.list_updates(master_task_id)
                    option = input("Select from menu: \n 1) Add update 2) Add highlight \n 3) Exit \n")
                    if option == '1':
                        self.task_manager.add_task_update(master_task_id)
                        self.task_manager.add_task_update(master_task_id)
                    elif option == '2':
                        self.task_manager.add_highlight()
                    elif option == '3':
                        continue
                    else:
                        print("Invalid input, please try again")

            elif moveOn == 'c':
                print("Exiting...")
                break

            else:
                print("Invalid input, please try again")


if __name__ == "__main__":
    task_manager = TaskManager('task.db')
    cli = CLI(task_manager)
    cli.run_cli()