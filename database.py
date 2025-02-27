import sqlite3
from datetime import datetime
from datetime import date
from datetime import timedelta

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
    
    def getTimestream(self, timestreamID):
        self.cursor.execute("""
            SELECT * FROM master_tasks WHERE task_id = ?;
        """, (timestreamID,))
    
    def getTimestreamName(self, timestreamID):
        self.cursor.execute("""
            SELECT task_name FROM master_tasks WHERE task_id = ?;
        """, (timestreamID,))
        return self.cursor.fetchone()[0]

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

    def getAllTimestreams(self):
        self.cursor.execute("""
        SELECT CAST(task_id AS TEXT), task_name FROM master_tasks;
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
    def getUpdates(self, master_task_id):
        self.cursor.execute("""
            SELECT update_id, task_id, update_date, update_time, update_text, highlight FROM task_updates 
            WHERE task_id = ? 
            ORDER BY update_date ASC, update_time ASC;
        """, (master_task_id,))
        return self.cursor.fetchall()
    
    def getUpdatesJoinMaster(self, master_task_id):
        self.cursor.execute("""
            SELECT task_updates.update_id, task_updates.task_id, task_updates.update_date, task_updates.update_time, task_updates.update_text, task_updates.highlight, master_tasks.task_name FROM task_updates
            JOIN master_tasks ON task_updates.task_id = master_tasks.task_id
            WHERE task_updates.task_id = ?
            ORDER BY update_date ASC, update_time ASC;
        """, (master_task_id,))
        return self.cursor.fetchall()
    
    def getUpdatesJoinGroupsLinkDB(self):
        self.cursor.execute("""
            SELECT task_updates.update_id, task_updates.task_id, task_updates.update_date, task_updates.update_time, task_updates.update_text, task_updates.highlight, task_update_links.group_id FROM task_updates
            JOIN task_updates_link ON task_updates.task_id = task_updates_link.update_id
            ORDER BY update_date ASC, update_time ASC;
        """)
        return self.cursor.fetchall()

    #write function to get updates from yesterday 12:01am to now
    def getUpdatesSinceYesterdayMidnight(self, master_task_id):
        yesterday_date_str = (datetime.now() - timedelta(days=1)).strftime("%m-%d-%Y")
        self.cursor.execute("""
            SELECT update_id, task_id, update_date, update_time, update_text, highlight FROM task_updates 
            WHERE task_id = ? AND update_date >= ? 
            ORDER BY update_date ASC, update_time ASC;
        """, (master_task_id, yesterday_date_str))
        return self.cursor.fetchall() 
    
    def getAllUpdatesSinceYesterdayMidnight(self):
        yesterday_date_str = (datetime.now() - timedelta(days=1)).strftime("%m-%d-%Y")
        self.cursor.execute("""
            SELECT update_id, task_id, update_date, update_time, update_text, highlight FROM task_updates
            WHERE update_date >= ?
            ORDER BY update_date ASC, update_time ASC;
        """, (yesterday_date_str,))
        return self.cursor.fetchall()

    def getAllUpdatesSinceYesterdayMidnightJoinMasterDBName(self):
        yesterday_date_str = (datetime.now() - timedelta(days=1)).strftime("%m-%d-%Y")
        self.cursor.execute("""
            SELECT task_updates.update_id, task_updates.task_id, master_tasks.task_name, task_updates.update_date, task_updates.update_time, task_updates.update_text, task_updates.highlight FROM task_updates
            JOIN master_tasks ON task_updates.task_id = master_tasks.task_id
            WHERE update_date >= ?
            ORDER BY update_date ASC, update_time ASC;
        """, (yesterday_date_str,))
        return self.cursor.fetchall()
        
    def getUpdateAndMaster(self, master_task_id, update_id):
        self.cursor.execute("""
            SELECT update_id, task_id, update_date, update_time, update_text, highlight FROM task_updates 
            WHERE task_id = ? AND update_id = ?;
        """, (master_task_id, update_id))
        return self.cursor.fetchone()

    def getUpdate(self, update_id):
        self.cursor.execute("""
            SELECT update_id, task_id, update_date, update_time, update_text, highlight FROM task_updates 
            WHERE update_id = ?;
        """, (update_id,))
        return self.cursor.fetchone()
    
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

class GroupsDB(Database):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_update_groups (
            group_id INTEGER PRIMARY KEY,
            master_task_id INTEGER,
            group_name TEXT,
            FOREIGN KEY (master_task_id) REFERENCES tasks (id)
            )
        """)
        self.conn.commit()

    def create_group(self, master_task_id, group_name):
        self.cursor.execute("""
            INSERT INTO task_update_groups (
            master_task_id, group_name) VALUES (?, ?)""",
            (master_task_id, group_name))
        self.conn.commit()

    def get_groups(self, master_task_id):
        self.cursor.execute("""
            SELECT group_id, group_name FROM task_update_groups 
            WHERE master_task_id = ?;
        """, (master_task_id,))
        return self.cursor.fetchall()
    

class GroupsLinkDB(Database):
    def __init__(self, db_name):
        super().__init__(db_name)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_update_links (
            update_id INTEGER,
            group_id INTEGER,
            FOREIGN KEY (update_id) REFERENCES task_updates (id),
            FOREIGN KEY (group_id) REFERENCES task_update_groups (group_id)
            )
        """)    
        self.conn.commit()

    def create_link(self, task_update_id, group_id):
        # Execute the SQL command
        self.cursor.execute("INSERT INTO task_update_links (update_id, group_id) VALUES (?, ?)",
                (task_update_id, group_id))
        # Commit the changes
        self.conn.commit()
        # Close the connection
    
    def get_links(self, group_id):
        self.cursor.execute("""
            SELECT update_id FROM task_update_links 
            WHERE group_id = ?;
        """, (group_id,))
        return self.cursor.fetchall()
    
    def get_updates_from_links(self, group_id):
        self.cursor.execute("""
            SELECT task_updates.update_id, task_updates.task_id, task_updates.update_date, task_updates.update_time, task_updates.update_text, task_updates.highlight FROM task_updates
            INNER JOIN task_update_links ON task_updates.update_id = task_update_links.update_id
            WHERE task_update_links.group_id = ?;
        """, (group_id,))
        return self.cursor.fetchall()

    



