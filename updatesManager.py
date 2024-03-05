from database import TaskUpdateDB, MasterTaskDB
from DisplayManager import DisplayManager
from GroupAndHighlightManager import GroupAndHighlightManager
from rich.prompt import Prompt

class UpdatesManager:
    def __init__(self):
        self.updatesDB = TaskUpdateDB('task.db')
        self.masterDB = MasterTaskDB('task.db')
        self.displayManager = DisplayManager()
        self.GHManager = GroupAndHighlightManager()

    def updatePromptAndProcess(self, timestreamID):
        responseIsNotCancel = True
        while responseIsNotCancel:
            self.viewUpdates(timestreamID)
            responseIsNotCancel = self.processUpdate(timestreamID)
            
    def processUpdate(self, timestreamID):

        update = input("\nEnter update, 'c' to cancel, 'o' for options, or 'd' for dim mode: \n\n")

        if update.lower() == 'c': return False
        elif update.lower() == 'o': self.updateOptions(timestreamID)
        elif update.lower() == 'd':
            print ("Entering Dim mode")
            updateID = input("\nEnter the ID of the update you want to DIM: ")
            update = self.updatesDB.getUpdate(updateID)
            print(update)
            self.updatesDB.add_highlight_to_update(updateID, "dim")
        else:
            self.updatesDB.add_update(timestreamID, update)
        return True
    
    def viewUpdates(self, timestreamID):
        self.displayManager.clearScreen()
        self.displayManager.displayUpdatesOrderedby(self.updatesDB.getUpdatesJoinMaster(timestreamID), "date")
        print(self.masterDB.getTimestreamName(timestreamID))


    def updateOptions(self, timestreamID):
        #how do you access the methods in OOP? 
        updateOptionsMenuChoices = {
                "1": ["Delete Update", "red", self.delete_task_update],
                "2": ["Add a highlight", "green", self.GHManager.add_highlight],
                "3": ["Get Update Details", "cyan", self.update_details],
                "4": ["Create a group", "blue", self.GHManager.create_group],
                "5": ["Add to group", "blue", self.GHManager.add_to_group],
                "6": ["View updates in group", "blue", self.GHManager.get_group_updates_with_text],
                "7": ["Exit update mode", "yellow", None]
            }

        self.displayManager.optionsMenu(updateOptionsMenuChoices)
        get_num = Prompt.ask("Choose an option: ")
        if get_num in updateOptionsMenuChoices:
            selected_option = updateOptionsMenuChoices[get_num][2]
        self.execute_task_update_option(selected_option, timestreamID)

    def execute_task_update_option(self, selected_option, master_task_id):
        if selected_option:
            selected_option(master_task_id)
        else:
            return
    
    def update_details(self, master_task_id):
        update_id = Prompt.ask("Enter the number of the update you want to view: ")
        update = self.updates_db.getUpdateAndMaster(master_task_id, update_id)
        self.displayManager.display_update_details(master_task_id, update)
        input("Press enter to continue...")

    def delete_task_update(self):
        update_id = Prompt.ask("Input #id of task you want to delete")
        prompt = Prompt.ask("Are you sure you want to delete this update? (y/n)")
        if prompt == 'y':
            self.updates_db.delete_update(update_id)
        else:
            Prompt.ask("Delete cancelled. Press enter to continue...")
            return
    