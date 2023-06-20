from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.align import Align
import os
from database import MasterTaskDB, TaskUpdateDB, TaskHighlightDB


class DisplayManager:
    def __init__(self):
        self.console = Console()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_main_menu(self):
        menu = Table(title="Main Menu", show_header=False, header_style="bold blue")
        menu.add_column("Menu Options", justify="left", style="cyan")
        menu.add_row("1) Add Task Update")
        menu.add_row("2) Add Highlight")
        menu.add_row("3) Exit program")
        self.console.print(menu)

    def display_master_tasks(self, master_tasks):
        tasks = master_tasks
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Task ID", style="dim", width=8)
        table.add_column("Master Task", style="dim", width=40)

        for task in tasks:
            table.add_row(Align.center(str(task[0])), task[1])

        self.console.print(table)

    def display_task_updates(self, task_updates):
        # Group updates by date
        updates_by_date = {}
        for update in task_updates:
            _, _, date, time, text, highlight = update
            if date in updates_by_date:
                updates_by_date[date].append((time, text, highlight))
            else:
                updates_by_date[date] = [(time, text, highlight)]

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Index", style="dim", width=6, justify="center")
        table.add_column("Date", width=12, justify="center")
        table.add_column("Time", style="dim", width=12, justify="center")
        table.add_column("Update", width=60)

        # Display updates
        index = 1
        for date, updates_on_date in updates_by_date.items():
            table.add_row("------", date, "------------", "-"*60)  # Add a row for the date
            for update in updates_on_date:
                time, text, highlight = update
                if highlight:
                    rich_text = Text.from_markup(f"[{highlight}]{text}[/]")
                    text = rich_text
                table.add_row(str(index), "", time, text)
                table.add_row("")
                index += 1
                
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
