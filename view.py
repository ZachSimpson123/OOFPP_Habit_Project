import sqlite3

def print_table_data(db, table):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Query to fetch all rows from the specified table
        query = f"SELECT * FROM {table}"
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Fetch column names
        column_names = [description[0] for description in cursor.description]

        # Print column names as table headers
        print(f"Table: {table}")
        print("-" * 120)
        print(" | ".join(column_names))
        print("-" * 120)

        # Print rows
        for row in rows:
            print(" | ".join(map(str, row)))

    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

print_table_data('main.db', 'habit')