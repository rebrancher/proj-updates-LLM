from rich.console import Console
from rich.table import Table
from database import MasterTaskDB, TaskUpdateDB, TaskHighlightDB
from rich.prompt import Prompt
from DisplayManager import DisplayManager

class TaskManager:
    def __init__(self, db_name):
        self.master_db = MasterTaskDB(db_name)
        self.updates_db = TaskUpdateDB(db_name)
        self.highlights_db = TaskHighlightDB(db_name)
        self.display_manager = DisplayManager()
        self.console = Console()

    def select_from_list(self, items, item_index):
        while True:
            try:
                if 1 <= item_index <= len(items):
                    selected_item = items[item_index - 1]
                    return selected_item[0], selected_item[1]
                else:
                    print("\nInvalid selection, out of range.")
            except ValueError:
                print("\nInvalid input, please enter a number.")

#**********************************************************************************************************************
#****************************************** Master Task Code***********************************************************
#**********************************************************************************************************************       
 
    def master_task_menu(self):
        response = input("Enter the number of the Master Task, 'c' to cancel, or 'o' for options: ")
        #if response is a number, return the master task id
        #if response is 'c', return None
        #if response is 'o', return 'o'
        try:
            response = int(response)
            return response
        except ValueError:
            if response.lower() == 'c':
                return 'c'
            elif response.lower() == 'o':
                self.master_task_options()
            else:
                return None
            
    def master_task_options(self):
        while True:
            self.display_manager.clear_screen()
            options = {
                "1": "Create a new Master Task",
                "2": "Delete a Master Task",
                "3": "Exit options menu"
            }
            self.display_manager.display_master_tasks(self.master_db.get_master_tasks())
            self.display_manager.options_menu(options, title="Master Task Options")
            selected_option = Prompt.ask("Choose an option: ")
            if selected_option == '1':
                task_name = input("Enter the name of the new Master Task: ")
                self.create_master_task(task_name)
            elif selected_option == '2':
                self.delete_master_task()
                print("Deleting a Master Task...")
                input("Press enter to continue...")
            elif selected_option == '3':
                break
            else:
                continue

    def create_master_task(self, task_name):
        self.master_db.create_task(task_name)


            
#**********************************************************************************************************************
#****************************************** Updates Code **************************************************************
#**********************************************************************************************************************    

    def add_task_update(self, master_task_id):
        while True:
            self.display_manager.clear_screen()
            task_updates = self.updates_db.get_updates(master_task_id)
            self.display_manager.display_task_updates(task_updates)
            update = self.task_update_menu(master_task_id)
            if update == 'c':
                break            

        input("Exiting update entry mode. Press enter to continue...")
        return

    def task_update_menu(self, master_task_id):
        response = input("Enter update (300 characters max), 'c' to cancel, or 'o' for options: ")

        if response.lower() == 'c':
            return 'c'
        elif response.lower() == 'o':
            self.task_update_options(master_task_id)
        else:
            self.updates_db.add_update(master_task_id, response)

    def task_update_options(self, master_task_id):
        options = {
                "1": "Delete Update",
                "2": "Add a highlight",
                "3": "Get Update Details",
                "4": "Make a group",
                "5": "Exit update mode"
            }

        self.display_manager.options_menu(options, title="Update Menu")
        selected_option = Prompt.ask("Choose an option: ")

        if selected_option == '1':
            # You need to define delete_update() function``
            self.delete_task_update()
            print("Update successfully deleted\n")
        elif selected_option == '2':
            # You need to define add_highlight() function
            self.add_highlight()
            print("Adding a highlight...")
        elif selected_option == '3':
            # You need to define make_group() function
            self.update_details(master_task_id)
            print("Making a group...")

        elif selected_option == '4':
            # You need to define make_group() function
            self.group_updates(master_task_id)
        elif selected_option == '5':
            return
        else:
            Prompt.ask("Invalid option. Press enter to continue...")
            return
    
    def update_details(self, master_task_id):
        update_id = Prompt.ask("Enter the number of the update you want to view: ")
        update = self.updates_db.get_update(master_task_id, update_id)
        self.display_manager.display_update_details(master_task_id, update)
        input("Press enter to continue...")

    def group_updates(self, master_task_id):
        task_updates = self.updates_db.get_updates(master_task_id)
        self.display_manager.display_task_updates(task_updates)
        update_ids = input("Enter the ids of the updates you want to group separated by comma: ")
        update_ids = list(map(int, update_ids.split(',')))
        grouped_updates = []
        for update_id in update_ids:
            update = self.updates_db.get_update(master_task_id, update_id)
            grouped_updates.append(update)
        # Now we have a grouped_updates list which contains grouped updates
        # This list can be passed to other functions as needed
        print(grouped_updates)
        Prompt.ask("Press enter to continue...")
        return grouped_updates

#**********************************************************************************************************************
#****************************************** Highlights Code ***********************************************************
#**********************************************************************************************************************

    def add_highlight(self):

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
            "bright_black",
            "bright_red",
            "bright_green",
            "bright_yellow",
            "bright_blue",
            "bright_magenta",
            "bright_cyan",
            "bright_white",
            "dim"
        ]

        # Print all color names.
        print("\nPossible colors for highlighting are:")
        for color in colors:
            print(color)
        
        highlight_color = input("\nEnter the color for your highlight: ")
        
        if highlight_color not in colors:
            print("Invalid color. Please try again with a valid color.")
            return
        
        print(index, highlight_color)
        self.updates_db.add_highlight_to_update(index, highlight_color)

    # Function to fetch all highlights of a particular task.
    
    def delete_master_task(self):
        task_id = input("Enter the number of the Master Task to delete: ")
        check = input("Are you sure you want to delete this Master Task? (y/n): ")
        if check == 'y':
            self.master_db.delete_task(task_id)
        else:
            return

    def delete_task_update(self):
        update_id = Prompt.ask("Input #id of task you want to delete")
        prompt = Prompt.ask("Are you sure you want to delete this update? (y/n)")
        if prompt == 'y':
            self.updates_db.delete_update(update_id)
        else:
            Prompt.ask("Delete cancelled. Press enter to continue...")
            return
