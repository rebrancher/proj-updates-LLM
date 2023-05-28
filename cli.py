import os

class CLI:
    def __init__(self, master_db, updates_db):
        self.master_db = master_db
        self.updates_db = updates_db

    def run_cli(self):
        while True:
            print("\nWelcome to the task manager, select from the menu below:\n")
            print("1. Create Master Task")
            print("2. Add Task Update")
            print("3. View Task Updates")
            print("4. Exit\n")
            choice = input("Enter your choice: ")

            if choice == '1':
                task_name = input("\nEnter the name of the new Master Task: ")
                self.master_db.create_task(task_name)

            elif choice == '2':
                task_id, _ = self.select_master_task()  # we don't care about task_name here
                update_text = input("\nEnter your task update (max 300 chars): ")
                self.updates_db.add_update(task_id, update_text)

            elif choice == '3':
                task_id, task_name = self.select_master_task()
                self.get_task_updates(task_id, task_name)

            elif choice == '4':
                print("\nExiting...\n")
                break

            else:
                print("\nInvalid choice. Please enter a number between 1 and 4.\n")

    def list_master_tasks(self):
        print("\nMaster Task List")
        print("================")
        tasks = self.master_db.list_tasks()
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task[1]}")
        print("================\n")

    def select_master_task(self):
        self.list_master_tasks()
        task_index = int(input("Please enter the number of the task you want to select: "))
        tasks = self.master_db.list_tasks()
        if 1 <= task_index <= len(tasks):
            selected_task = tasks[task_index - 1]
            return selected_task[0], selected_task[1]  # returns both task_id and task_name
        else:
            print("\nInvalid selection.")
            return None, None

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

if __name__ == "__main__":
    from database import MasterTaskDB, TaskUpdateDB
    master_db = MasterTaskDB('task.db')
    updates_db = TaskUpdateDB('task.db')
    cli = CLI(master_db, updates_db)
    cli.run_cli()
