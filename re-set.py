import sqlite3


def drop_table(database_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Get the names of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Drop each table
    for table_name in tables:
        table_name = table_name[0]  # Extract table name from tuple
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Table {table_name} dropped.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("All tables dropped.")

drop_table('main.db')