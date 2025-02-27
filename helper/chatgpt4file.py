cli.py:
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
taskmanager.py
from rich.console import Console
from rich.table import Table
from database import MasterTaskDB, TaskUpdateDB, TaskHighlightDB, GroupsLinkDB, GroupsDB 
from rich.prompt import Prompt
from DisplayManager import DisplayManager

#just put on your backpack and go

class TaskManager:
    def __init__(self, db_name):
        #should there be a DB class that all of these inherit from?
        self.master_db = MasterTaskDB(db_name)
        self.updates_db = TaskUpdateDB(db_name)
        self.highlights_db = TaskHighlightDB(db_name)
        self.groups_db = GroupsDB(db_name)
        self.groupsLink_db = GroupsLinkDB(db_name)
        self.displayManager = DisplayManager()
        self.console = Console()
 
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
            
#**********************************************************************************************************************
#****************************************** Updates Code **************************************************************
#**********************************************************************************************************************    

    def updatePromptAndProcess(self, timestreamID):
        responseIsNotCancel = True
        while responseIsNotCancel:
            self.viewUpdates(timestreamID)
            responseIsNotCancel = self.processUpdate(timestreamID)
            

    def viewUpdates(self, timestreamID):
        self.displayManager.clearScreen()
        self.displayManager.displayUpdates(self.updates_db.getUpdates(timestreamID))
        print(self.master_db.getTimestreamName(timestreamID))
    
    def processUpdate(self, timestreamID):
        update = input("\nEnter update (300 characters max), 'c' to cancel, or 'o' for options: \n\n")
        if update.lower() == 'c':
            return False
        elif update.lower() == 'o':
            self.updateOptions(timestreamID)
        else:
            self.updates_db.add_update(timestreamID, update)
        return True
    

    def updateOptions(self, timestreamID):
        #how do you access the methods in OOP? 
        updateOptionsMenuChoices = {
                "1": ["Delete Update", "red", self.delete_task_update],
                "2": ["Add a highlight", "green", self.add_highlight],
                "3": ["Get Update Details", "cyan", self.update_details],
                "4": ["Create a group", "blue", self.create_group],
                "5": ["Add to group", "blue", self.add_to_group],
                "6": ["View updates in group", "blue", self.get_group_updates_with_text],
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
        update = self.updates_db.get_update(master_task_id, update_id)
        self.displayManager.display_update_details(master_task_id, update)
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
displaymanager.py
from rich.console import Console
from rich.table import Table, Column
from rich.text import Text
from rich.align import Align
import os
from database import MasterTaskDB, TaskUpdateDB, TaskHighlightDB

## I think that to change this you have to make it only manage displays
## right now there is some logic involved here, which is not good
class DisplayManager:
    def __init__(self):
        self.console = Console()
        self.master_db = MasterTaskDB("task.db")

    def displayTable(self, **kwargs):
        tableTitle = kwargs["tableTitle"]
        tableHeaderStyle = kwargs["tableHeaderStyle"]
        columns = kwargs["columns"]
        data = kwargs["data"]
        table = Table(title=tableTitle, show_header=True, header_style=tableHeaderStyle)

        for colInfo in columns:
            print(colInfo)
            table.add_column(header=colInfo["header"], style=colInfo["style"], width=colInfo["width"])
        
        for row in data:
            table.add_row(*row)

        self.console.print(table)

    def displayTimestreams1(self):
        timestreams = self.master_db.getAllTimestreams()
        columns = [
            {"header": "Task_ID", "style": "dim", "width": 10}, 
            {"header": "Master Task", "style": "dim", "width": 40}
            ]
        self.displayTable(tableTitle="Timestreams", tableHeaderStyle="bold magenta", columns=columns, data=timestreams)

    def display_table(self, title, header_style, columns, data):
        table = Table(show_header=True, header_style=header_style)
        
        for header, style, width in columns.values():
            table.add_column(header, style=style, width=width)

        for row in data:
            table.add_row(*row)

        self.console.print(table)

    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')


    def optionsMenu(self, options):
        menu = Table(title="Options Menu", show_header=False, header_style="bold blue")
        menu.add_column("Menu Options", justify="left", style="cyan")
        
        for option, description in options.items():
            menu.add_row(f"{option}) {description[0]}", style=description[1])
        self.console.print(menu)
    

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

    

    def displayUpdates(self, task_updates):
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
    
    def displayUpdatesWithMasterTaskIDAndName(self, updates):
        # Group updates by date
        updatesByTimestream = {}
        for update in updates:
            update_id, timestreamID, master_name, date, time, text, highlight = update
            if timestreamID in updatesByTimestream:
                updatesByTimestream[timestreamID].append(update_id, timestreamID, master_name, date, time, text, highlight)
            else:
                updatesByTimestream[timestreamID] = [(update_id, timestreamID, master_name, date, time, text, highlight)]

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Index", style="dim", width=6, justify="center")
        table.add_column("Date", width=12, justify="center")
        table.add_column("TS ID", width=5)
        table.add_column("TS Name", width=15)
        table.add_column("Time", style="dim", width=12, justify="center")
        table.add_column("Update", width=60)
        

        # Display updates
        for timestreamID, updatesByTimestream in updatesByTimestream.items():
            table.add_row("------", date, "-"*5, "-"*15, "----------"*60, "----------------------------------------")
            for update in updatesByTimestream:
                update_id, timestreamID, master_name, date, time, text, highlight = update
                if highlight:
                    rich_text = Text.from_markup(f"[{highlight}]{text}[/]")
                    text = rich_text
                table.add_row(str(update_id), "" , str(timestreamID), master_name, time, text)
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
