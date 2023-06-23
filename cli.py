from rich.console import Console
from taskManager import TaskManager
from database import MasterTaskDB
from DisplayManager import DisplayManager

class CLI:
    #init, starts a task_manager instance and a console class?
    def __init__(self, task_manager, db_name):
        self.task_manager = task_manager
        self.master_db = MasterTaskDB(db_name)
        self.display_manager = DisplayManager()
        self.console = Console()

    def run_cli(self):

        while True:
            self.display_manager.clear_screen()
            master_tasks = self.master_db.get_master_tasks()
            self.display_manager.display_master_tasks(master_tasks)
            print("\n")
            master_task_id, _ = self.task_manager.select_from_list(master_tasks)

            if master_task_id:
                self.task_manager.add_task_update(master_task_id)
            else:
                break


if __name__ == "__main__":
    db_name = 'task.db'
    task_manager = TaskManager(db_name)
    cli = CLI(task_manager, db_name)
    cli.run_cli()