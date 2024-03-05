from rich.console import Console
from rich.table import Table, Column
from rich.text import Text
from rich.align import Align
import os
from database import MasterTaskDB, TaskUpdateDB, TaskHighlightDB

#Sort by KEYWORD

class DisplayManager:
    def __init__(self):
        self.console = Console()
        self.master_db = MasterTaskDB("task.db")
    
    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def getUpdatesTable(self):
        tableTitle = "Updates"
        tableHeaderStyle = "bold magenta"
        table = Table(title=tableTitle, show_header=True, header_style=tableHeaderStyle)
        table.add_column("Index", style="dim", width=6, justify="center")
        table.add_column("Date", width=12, justify="center")
        table.add_column("Time", style="dim", width=12, justify="center")
        table.add_column("Update", width=60)
        table.add_column("Misc", style="dim", width=10, justify="center")
        return table
    
    def displayUpdatesOrderedby(self, taskUpdates, orderBy):
        updatesByOrder = {}
        for update in taskUpdates:
            updateID, taskID, date, time, text, highlight, misc = update
            dicti = {
                'updateID': updateID,
                'taskID': taskID,
                'date': date,
                'time': time,
                'text': text,
                'highlight': highlight,
                'misc': misc
            }

            if orderBy in dicti:
                if dicti[orderBy] in updatesByOrder:
                    updatesByOrder[dicti[orderBy]].append(dicti)
                else:
                    updatesByOrder[dicti[orderBy]] = [dicti]
            else:
                print("Invalid order by")
                return
            
            table = self.getUpdatesTable()
            for order, updates in updatesByOrder.items():
                table.add_row("------", order, "------------", "-"*60)
                for update in updates:
                    table.add_row(str(update['updateID']), "", update['time'], update['text'], update['misc'])
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


    def displayTable(self, **kwargs):
        tableTitle = kwargs["tableTitle"]
        tableHeaderStyle = kwargs["tableHeaderStyle"]
        columns = kwargs["columns"]
        data = kwargs["data"]
        table = Table(title=tableTitle, show_header=True, header_style=tableHeaderStyle)

        for colInfo in columns:
            table.add_column(header=colInfo["header"], style=colInfo["style"], width=colInfo["width"])
        
        for row in data:
            table.add_row(*row)

        self.console.print(table)
        print("\n")

    def displayTimestreams1(self):
        timestreams = self.master_db.getAllTimestreams()
        columns = [
            {"header": "ID", "style": "dim", "width": 10}, 
            {"header": "Timestreams", "style": "dim", "width": 40}
            ]
        self.displayTable(tableTitle="Timestreams", tableHeaderStyle="bold magenta", columns=columns, data=timestreams)

    def optionsMenu(self, options):
        menu = Table(title="Options Menu", show_header=False, header_style="bold blue")
        menu.add_column("Menu Options", justify="left", style="cyan")
        
        for option, description in options.items():
            menu.add_row(f"{option}) {description[0]}", style=description[1])
        self.console.print(menu)
    

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

    def displayUpdatesWithMasterTaskIDAndName(self, updates):
        updatesByTimestream = {}
        for update in updates:
            update_id, timestreamID, master_name, date, time, text, highlight = update
            if timestreamID in updatesByTimestream:
                updatesByTimestream[timestreamID].append([update_id, timestreamID, master_name, date, time, text, highlight])
            else:
                updatesByTimestream[timestreamID] = [(update_id, timestreamID, master_name, date, time, text, highlight)]

        table = self.getUpdatesTable()
        for timestreamID, updates in updatesByTimestream.items():
            table.add_row(f"------", f"Timestream ID: {timestreamID}", f"------------", f"-"*60)
            for update in updates:
                update_id, timestreamID, master_name, date, time, text, highlight = update
                if highlight:
                    rich_text = Text.from_markup(f"[{highlight}]{text}[/]")
                    text = rich_text
                table.add_row(str(update_id), master_name, time, text)
                table.add_row("")
        
        self.console.print(table)

        