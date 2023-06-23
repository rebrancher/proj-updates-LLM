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

    def select_from_list(self, items):
        while True:
            try:
                item_index = input("Please enter the number of the item you want to select, press c to cancel: ")
                if item_index.lower() == 'c':
                    return None, None
                item_index = int(item_index)
                if 1 <= item_index <= len(items):
                    selected_item = items[item_index - 1]
                    return selected_item[0], selected_item[1]
                else:
                    print("\nInvalid selection.")
            except ValueError:
                print("\nInvalid input, please enter a number.")


# Master Task Code

    def create_master_task(self, task_name):
        self.master_db.create_task(task_name)

# Updates Code
    def add_task_update(self, master_task_id):
        while True:
            self.display_manager.clear_screen()
            task_updates = self.updates_db.get_updates(master_task_id)
            self.display_manager.display_task_updates(task_updates)
            
            # Define menu options
            options = {
                "1": "Update text",
                "2": "Add a highlight",
                "3": "Make a group",
                "4": "Exit update mode"
            }

            self.display_manager.options_menu(options, title="Update Menu")


            # Ask for user choice
            selected_option = Prompt.ask("Choose an option: ")

            if selected_option == '1':
                update_text = input("Enter your task update (max 300 chars), press 'c' to cancel: ")
                print("")
                if update_text.lower() == 'c':
                    break
                self.updates_db.add_update(master_task_id, update_text, highlight=None)
                print("Update successfully added\n")
            elif selected_option == '2':
                # You need to define add_highlight() function
                print("Adding a highlight...")
            elif selected_option == '3':
                # You need to define make_group() function
                print("Making a group...")
            elif selected_option == '4':
                task = self.select_from_list(task_updates)


        print("Exited update entry mode.")


    def menu_add_update(self, master_task_id):
        ##this part you have to figure out how to get menus out of the function codes
        self.list_updates(master_task_id)
        print("Options:")
        print("1. Add new update")
        print("2. Go back to main menu \n")
        option = input("Choose your option: ")

        if option == '1':
            self.add_task_update(master_task_id)

        elif option == '2':
            return

#Highlights Code
    def add_highlight(self, master_task_id):
        if master_task_id:
            items = self.updates_db.get_updates(master_task_id)
            index, text = self.select_from_list(items)
            if not index:
                return
        else:
            return

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
        
        print(index, master_task_id, highlight_color)
        self.updates_db.add_highlight_to_update(index, highlight_color)

    # Function to fetch all highlights of a particular task.
    
    def delete_master_task(self, task_id):
        self.master_db.delete_task(task_id)

    def delete_task_update(self, update_id):
        self.updates_db.delete_update(update_id)

