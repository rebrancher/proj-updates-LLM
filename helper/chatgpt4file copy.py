cli.py:
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
            #Display Master Tasks
            self.display_manager.clear_screen()
            master_tasks = self.master_db.get_master_tasks_string()
            self.display_manager.display_master_tasks(master_tasks)
            print("\n")
            
            #Handles master task input
            item_index = self.task_manager.master_task_menu()
            if isinstance(item_index, int):
                #need to update select_list
                master_task_id, _ = self.task_manager.select_from_list(master_tasks, item_index)

                #add_task_update should be something like updates_handler?
                if master_task_id:
                    self.task_manager.add_task_update(master_task_id)
                else:
                    break
            elif item_index == 'c':

                #Saving...

                print("\nGoodbye!\n")
                break
            else:
                continue

if __name__ == "__main__":
    db_name = 'task.db'
    task_manager = TaskManager(db_name)
    cli = CLI(task_manager, db_name)
    cli.run_cli()
taskmanager.py
from rich.console import Console
from rich.table import Table
from database import MasterTaskDB, TaskUpdateDB, TaskHighlightDB, GroupsLinkDB, GroupsDB 
from rich.prompt import Prompt
from DisplayManager import DisplayManager



class TaskManager:
    def __init__(self, db_name):
        self.master_db = MasterTaskDB(db_name)
        self.updates_db = TaskUpdateDB(db_name)
        self.highlights_db = TaskHighlightDB(db_name)
        self.groups_db = GroupsDB(db_name)
        self.groupsLink_db = GroupsLinkDB(db_name)
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
                "1": ["Create a new Master Task", "green"],
                "2": ["Delete a Master Task", "red"],
                "3": ["Exit options menu", "blue"]
            }
            self.display_manager.display_master_tasks(self.master_db.get_master_tasks())
            self.display_manager.options_menu(options, title="Master Task Options")
            selected_option = Prompt.ask("Choose an option: ")
            if selected_option == '1':
                task_name = input("Enter the name of the new Master Task: ")
                self.master_db.create_task(task_name)
            elif selected_option == '2':
                self.delete_master_task()
                print("Deleting a Master Task...")
                input("Press enter to continue...")
            elif selected_option == '3':
                break
            else:
                continue



            
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
        response = input("\nEnter update (300 characters max), 'c' to cancel, or 'o' for options: \n\n")
        if response.lower() == 'c':
            return 'c'
        elif response.lower() == 'o':
            self.task_update_options(master_task_id)
        else:
            self.updates_db.add_update(master_task_id, response)

    def task_update_options(self, master_task_id):
        options = {
                "1": ["Delete Update", "red", self.delete_task_update],
                "2": ["Add a highlight", "green", self.add_highlight],
                "3": ["Get Update Details", "cyan", self.update_details],
                "4": ["Create a group", "blue", self.create_group],
                "5": ["Add to group", "blue", self.add_to_group],
                "6": ["View updates in group", "blue", self.get_group_updates_with_text],
                "7": ["Exit update mode", "yellow", None]
            }

        self.display_manager.options_menu(options, title="Update Menu")
        get_num = Prompt.ask("Choose an option: ")
        if get_num in options:
            selected_option = options[get_num][2]
        self.execute_task_update_option(selected_option, master_task_id)

    def execute_task_update_option(self, selected_option, master_task_id):
        if selected_option:
            selected_option(master_task_id)
        else:
            return
    
    def update_details(self, master_task_id):
        update_id = Prompt.ask("Enter the number of the update you want to view: ")
        update = self.updates_db.get_update(master_task_id, update_id)
        self.display_manager.display_update_details(master_task_id, update)
        input("Press enter to continue...")

    

#**********************************************************************************************************************
#****************************************** Highlights Code ***********************************************************
#**********************************************************************************************************************

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

    def delete_task_update(self, master_task_id):
        update_id = Prompt.ask("Input #id of task you want to delete")
        prompt = Prompt.ask("Are you sure you want to delete this update? (y/n)")
        if prompt == 'y':
            self.updates_db.delete_update(update_id)
        else:
            Prompt.ask("Delete cancelled. Press enter to continue...")
            return


#**********************************************************************************************************************
#****************************************** Links Code ***********************************************************
#**********************************************************************************************************************


