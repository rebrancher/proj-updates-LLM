from rich.console import Console
from taskManager import TaskManager
from database import MasterTaskDB, TaskUpdateDB, TaskHighlightDB
from DisplayManager import DisplayManager

class CLI:
    #init, starts a task_manager instance and a console class?
    def __init__(self, task_manager, db_name):
        self.task_manager = task_manager
        self.master_db = MasterTaskDB(db_name)
        self.updates_db = TaskUpdateDB(db_name)
        self.highlights_db = TaskHighlightDB(db_name)
        self.display_manager = DisplayManager()
        self.console = Console()

    def run_cli(self):
        #Main menu, should see if its worth creating a menu type object taht can just
        #take in inputs


        while True:
            self.display_manager.clear_screen()
            master_tasks = self.master_db.get_master_tasks()
            self.display_manager.display_master_tasks(master_tasks)
            print("\n")
            master_task_id, _ = self.task_manager.select_from_list(master_tasks)

            self.display_manager.clear_screen()
            task_updates = self.updates_db.get_updates(master_task_id)
            self.display_manager.display_task_updates(task_updates)

            #self.console.print("Tasks added yesterday: ", style="bold green")
            #self.console.print("Meta commands:\n ", style="bold yellow")

            if master_task_id:
                self.display_manager.clear_screen()
                self.display_manager.display_task_updates(task_updates)
                self.task_manager.add_task_update(master_task_id)
                # self.display_manager.display_updates_menu()
                # option = input("Select from the menu: ")
                # if option == '1': #Add Task Update
                #     self.task_manager.add_task_update(master_task_id)
                # elif option == '2': #Add Highlight
                #     self.task_manager.add_highlight(master_task_id)
                # elif option == '3': #Main Menu
                #     continue
                # else:
                #     print("Invalid input, please try again")

            else:
                break


if __name__ == "__main__":
    db_name = 'task.db'
    task_manager = TaskManager(db_name)
    cli = CLI(task_manager, db_name)
    cli.run_cli()