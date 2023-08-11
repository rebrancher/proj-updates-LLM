from rich.console import Console
from taskManager import TaskManager
from database import MasterTaskDB, TaskUpdateDB
from DisplayManager import DisplayManager

class CLI:
    #init, starts a task_manager instance and a console class?
    def __init__(self, task_manager, db_name):
        self.taskManager = task_manager
        self.masterDB = MasterTaskDB(db_name)
        self.updatesDB = TaskUpdateDB(db_name)
        self.displayManager = DisplayManager()
        self.console = Console()

    def run_cli(self):
        while True:
            self.displayManager.clearScreen()
            self.displayManager.displayTimestreams1()
            self.getAndProcessInputCli()

    def getAndProcessInputCli(self):
        timestreamID = input("Enter the ID of the Timestream, 'c' to cancel, or 'o' for options, 'y' for yesterdays updates: ")
        if timestreamID.isdigit():
            try:
                #this is more of an update menu type thing?
                self.taskManager.updatePromptAndProcess(timestreamID)
            except TypeError as e:
                print(e)
                input("\nInvalid input, please try again. Press enter to continue.")
                return
                
        elif timestreamID.lower() == 'c':
            print("Exiting...")
            exit()  
        elif timestreamID.lower() == 'o':
            self.taskManager.timestreamOptions()
        elif timestreamID.lower() == 'y':
            yesterdaysUpdates = self.updatesDB.getAllUpdatesSinceYesterdayMidnightJoinMasterDBName()
            self.displayManager.displayUpdatesWithMasterTaskIDAndName(yesterdaysUpdates)
            input("\nPress enter to continue.")
        
        else:
            input("\nInvalid input, please try again. Press enter to continue.")
            return

if __name__ == "__main__":
    db_name = 'task.db'
    task_manager = TaskManager(db_name)
    cli = CLI(task_manager, db_name)
    cli.run_cli()