from database import MasterTaskDB, TaskUpdateDB, TaskHighlightDB

master_db = MasterTaskDB("task.db")
updates_db = TaskUpdateDB("task.db")
highlights_db = TaskHighlightDB("task.db")

print(master_db.view_table())
print("check")
print(updates_db.view_table())
print(highlights_db.view_table())
