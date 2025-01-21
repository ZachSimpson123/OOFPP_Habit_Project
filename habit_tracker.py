import sqlite3
from datetime import datetime, timedelta
import json



class Habit:

    """
    A class representing a habit, including its attributes and associated database operations.

    Attributes:
        _DB_NAME (str): The name of the SQLite database file.
        name (str): The name of the habit.
        description (str): A description of the habit.
        period (str): The frequency of the habit (e.g., "Daily" or "Weekly").
        date_and_time_of_creation (str): The creation timestamp of the habit.
        completed_dates (list): A list of dates when the habit was marked as complete.
        longest_streak (int): The longest streak of consecutive completions.
        current_streak (int): The current streak of consecutive completions.
    """

    _DB_NAME ='main.db' # Database file name

    def __init__(self,name = None, description=None, completed_dates=None, period = None, date_and_time_of_creation = None, longest_streak = None, current_streak = None):
        """
                Initialize a new Habit instance.

                Args:
                    name (str, optional): The name of the habit.
                    description (str, optional): A description of the habit.
                    completed_dates (list, optional): Dates the habit was completed.
                    period (str, optional): The frequency of the habit.
                    date_and_time_of_creation (str, optional): Timestamp of habit creation.
                    longest_streak (int, optional): The longest streak.
                    current_streak (int, optional): The current streak.
                """
        self.name = name
        self.description = description
        self.period = period
        self.date_and_time_of_creation = date_and_time_of_creation
        self.completed_dates = completed_dates if completed_dates is not None else []
        self.longest_streak = longest_streak
        self.current_streak = current_streak

    def save_weekly(self):
        """
        Save the habit as a weekly habit to the database.
        """
        period = "Weekly"
        cur_datetime = datetime.now().replace(second=0, microsecond=0)
        with sqlite3.connect(self._DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO habit (name, description, 'date_and_time_of_creation', period) VALUES (?,?,?,?) ''',
                (self.name, self.description, cur_datetime, period))
            conn.commit()

    def save_daily(self):
        """
        Save the habit as a daily habit to the database.
        """
        period = "Daily"
        cur_datetime = datetime.now().replace(second=0,microsecond=0)
        with sqlite3.connect(self._DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO habit (name, description, 'date_and_time_of_creation', period) VALUES (?,?,?,?) ''', (self.name, self.description, cur_datetime, period))
            conn.commit()


    def update(self, new_name, description, name):
        """
        Update the name and description of a habit.

        Args:
            new_name (str): The new name of the habit.
            description (str): The updated description.
            name (str): The current name of the habit.
        """
        with sqlite3.connect(self._DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE habit SET name = ?, description = ? WHERE name = ?''', (new_name, description,name))
            conn.commit()

    def delete(self):
        """
        Delete a habit from the database
        """
        with sqlite3.connect(self._DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM habit WHERE name = ?
            """, (self.name,))
            conn.commit()

    @classmethod
    def load_one(cls, name):
        """
        Retrieve a habit by its name along with its tracking data.

        Args:
            name (str): The name of the habit to load.

        Returns:
            Habit or None: The Habit instance if found, else None.
        """
        with sqlite3.connect(cls._DB_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT name, description,date_and_time_of_creation,period, completed_dates  FROM habit WHERE name = ?      
                """, (name,))
            result = cursor.fetchone()
            if not result:
                return None

            habit = cls(name=result[0], description=result[1], date_and_time_of_creation =result[2], period = result[3], completed_dates=result[4])
            return habit


    @classmethod
    def load_by_name(cls, name):
        """
        Load a habit by its name and return a Habit instance.

        Args:
            name (str): The name of the habit to load.

        Returns:
            Habit or None: The Habit instance if found, else None.
        """
        with sqlite3.connect(cls._DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, completed_dates, period FROM habit WHERE name = ?", (name,))
            result = cursor.fetchone()
            if not result: # If no result is found, return None
                return None
            habit = cls(name=result[0], completed_dates=result[1], period = result[2])
            return habit


    @classmethod
    def load_list(cls, period):
        """
        Load a list of habits filtered by their period (e.g., "Daily" or "Weekly").

        Args:
            period (str): The period to filter habits by.

        Returns:
            tuple: A tuple containing a list of column names and a list of rows with habit data.
        """
        with sqlite3.connect(cls._DB_NAME) as conn:
            cursor = conn.cursor()
        cursor.execute("""SELECT name, description, Date_and_Time_of_Creation, period, completed_dates FROM habit WHERE period = ? """, (period,))
        rows = cursor.fetchall() # Fetch all matching rows
        column_names = [description[0] for description in cursor.description]
        return column_names, rows

    @classmethod
    def load_whole_list(cls):
        """
        Load all habits from the database.

        Returns:
            tuple: A tuple containing a list of column names and a list of rows with all habit data.
        """
        with sqlite3.connect(cls._DB_NAME) as conn:
            cursor = conn.cursor()
        cursor.execute("""SELECT name, description, Date_and_Time_of_Creation, period, completed_dates FROM habit""")
        rows = cursor.fetchall() # Fetch all rows
        column_names = [description[0] for description in cursor.description]
        return column_names, rows

    @classmethod
    def load_completed_dates(cls, name, period):
        """
        Load the list of completed dates for a habit.

        Args:
            name (str): The name of the habit.
            period (str): The period of the habit.

        Returns:
            list: A list of completed dates.
        """
        with sqlite3.connect(cls._DB_NAME) as conn:
            cursor = conn.cursor()
        cursor.execute("""SELECT completed_dates FROM habit WHERE name = ? AND period = ?""", (name,period))
        result = cursor.fetchone()  # Fetch the result
        if result:  # If a result is found, parse the JSON string into a list
            completed_dates = json.loads(result[0]) # Extract the first element of the tuple
        else:
            completed_dates = []    # Return an empty list if no data is found
        return completed_dates

    @classmethod
    def load_streaks(cls, name, period):
        """
        Load the current and longest streaks for a habit.

        Args:
            name (str): The name of the habit.
            period (str): The period of the habit.

        Returns:
            tuple: A tuple containing the habit name, current streak, and longest streak.
        """
        with sqlite3.connect(cls._DB_NAME) as conn:
            cursor = conn.cursor()
        cursor.execute("""SELECT name, current_streak, longest_streak FROM habit WHERE name = ? AND period = ?""", (name, period))
        habit = cursor.fetchone() # Fetch the streak data
        return habit

    @classmethod
    def load_longest_streak(cls):
        """
        Load the habit with the longest streak.

        Returns:
            tuple: A tuple containing the longest streak and the name of the habit.
        """
        with sqlite3.connect(cls._DB_NAME) as conn:
            cursor = conn.cursor()
        cursor.execute("""SELECT longest_streak,name FROM habit ORDER BY longest_streak DESC LIMIT 1""")
        habit = cursor.fetchone()  # Fetch the habit with the longest streak
        return habit

    @classmethod
    def update_streaks(cls, current_streak, longest_streak, name):
        """
        Update the current and longest streaks for a habit.

        Args:
            current_streak (int): The current streak count.
            longest_streak (int): The longest streak count.
            name (str): The name of the habit.
        """
        with sqlite3.connect(cls._DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE habit SET current_streak = ?, longest_streak = ? WHERE name = ?''', (current_streak,longest_streak,name))
            conn.commit()

    def mark_complete(self, date=None):
        """
        Mark a habit as completed on a given date.

        Args:
            date (str, optional): The date to mark the habit as completed. Defaults to today's date.
        """
        if date is None:    # Default to today's date if no date is provided
            date = str(datetime.today().date())

        if self.completed_dates is None:    # Initialize completed dates if not set
                self.completed_dates = []

        if isinstance(self.completed_dates, str):   # Parse the string into a list if needed
                    self.completed_dates = json.loads(self.completed_dates)

                    # Avoid duplicate entries
        if date not in self.completed_dates:

                    self.completed_dates.append(date)

                    # Update the database
                    with sqlite3.connect(self._DB_NAME) as conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE habit SET completed_dates = ? WHERE name = ?",
                            (json.dumps(self.completed_dates), self.name),   # Store as a JSON string
                        )
                        conn.commit()

    @classmethod
    def compute_streak(cls,completed_dates, name, number):
        """
        Compute the current and longest streaks for a habit based on completed dates.

        Args:
            completed_dates (list): A list of completed dates.
            name (str): The name of the habit.
            number (int): The interval (in days) defining a streak.

        Updates:
            The current and longest streaks are updated in the database.
        """
        sorted_dates = sorted(completed_dates)   # Sort dates chronologically
        print(sorted_dates)
        longest_streak = 1
        current_streak = 1
        for i in range(1, len(sorted_dates)):
            if (datetime.strptime(sorted_dates[i], "%Y-%m-%d") -
                    datetime.strptime(sorted_dates[i - 1], "%Y-%m-%d") == timedelta(days=number)):
                current_streak += 1  # Increment current streak if dates are consecutive
                longest_streak = max(longest_streak, current_streak) # Update longest streak
            else:
                current_streak = 1 # Reset current streak
        Habit.update_streaks(current_streak, longest_streak, name)  # Update database
        return current_streak , longest_streak

def print_tables(column_names, rows):
    """
    Print a formatted table of habits.

    Args:
        column_names (list): The column names of the table.
        rows (list): The rows of data to display.

    Prints:
        A formatted table of the provided column names and rows.
    """
    if not rows:   # Check if rows are empty
        print('No habits found')
        return
    print("Table: Habits")
    print("-"* 120)
    print(' | '.join(column_names))  # Print column headers
    print("-"* 120)
    for row in rows:   # Iterate through rows and print data
        print(" | ".join(map(str,row)))
    print('-'* 120)