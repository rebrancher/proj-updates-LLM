# Task Manager Application Documentation - Continued

Below, we dive deeper into the important functions that are called within each method of the `TaskManager` class in `taskmanager.py`.

### `TaskManager` class:

---

#### **`main_loop()`**

This is the main function that drives the program. It continuously displays the options menu and processes user input until the user decides to exit.

*Important functions called within:*
- `self.display_manager.options_menu()`: Displays the main menu options.
- `self.add_master_task()`, `self.view_master_tasks()`, etc: Calls the appropriate function based on the user's selection.

**Function tree:**
```
main_loop()
├── options_menu()
├── add_master_task()
├── view_master_tasks()
├── delete_master_task()
├── add_task_update()
├── view_task_updates()
├── delete_task_update()
├── add_highlight()
├── delete_highlight()
└── add_task_to_group()
```

---

#### **`add_master_task()`**

This function is used to create a new master task.

*Important functions called within:*
- `self.display_manager.input_master_task()`: Gets input from the user for the master task details.
- `self.master_task_db.add_task()`: Adds the new master task to the database.

**Function tree:**
```
add_master_task()
├── input_master_task()
└── add_task()
```

---

#### **`view_master_tasks()`**

This function is used to display all master tasks.

*Important functions called within:*
- `self.master_task_db.get_tasks()`: Retrieves all master tasks from the database.
- `self.display_manager.display_master_tasks()`: Displays the retrieved tasks.

**Function tree:**
```
view_master_tasks()
├── get_tasks()
└── display_master_tasks()
```

---

#### **`delete_master_task()`**

This function is used to delete a master task.

*Important functions called within:*
- `self.display_manager.select_master_task()`: Gets user selection for which master task to delete.
- `self.master_task_db.delete_task()`: Deletes the selected task from the database.

**Function tree:**
```
delete_master_task()
├── select_master_task()
└── delete_task()
```

---

#### **`add_task_update()`**

This function is used to add an update to a specific master task.

*Important functions called within:*
- `self.display_manager.select_master_task()`: Gets user selection for which master task to update.
- `self.display_manager.input_task_update()`: Gets user input for the task update details.
- `self.task_update_db.add_update()`: Adds the new task update to the database.

**Function tree:**
```
add_task_update()
├── select_master_task()
├── input_task_update()
└── add_update()
```

---

#### **`view_task_updates()`**

This function is used to view all updates for a specific master task.

*Important functions called within:*
- `self.display_manager.select_master_task()`: Gets user selection for which master task to view updates for.
- `self.task_update_db.get_updates()`: Retrieves all updates for the selected task from the database.
- `self.display_manager.display_task_updates()`: Displays the retrieved updates.

**Function tree:**
```
view_task_updates()
├── select_master_task()
├── get_updates()
└── display_task_updates()
```

---

#### **`delete_task_update()`**

This function is used to delete a task update.

*Important functions called within:*
- `self.display_manager.select_task_update()`: Gets user selection for which task update to delete.
- `self