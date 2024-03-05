from database import TaskUpdateDB, MasterTaskDB, GroupsDB, GroupsLinkDB
from DisplayManager import DisplayManager


class GroupAndHighlightManager:
    def __init__(self):
        self.updatesDB = TaskUpdateDB('task.db')
        self.masterDB = MasterTaskDB('task.db')
        self.groupsDB = GroupsDB('task.db')
        self.groupsLinkDB = GroupsLinkDB('task.db')
        self.displayManager = DisplayManager()




    def add_highlight(self, master_task_id):
        index = input("Enter the number of the update you want to highlight: ")
        colors = [
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
            "dim"
        ]

        print("\nPossible colors for highlighting are:")
        for color in colors:
            print(color)
        
        highlight_color = input("\nEnter the color for your highlight: ")
        
        if highlight_color not in colors:
            print("Invalid color. Please try again with a valid color.")
            return
        
        print(index, highlight_color)
        self.updates_db.add_highlight_to_update(index, highlight_color)


    def create_group(self, master_task_id):
        group_name = input("Enter the name of the new group: ")
        self.groupsDB.create_group(master_task_id, group_name)
    
    def get_group_id(self, master_task_id):
        groups = self.groupsDB.get_groups(master_task_id)
        self.displayManager.display_groups(groups)
        group_id = input("Enter the number of the group you want to select: ")
        return group_id
    
    def add_to_group(self, master_task_id):
        group_id = self.get_group_id(master_task_id)
        update_id = input("Enter the number of the update you want to add to the group: ")
        self.groupsLink_db.create_link(update_id, group_id)

    def get_group_updates_with_text(self, master_task_id):
        group_id = self.get_group_id(master_task_id)
        updates = self.groupsLink_db.get_updates_from_links(group_id)
        print(updates)
        
        self.displayManager.display_task_updates(updates)
        input("Press enter to continue...")