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
            self.console.print("\nWelcome to the task manager, select from the menu below:\n", style="bold blue")
            self.console.print("1. Create Master Task")
            self.console.print("2. List Master Tasks\n")
            self.console.print("3. Create Task Update")
            self.console.print("4. View Task Updates\n")
            self.console.print("5. Add Highlight to a Task")
            self.console.print("6. View Task Highlights\n")
            self.console.print("8. Delete Master Task")
            self.console.print("9. Delete Task Update\n")
            self.console.print("10. Exit\n", style="bold red")
            choice = input("Select option by inputting corresponding #: ")

            #Create Master Task
            if choice == '1':
                self.task_manager.clear_screen()
                print("Current Master Tasks:\n")
                self.task_manager.list_master_tasks()
                task_name = input("\nEnter the name of the new Master Task, press c to cancel: ")
                #cancelling
                if task_name == "c":
                    continue

                """
                    This goes to the task_manager which then points to the
                    DB function, is this the best way to go about this?
                """
                self.task_manager.create_master_task(task_name)

            #List Master Tasks - Pretty straightforward print
            elif choice == '2':
                self.task_manager.clear_screen()
                self.task_manager.list_master_tasks()
                input("Press any key to continue...")
                self.task_manager.clear_screen()

            #Add Task Update
            elif choice == '3':

                self.task_manager.clear_screen()
                master_task_id, _ = self.task_manager.select_master_task()
                if master_task_id:
                    self.task_manager.list_updates(master_task_id)
                    self.task_manager.add_task_update(master_task_id)

            #View task updates
            elif choice == '4':
                master_task_id, task_name = self.task_manager.select_master_task()
                if master_task_id:
                    self.task_manager.list_updates(master_task_id)
                input("Press any key to continue...")

            #Add highlight to a task
            elif choice == '5':
                self.task_manager.add_highlight()

            #View task highlights
            elif choice == '6':
                master_task_id, task_name = self.task_manager.select_master_task()
                if master_task_id:
                    self.task_manager.get_highlights(master_task_id)

            #Delete Master Task
            elif choice == '8':
                task_id, _ = self.task_manager.select_master_task()
                confirmation = input("Are you sure you want to delete this Master Task? y/n: ")
                if confirmation.lower() == 'y':
                    self.task_manager.delete_master_task(task_id)
                else:
                    continue
            #Delete Task Update
            elif choice == '9':
                master_task_id, _ = self.task_manager.select_master_task()
                if master_task_id:
                    update_id, _ = self.task_manager.select_update(master_task_id)
                    confirmation = input("Are you sure you want to delete this Task Update? y/n: ")
                    if confirmation.lower() == 'y':
                        self.task_manager.delete_task_update(update_id)
                    else:
                        continue
            #exit
            elif choice == '10':
                print("\nExiting...\n")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 10.\n")


if __name__ == "__main__":
    task_manager = TaskManager('task.db')
    cli = CLI(task_manager)
    cli.run_cli()