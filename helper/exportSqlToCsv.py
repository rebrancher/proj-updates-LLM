import sqlite3
import csv
from pathlib import Path


path = Path(__file__).parent.parent
path = str(path) + "/task.db"
print("PATH")
print(path)
# Connect to the SQLite database
conn = sqlite3.connect(str(path))
cursor = conn.cursor()

# Execute a SELECT statement to fetch the data from the SQLite table
cursor.execute("SELECT update_date, update_time, update_text, highlight FROM task_updates WHERE task_id = 1;")

# Fetch all rows from the last executed statement
rows = cursor.fetchall()

# Define the name of the CSV file to export to
csv_filename = 'my_table.csv'

# Open the CSV file in write mode
with open(csv_filename, 'w', newline='') as csv_file:
    # Create a CSV writer
    csv_writer = csv.writer(csv_file)
    
    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Write the header to the CSV file
    csv_writer.writerow(column_names)

    # Write all rows to the CSV file
    csv_writer.writerows(rows)

print(f"Data exported to '{csv_filename}' successfully.")
