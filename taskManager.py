from rich.console import Console
from rich.table import Table
from database import MasterTaskDB, TaskUpdateDB
from DisplayManager import DisplayManager
from updatesManager import UpdatesManager

#just put on your backpack and go

class TaskManager:
    def __init__(self, db_name):
        #should there be a DB class that all of these inherit from?
        self.master_db = MasterTaskDB(db_name)
        self.updates_db = TaskUpdateDB(db_name)
        self.displayManager = DisplayManager()
        self.console = Console()
        self.updatesManager = UpdatesManager()
 
    def timestreamOptions(self):
        options = {
            "1": ["Create a new Master Task", "green"],
            "2": ["Delete a Master Task", "red"],
            "3": ["Exit options menu", "blue"]
        }
        self.displayManager.optionsMenu(options)
        #this select options needs some rework
        #if input in options then do something
        selectedOption = Prompt.ask("Choose an option: ")
        if selectedOption == '1':
            task_name = input("Enter the name of the new Master Task: ")
            self.master_db.create_task(task_name)
        elif selectedOption == '2':
            self.delete_master_task()
            print("Deleted a Master Task")
        elif selectedOption == '3':
            return
        else:
            print("Invalid input, please try again. Going back to main menu")
            return
    
    def delete_master_task(self):
        task_id = input("Enter the number of the Master Task to delete: ")
        check = input("Are you sure you want to delete this Master Task? (y/n): ")
        if check == 'y':
            self.master_db.delete_task(task_id)
        else:
            return

    
    

