import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def view_table(self, table_name):
        c = self.cursor.execute(f"SELECT * FROM {table_name}")
        for row in c.fetchall(): 
            print(row)
        #return self.cursor.fetchall()

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

    def get_master_tasks(self):
        self.cursor.execute("""
            SELECT * FROM master_tasks;
        """)
        return self.cursor.fetchall()
    
    def view_table(self):
        print("master_tasks")
        return super().view_table("master_tasks")
    
    def delete_task(self, task_id):
        self.cursor.execute("""
            DELETE FROM master_tasks WHERE task_id = ?;
        """, (task_id,))
        self.conn.commit()
    
    
        

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
                highlight TEXT,
                FOREIGN KEY (task_id) REFERENCES master_tasks (task_id)
            );
        """)

    def add_update(self, task_id, update_text, highlight=None):
        date_str = datetime.now().strftime("%m-%d-%Y")
        time_str = datetime.now().strftime("%H:%M:%S")
        self.cursor.execute("""
            INSERT INTO task_updates (task_id, update_date, update_time, update_text, highlight) 
            VALUES (?, ?, ?, ?, ?);
        """, (task_id, date_str, time_str, update_text, highlight))
        self.conn.commit()

    #change this to list_updates
    def get_updates(self, master_task_id):
        self.cursor.execute("""
            SELECT update_id, task_id, update_date, update_time, update_text, highlight FROM task_updates 
            WHERE task_id = ? 
            ORDER BY update_date ASC, update_time ASC;
        """, (master_task_id,))
        return self.cursor.fetchall()
    
    def add_highlight_to_update(self, task_id, highlight):
        self.cursor.execute("""
            UPDATE task_updates
            SET highlight = ?
            where update_id = ?;
        """, (highlight, task_id))
        self.conn.commit()
    
    def view_table(self):
        print("task_updates")
        return super().view_table("task_updates")
    
    def delete_update(self, update_id):
        self.cursor.execute("""
            DELETE FROM task_updates WHERE update_id = ?;
        """, (update_id,))
        self.conn.commit()
    
    # TaskHighlightDB inherits from the Database class.

    #not sure if this is ever used or is necessary
class TaskHighlightDB(Database):
    def __init__(self, db_name):
        super().__init__(db_name)
        # SQL command to create a new table "task_highlights" in the database,
        # if it does not already exist.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_highlights(
                highlight_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                highlight_text TEXT NOT NULL,
                highlight_color TEXT NOT NULL,
                FOREIGN KEY (task_id) REFERENCES master_tasks (task_id)
            );
        """)

    # Function to add a new highlight to the database.
    def add_highlight(self, task_id, highlight_text, highlight_color):
        self.cursor.execute("""
            INSERT INTO task_highlights (task_id, highlight_text, highlight_color) 
            VALUES (?, ?, ?);
        """, (task_id, highlight_text, highlight_color))
        self.conn.commit()  # Save the changes to the database.

    # Function to fetch all highlights associated with a particular task from the database.
    def get_highlights(self, task_id):
        self.cursor.execute("""
            SELECT highlight_text, highlight_color FROM task_highlights 
            WHERE task_id = ?;
        """, (task_id,))
        return self.cursor.fetchall()  # Return all rows fetched from the database.
    
    def view_table(self):
        print("task_highlights")
        return super().view_table("task_highlights")

