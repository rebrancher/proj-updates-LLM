from database import Database, MasterTaskDB, TaskUpdateDB, TaskHighlightDB


class database_viewer:
    def __init__(self, db_name):
        self.database = Database(db_name)
        self.master_db = MasterTaskDB(db_name)
        self.updates_db = TaskUpdateDB(db_name)
        self.highlights_db = TaskHighlightDB(db_name)

    def view_tables(self):
        print("task_updates")
        self.database.view_table("task_updates")
        print("\n master_tasks")
        self.database.view_table("master_tasks")
        print("\n task_highlights")
        self.database.view_table("task_highlights")


if __name__ == "__main__":
    db_name = "task.db"
    db_viewer = database_viewer(db_name)
    db_viewer.view_tables()