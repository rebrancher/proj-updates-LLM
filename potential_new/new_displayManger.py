# displaymanager.py
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.align import Align
import os
from database import MasterTaskDB, TaskUpdateDB, TaskHighlightDB

class DisplayManager:
    def __init__(self):
        self.console = Console()

    # .....

    def display_table(self, title, header_style, columns, data):
        table = Table(show_header=True, header_style=header_style)
        
        for header, style, width in columns:
            table.add_column(header, style=style, width=width)

        for row in data:
            table.add_row(*row)

        self.console.print(table)
