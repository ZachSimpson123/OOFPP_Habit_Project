import sqlite3


def get_db(name):
    """
    Connect to a SQLite database or create a new one if it doesn't exist.

    Args:
        name (str): The name of the database file.

    Returns:
        sqlite3.Connection: A connection object to interact with the SQLite database.
    """
    db = sqlite3.connect(name)
    return db

def create_table(db):
    """
    Create a table for storing habit tracking information if it doesn't already exist.

    Args:
        db (sqlite3.Connection): A connection object for the database.

    The table structure includes the following columns:
        - name (TEXT, PRIMARY KEY): The unique name of the habit.
        - description (TEXT, NOT NULL): A description of the habit.
        - date_and_time_of_creation (DATETIME): The timestamp when the habit was created.
        - period (TEXT): The frequency of the habit (e.g., daily, weekly).
        - completed_dates (TEXT): A string of dates when the habit was completed.
        - current_streak (INT): The current streak of the habit being maintained.
        - longest_streak (INT): The longest streak achieved for the habit.
        """
    cursor = db.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS habit (
                    name TEXT PRIMARY KEY,
                    description TEXT NOT NULL,
                    date_and_time_of_creation DATETIME,
                    period TEXT,
                    completed_dates TEXT,
                    current_streak INT,
                    longest_streak INT
                    )
                """)


    db.commit()




db = get_db('main.db')
create_table(db)