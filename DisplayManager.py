from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.align import Align
import os
from database import MasterTaskDB, TaskUpdateDB, TaskHighlightDB

## I think that to change this you have to make it only manage displays
## right now there is some logic involved here, which is not good
class DisplayManager:
    def __init__(self):
        self.console = Console()

    def display_table(self, title, header_style, columns, data):
        table = Table(show_header=True, header_style=header_style)
        
        for header, style, width in columns.values():
            table.add_column(header, style=style, width=width)

        for row in data:
            table.add_row(*row)

        self.console.print(table)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_master_tasks(self, master_tasks):
        columns = {
            "1": ["Task_ID","dim", 10],
            "2": ["Master Task","dim", 40]
        }
        self.display_table("Master Tasks", "bold magenta", columns, master_tasks)

    def options_menu(self, options, title="Options Menu"):
        # options: A dictionary where keys are the option numbers/letters and values are the option descriptions.
        # title: The title to display at the top of the menu.

        menu_table = Table(title=title, show_header=False, header_style="bold blue")
        menu_table.add_column("Menu Options", justify="left", style="cyan")
        
        for option, description in options.items():
            menu_table.add_row(f"{option}) {description[0]}", style=description[1])

        self.console.print(menu_table)
    

    def display_update_details(self, master_task_id, update):
        update_id, _, date, time, text, highlight = update
        update_text = Text(text)
        if highlight:
            update_text.stylize("bold magenta")
        else:
            update_text.stylize("dim")
        update_table = Table(title="Update Details", show_header=False, header_style="bold blue")
        update_table.add_column("Update Details", justify="left", style="cyan")
        update_table.add_row(f"Master Task ID: {master_task_id}")
        update_table.add_row(f"Update ID: {update_id}")
        update_table.add_row(f"Date: {date}")
        update_table.add_row(f"Time: {time}")
        update_table.add_row(f"Update: {update_text}")
        self.console.print(update_table)

    

    def display_task_updates(self, task_updates):
        # Group updates by date
        updates_by_date = {}
        for update in task_updates:
            update_id, _, date, time, text, highlight = update
            if date in updates_by_date:
                updates_by_date[date].append((update_id, time, text, highlight))
            else:
                updates_by_date[date] = [(update_id, time, text, highlight)]

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Index", style="dim", width=6, justify="center")
        table.add_column("Date", width=12, justify="center")
        table.add_column("Time", style="dim", width=12, justify="center")
        table.add_column("Update", width=60)

        # Display updates
        for date, updates_on_date in updates_by_date.items():
            table.add_row("------", date, "------------", "-"*60)  # Add a row for the date
            for update in updates_on_date:
                update_id, time, text, highlight = update
                if highlight:
                    rich_text = Text.from_markup(f"[{highlight}]{text}[/]")
                    text = rich_text
                table.add_row(str(update_id), "", time, text)
                table.add_row("")
                
        self.console.print(table)

    def display_highlights(self, task_highlights):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Highlight ID", style="dim", width=10)
        table.add_column("Highlight Text", style="dim", width=40)
        table.add_column("Highlight Color", style="dim", width=10)

        for highlight in task_highlights:
            highlight_id, highlight_text, highlight_color = highlight
            table.add_row(str(highlight_id), highlight_text, highlight_color)

        self.console.print(table)

    def display_groups(self, groups):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Group ID", style="dim", width=10)
        table.add_column("Group Name", style="dim", width=40)

        for group in groups:
            group_id, group_name = group
            table.add_row(str(group_id), group_name)

        self.console.print(table)

    def display_group_updates(self, group_updates):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Task ID", style="dim", width=10)
        table.add_column("Task Name", style="dim", width=40)

        for task in group_updates:
            task_id, task_name = task
            table.add_row(str(task_id), task_name)

        self.console.print(table)