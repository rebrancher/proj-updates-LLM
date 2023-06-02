from rich.console import Console
from rich.table import Table
from rich.text import Text
from database import MasterTaskDB, TaskUpdateDB, TaskHighlightDB

class TaskManager:
    def __init__(self, db_name):
        self.master_db = MasterTaskDB(db_name)
        self.updates_db = TaskUpdateDB(db_name)
        self.highlights_db = TaskHighlightDB(db_name)
        self.console = Console()

# Master Task Code

    def create_master_task(self, task_name):
        self.master_db.create_task(task_name)

    def list_master_tasks(self):
        tasks = self.master_db.list_master_tasks()

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Index", style="dim", width=12)
        table.add_column("Master Task", style="dim", width=20)

        for i, task in enumerate(tasks, start=1):
            table.add_row(str(i), task[1])

        self.console.print(table)

    def select_master_task(self):
        self.list_master_tasks()
        while True:
            try:
                task_index = int(input("Please enter the number of the Master Task you want to select: "))
                tasks = self.master_db.list_master_tasks()
                if 1 <= task_index <= len(tasks):
                    selected_task = tasks[task_index - 1]
                    return selected_task[0], selected_task[1]
                else:
                    print("\nInvalid selection.")
            except ValueError:
                print("\nInvalid input, please enter a number.")

# Updates Code

    def add_task_update(self, master_task_id):
        
        update_text = input("Enter your task update (max 300 chars): ")
        print("")
        self.updates_db.add_update(master_task_id, update_text, highlight=None)
        print("Task successfully added\n")

        self.menu_add_update(master_task_id)

    # def select_update(self, master_task_id = None):
    #     if not master_task_id:
    #         master_task_id = self.select_master_task()
    #     else:
    #         self.list_updates(self, master_task_id)
    #         while True:
    #             try:
    #                 update_index = int(input("Please enter the number of the Update you want to select: ")) 
    #                 updates = self.updates_db.get_updates()
    #                 if 1 <= update_index <= len(updates):
    #                     selected_update = updates[update_index - 1]
    #                     return selected_update[0], selected_update[1]
    #                 else:
    #                     print("\n Invalid selection.")
    #             except ValueError:
    #                 print("Invalid input, please enter a number")

    def select_update(self, master_task_id):
        self.list_updates(master_task_id)
        while True:
            try:
                task_index = int(input("Please enter the number of the update you want to select: "))
                tasks = self.updates_db.get_updates(master_task_id)
                if 1 <= task_index <= len(tasks):
                    selected_task = tasks[task_index - 1]
                    return selected_task[0], selected_task[1]
                else:
                    print("\nInvalid selection.")
            except ValueError:
                print("\nInvalid input, please enter a number.")

    
    def list_updates(self, master_task_id):
        updates = self.updates_db.get_updates(master_task_id)
        
        # Group updates by date
        updates_by_date = {}
        for update in updates:
            _, _, date, time, text, highlight = update
            if date in updates_by_date:
                updates_by_date[date].append((time, text, highlight))
            else:
                updates_by_date[date] = [(time, text, highlight)]

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Date", style="dim", width=12)
        table.add_column("Time", style="dim", width=12)
        table.add_column("Update", style="dim", width=60)

        # Display updates
        for date, updates_on_date in updates_by_date.items():
            for update in updates_on_date:
                time, text, highlight = update
                if highlight:
                    rich_text = Text()
                    rich_text.append(f"{text}", style="blue")
                    print(rich_text)
                    text = rich_text
                table.add_row(date, time, text)
                
        self.console.print(table)

    def menu_add_update(self, master_task_id):
        ##this part you have to figure out how to get menus out of the function codes

        print("Options:")
        print("1. Add new update")
        print("2. Go back to main menu \n")
        option = input("Choose your option: ")

        if option == '1':
            self.add_task_update(master_task_id)

        elif option == '2':
            return



    

   
#Highlights Code

    # Function to add a new highlight to a task.
    def add_highlight(self):
        master_task_id, _ = self.select_master_task()
        index, text = self.select_update(master_task_id)
        highlight_color = input("\nEnter the color for your highlight: ")
        print(index, master_task_id, highlight_color)
        self.updates_db.add_highlight_to_update(index, highlight_color)

    # Function to fetch all highlights of a particular task.
    def get_highlights(self, task_id):
        return self.highlights_db.get_highlights(task_id)
