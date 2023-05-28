import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

class MasterTaskDB(Database):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS master_tasks(
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL
            );
        """)

    def create_task(self, task_name):
        self.cursor.execute("""
            INSERT INTO master_tasks (task_name) VALUES (?);
        """, (task_name,))
        self.conn.commit()

    def list_tasks(self):
        self.cursor.execute("""
            SELECT * FROM master_tasks;
        """)
        return self.cursor.fetchall()

class TaskUpdateDB(Database):
    def __init__(self, db_name):
        super().__init__(db_name)
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

    def add_update(self, task_id, update_text):
        date_str = datetime.now().strftime("%m-%d-%Y")
        time_str = datetime.now().strftime("%H:%M:%S")
        self.cursor.execute("""
            INSERT INTO task_updates (task_id, update_date, update_time, update_text) 
            VALUES (?, ?, ?, ?);
        """, (task_id, date_str, time_str, update_text))
        self.conn.commit()

    def get_updates(self, task_id):
        self.cursor.execute("""
            SELECT update_date, update_time, update_text FROM task_updates 
            WHERE task_id = ? 
            ORDER BY update_date ASC, update_time ASC;
        """, (task_id,))
        return self.cursor.fetchall()