#**********************************************************************************************************************
#****************************************** Groups Code ***********************************************************
#**********************************************************************************************************************

    def create_group(self, master_task_id):
        group_name = input("Enter the name of the new group: ")
        self.groups_db.create_group(master_task_id, group_name)
    
    def get_group_id(self, master_task_id):
        groups = self.groups_db.get_groups(master_task_id)
        self.display_manager.display_groups(groups)
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
        
        self.display_manager.display_task_updates(updates)
        input("Press enter to continue...")
displaymanager.py
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.align import Align
import os
from database import MasterTaskDB, TaskUpdateDB, TaskHighlightDB


class DisplayManager:
    def __init__(self):
        self.console = Console()

    def display_table(self, title, header_style, columns, data):
        table = Table(show_header=True, header_style=header_style)
        
        for header, style, width in columns.values():
            table.add_column(header, style=style, width=width)

        for row in data:
            table.add_row(*row)

        self.console.print(table)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_master_tasks(self, master_tasks):
        columns = {
            "1": ["Task_ID","dim", 10],
            "2": ["Master Task","dim", 40]
        }
        self.display_table("Master Tasks", "bold magenta", columns, master_tasks)

    def options_menu(self, options, title="Options Menu"):
        # options: A dictionary where keys are the option numbers/letters and values are the option descriptions.
        # title: The title to display at the top of the menu.

        menu_table = Table(title=title, show_header=False, header_style="bold blue")
        menu_table.add_column("Menu Options", justify="left", style="cyan")
        
        for option, description in options.items():
            menu_table.add_row(f"{option}) {description[0]}", style=description[1])

        self.console.print(menu_table)
    

    def display_update_details(self, master_task_id, update):
        update_id, _, date, time, text, highlight = update
        update_text = Text(text)
        if highlight:
            update_text.stylize("bold magenta")
        else:
            update_text.stylize("dim")
        update_table = Table(title="Update Details", show_header=False, header_style="bold blue")
        update_table.add_column("Update Details", justify="left", style="cyan")
        update_table.add_row(f"Master Task ID: {master_task_id}")
        update_table.add_row(f"Update ID: {update_id}")
        update_table.add_row(f"Date: {date}")
        update_table.add_row(f"Time: {time}")
        update_table.add_row(f"Update: {update_text}")
        self.console.print(update_table)

    

    def display_task_updates(self, task_updates):
        # Group updates by date
        updates_by_date = {}
        for update in task_updates:
            update_id, _, date, time, text, highlight = update
            if date in updates_by_date:
                updates_by_date[date].append((update_id, time, text, highlight))
            else:
                updates_by_date[date] = [(update_id, time, text, highlight)]

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Index", style="dim", width=6, justify="center")
        table.add_column("Date", width=12, justify="center")
        table.add_column("Time", style="dim", width=12, justify="center")
        table.add_column("Update", width=60)

        # Display updates
        for date, updates_on_date in updates_by_date.items():
            table.add_row("------", date, "------------", "-"*60)  # Add a row for the date
            for update in updates_on_date:
                update_id, time, text, highlight = update
                if highlight:
                    rich_text = Text.from_markup(f"[{highlight}]{text}[/]")
                    text = rich_text
                table.add_row(str(update_id), "", time, text)
                table.add_row("")
                
        self.console.print(table)

    def display_highlights(self, task_highlights):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Highlight ID", style="dim", width=10)
        table.add_column("Highlight Text", style="dim", width=40)
        table.add_column("Highlight Color", style="dim", width=10)

        for highlight in task_highlights:
            highlight_id, highlight_text, highlight_color = highlight
            table.add_row(str(highlight_id), highlight_text, highlight_color)

        self.console.print(table)

    def display_groups(self, groups):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Group ID", style="dim", width=10)
        table.add_column("Group Name", style="dim", width=40)

        for group in groups:
            group_id, group_name = group
            table.add_row(str(group_id), group_name)

        self.console.print(table)

    def display_group_updates(self, group_updates):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Task ID", style="dim", width=10)
        table.add_column("Task Name", style="dim", width=40)

        for task in group_updates:
            task_id, task_name = task
            table.add_row(str(task_id), task_name)

        self.console.print(table)
database.py
