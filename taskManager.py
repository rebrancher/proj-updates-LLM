import sqlite3
from datetime import datetime
import os

class TaskManager:
    def __init__(self):
        self.conn = sqlite3.connect('task.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS master_tasks(
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_updates(
                update_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                update_date TEXT NOT NULL,
                update_time TEXT NOT NULL,
                update_text TEXT NOT NULL,
                FOREIGN KEY (task_id) REFERENCES master_tasks (task_id)
            );
        """)

    def create_master_task(self, task_name):
        self.cursor.execute("""
            INSERT INTO master_tasks (task_name) VALUES (?);
        """, (task_name,))
        self.conn.commit()

    def add_task_update(self, task_id, update_text):
        date_str = datetime.now().strftime("%m-%d-%Y")
        time_str = datetime.now().strftime("%H:%M:%S")
        self.cursor.execute("""
            INSERT INTO task_updates (task_id, update_date, update_time, update_text) 
            VALUES (?, ?, ?, ?);
        """, (task_id, date_str, time_str, update_text))
        self.conn.commit()

    def list_master_tasks(self):
        print("\nMaster Task List")
        print("================")
        self.cursor.execute("""
            SELECT * FROM master_tasks;
        """)
        tasks = self.cursor.fetchall()
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task[1]}")
        print("================\n")

    def select_master_task(self):
        self.list_master_tasks()
        task_index = int(input("Please enter the number of the task you want to select: "))
        self.cursor.execute("""
            SELECT * FROM master_tasks;
        """)
        tasks = self.cursor.fetchall()
        if 1 <= task_index <= len(tasks):
            selected_task = tasks[task_index - 1]
            return selected_task[0], selected_task[1]  # returns both task_id and task_name
        else:
            print("\nInvalid selection.")
            return None, None

    def get_task_updates(self, task_id, task_name):
        os.system('cls' if os.name == 'nt' else 'clear')

        self.cursor.execute("""
            SELECT update_date, update_time, update_text FROM task_updates 
            WHERE task_id = ? 
            ORDER BY update_date ASC, update_time ASC;
        """, (task_id,))
        updates = self.cursor.fetchall()
        print(f"\nTask Updates for {task_name}\n------------")
        for update in updates:
            print(f"Date: {update[0]} -- Time: {update[1]}")
            print("----------------------------------------")
            print(f"Update: {update[2]}\n")
        print("====================================\n")
        input("Press any key to continue...")

def run_cli():
    taskManager = TaskManager()
    while True:
        print("\nWelcome to the task manager, select from the menu below:\n")
        print("1. Create Master Task")
        print("2. Add Task Update")
        print("3. View Task Updates")
        print("4. Exit\n")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            task_name = input("\nEnter the name of the new Master Task: ")
            taskManager.create_master_task(task_name)

        elif choice == '2':
            task_id, _ = taskManager.select_master_task()  # we don't care about task_name here
            update_text = input("\nEnter your task update (max 300 chars): ")
            taskManager.add_task_update(task_id, update_text)

        elif choice == '3':
            task_id, task_name = taskManager.select_master_task()
            taskManager.get_task_updates(task_id, task_name)

        elif choice == '4':
            print("\nExiting...\n")
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.\n")

if __name__ == "__main__":
    run_cli()
