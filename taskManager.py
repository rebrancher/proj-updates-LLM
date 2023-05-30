import os
from database import MasterTaskDB, TaskUpdateDB

class TaskManager:
    def __init__(self, db_name):
        self.master_db = MasterTaskDB(db_name)
        self.updates_db = TaskUpdateDB(db_name)

    def create_master_task(self, task_name):
        self.master_db.create_task(task_name)

    def add_task_update(self, task_id, update_text):
        self.updates_db.add_update(task_id, update_text)

    def list_master_tasks(self):
        print("\nMaster Task List")
        print("================")
        tasks = self.master_db.list_tasks()
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task[1]}")
        print("================\n")

    def select_master_task(self):
        self.list_master_tasks()
        while True:
            try:
                task_index = int(input("Please enter the number of the task you want to select: "))
                tasks = self.master_db.list_tasks()
                if 1 <= task_index <= len(tasks):
                    selected_task = tasks[task_index - 1]
                    return selected_task[0], selected_task[1]
                else:
                    print("\nInvalid selection.")
            except ValueError:
                print("\nInvalid input, please enter a number.")

    def get_task_updates(self, task_id, task_name):
        os.system('cls' if os.name == 'nt' else 'clear')

        updates = self.updates_db.get_updates(task_id)
        
        # Group updates by date
        updates_by_date = {}
        for update in updates:
            date, time, text = update
            if date in updates_by_date:
                updates_by_date[date].append((time, text))
            else:
                updates_by_date[date] = [(time, text)]
        
        # Display updates
        print(f"\nTask Updates for {task_name}\n------------")
        for date, updates_on_date in updates_by_date.items():
            print(f"\nDate: {date}")
            print("----------------")
            for update in updates_on_date:
                time, text = update
                print(f"{time} -- Update: {text}\n")
        print("====================================\n")
        
        while True:
            print("Options:")
            print("1. Add new update")
            print("2. Go back to main menu")
            option = input("Choose your option: ")

            if option == '1':
                update_text = input("Enter your task update (max 300 chars): ")
                self.updates_db.add_update(task_id, update_text)
                # Refresh task updates view after adding new update
                self.get_task_updates(task_id, task_name)
            elif option == '2':
                break
            else:
                print("Invalid option, try again.")
