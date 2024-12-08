import sqlite3
import csv
import re
import os

def clean_column_name(name):
    """Clean column names to ensure they are valid SQL identifiers."""
    name = name.strip()
    name = re.sub(r'\s+', '_', name)  # Replace spaces with underscores
    name = re.sub(r'[^\w_]', '', name)  # Remove invalid characters
    return name

def import_csv_to_db(csv_files, db_file):
    """
    Import a list of CSV files into a SQLite database.

    Args:
        csv_files (list): List of paths to CSV files.
        db_file (str): Path to the SQLite database file.

    Raises:
        ValueError: If no CSV files are provided or db_file is empty.
        Exception: For any errors during database operations.
    """
    if not csv_files:
        raise ValueError("No CSV files provided.")
    if not db_file:
        raise ValueError("Database file path is empty.")

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        for csv_file in csv_files:
            table_name = os.path.splitext(os.path.basename(csv_file))[0]

            with open(csv_file, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                header = next(csvreader)

                cleaned_header = [clean_column_name(col) for col in header]
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(cleaned_header)})")

                for row in csvreader:
                    cursor.execute(
                        f"INSERT INTO {table_name} ({', '.join(cleaned_header)}) VALUES ({', '.join(['?' for _ in cleaned_header])})",
                        row
                    )

        conn.commit()
    except Exception as e:
        raise Exception(f"Error importing CSV files: {e}")
    finally:
        conn.close()
