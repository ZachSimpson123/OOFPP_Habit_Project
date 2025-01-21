import unittest
import sqlite3
from datetime import datetime
from habit_tracker import Habit
import json
from main import create_habit
from unittest.mock import patch


class TestHabit(unittest.TestCase):
    """
    Test cases for the Habit class methods to ensure the functionality of habit tracking and database operations.
    """
    def setUp(self):
        """
        Set up the test database and create Habit instances before each test.
        """
        # Create a test database
        self.test_db = 'test_db'
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS habit (
                                name TEXT PRIMARY KEY,
                                description TEXT NOT NULL,
                                Date_and_Time_of_Creation DATETIME,
                                period TEXT,
                                completed_dates TEXT,
                                current_streak INT,
                                longest_streak INT
                                )
                            """)
            conn.commit()

        # Create a Habit instances for testing
        self.habit = Habit()
        self.habit1 = Habit(name="Weekly Habit",description="A weekly test habit for unit testing", period = 'Weekly', completed_dates=0 )
        self.habit2 = Habit(name = 'Daily Habit',description = 'A daily test habit for unit testing',period ='Daily', completed_dates= 0 )
        self.habit3 = Habit(name ='Daily Streak Habit', description = 'Test habit for computing the streak for a daily habit', period = 'Daily', completed_dates = '["2023-1-01","2023-1-02","2023-1-03","2023-1-04","2023-1-05","2023-1-06","2023-1-07","2023-1-08","2023-1-09","2023-1-10","2023-1-11","2023-1-12","2023-1-13","2023-1-14","2023-1-15","2023-1-16","2023-1-18","2023-1-19","2023-1-20","2023-1-21","2023-1-22","2023-1-23","2023-1-24","2023-1-25","2023-1-26","2023-1-27","2023-1-28","2023-1-29"]',current_streak = None, longest_streak =None)
        self.habit4 = Habit(name ='Weekly Streak Habit', description ='Test habit for computing the streak for a daily habit', period = 'Weekly',completed_dates=  '["2023-1-01","2023-1-08","2023-1-15","2023-1-22","2023-2-04","2023-2-11"]', current_streak= None, longest_streak= None)
        self.habit5 = Habit(name ='Habit Marked Complete', description ='Habit to be marked complete', period ='Weekly', completed_dates= '[]' )
        self.habit._DB_NAME = self.test_db   # Point the instance to the test database
        self.habit1._DB_NAME = self.test_db  # Point the instance to the test database
        self.habit2._DB_NAME = self.test_db  # Point the instance to the test database
        self.habit3._DB_NAME = self.test_db  # Point the instance to the test database
        self.habit4._DB_NAME = self.test_db  # Point the instance to the test database
        self.habit5._DB_NAME = self.test_db  # Point the instance to the test database


    def test_save_weekly(self):

        """
        Test saving a weekly habit into the database.
        """
        self.habit1.save_weekly()

        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM habit WHERE name = ?", (self.habit1.name,))
            result = cursor.fetchone()

        self.assertIsNotNone(result, "The habit was not saved to the database.")
        self.assertEqual(result[0], "Weekly Habit", "The habit name is incorrect.")
        self.assertEqual(result[1], "A weekly test habit for unit testing", "The habit description is incorrect.")
        self.assertEqual(result[3], "Weekly", "The habit period is incorrect.")

    def test_save_daily(self):
        """
        Test saving a daily habit into the database.
        """
        self.habit2.save_daily()

        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM habit WHERE name = ?", (self.habit2.name,))
            result = cursor.fetchone()

        self.assertIsNotNone(result, "The habit was not saved to the database.")
        self.assertEqual(result[0], "Daily Habit", "The habit name is incorrect.")
        self.assertEqual(result[1], "A daily test habit for unit testing", "The habit description is incorrect.")
        self.assertEqual(result[3], "Daily", "The habit period is incorrect.")

    def test_update(self):
        """
        Test updating an existing habit in the database.
        """
        # Step 1: Insert a habit into the database
        self.habit1.save_weekly()

        # Step 2: Update the habit
        self.habit1.update(new_name="Updated Weekly Habit", description="Updated Weekly description", name= 'Weekly Habit')


        # Step 3: Verify the update
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM habit WHERE name = ?", ('Updated Weekly Habit',))
            result = cursor.fetchone()

        # Assertions
        self.assertIsNotNone(result, "The habit was not updated in the database.")
        self.assertEqual(result[0], "Updated Weekly Habit", "The habit name was not updated correctly.")
        self.assertEqual(result[1], "Updated Weekly description", "The habit description was not updated correctly.")


    def test_delete(self):
        """
        Test deleting a habit from the database.
        """
        # Step 1: Insert a habit into the database
        self.habit1.save_weekly()

        # Step 2: Update the habit
        self.habit1.delete()

        # Step 3: Verify the habit is deleted
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM habit WHERE name = ?", (self.habit1.name,))
            result = cursor.fetchone()

        # Assertions
        self.assertIsNone(result, "The habit was not deleted from the database.")

    def test_mark_complete_default_date(self):
        """
        Test marking a habit as complete with the default date.
        """
        #Insert a habit into the database
        self.habit5.save_weekly()

        # Mark the habit as complete with the default date
        self.habit5.mark_complete()

        # Verify that the habit was updated in the database
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT completed_dates FROM habit WHERE name = ?", (self.habit5.name,))
            result = cursor.fetchone()
            completed_dates = json.loads(result[0])

        # Assert that the default date is in the completed_dates list
        self.assertIn(str(datetime.today().date()), completed_dates,
                      "The default date was not added to completed_dates.")



    @patch('questionary.text')
    @patch('questionary.select')
    @patch.object(Habit, 'save_weekly')
    def test_create_habit(self, mock_save_weekly, mock_select, mock_text):

        """
        Test creating a habit through the user interface (using mocks).
        """

        # Mock the `ask` method for select and text
        mock_select.return_value.ask.return_value = "Weekly"  # Simulate selecting "Weekly"
        mock_text.return_value.ask.side_effect = ["Test Habit", "A test description"]  # Simulate text inputs

        # Mock the main_menu function to prevent it from being called
        with patch('main.main_menu') as mock_main_menu:
            # Call the function
            create_habit()

            # Verify `questionary.select` was called with correct arguments
            mock_select.assert_called_once_with(
                "Weekly or Daily Habit:",
                choices=["Weekly", "Daily"]
            )
            # Verify `questionary.text` was called for name and description
            mock_text.assert_any_call("Enter the habit name:")
            mock_text.assert_any_call("Enter the habit description:")

            # Verify `save_weekly` was called
            mock_save_weekly.assert_called_once()

            # Verify `main_menu` was called
            mock_main_menu.assert_called_once()


    def test_compute_daily_streak(self):
        """
        Test computing the daily streak for a habit.
        """

        period = "Daily"
        cur_datetime = datetime.now().replace(second=0, microsecond=0).isoformat()
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO habit (name, description, 'date_and_time_of_creation', period, completed_dates) VALUES (?,?,?,?,?) ''',
                (self.habit3.name, self.habit3.description, cur_datetime, period, self.habit3.completed_dates))
            conn.commit()

        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
        cursor.execute("""SELECT completed_dates FROM habit WHERE name = ? AND period = ?""", (self.habit3.name,self.habit3.period))
        result = cursor.fetchone()
        if result:
            completed_dates = json.loads(result[0]) # Extract the first element of the tuple
        else:
            completed_dates = []
        number = 1

        self.habit3.compute_streak(completed_dates, self.habit3.name, number)
        current_streak, longest_streak = self.habit3.compute_streak(completed_dates, self.habit3.name, number)

        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE habit SET current_streak = ?, longest_streak = ? WHERE name = ?''', (current_streak,longest_streak,self.habit3.name))
            conn.commit()

        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT current_streak, longest_streak FROM habit WHERE name = ?", (self.habit3.name,))
            result = cursor.fetchone()


        self.assertIsNotNone(result, "Streak values were not found in the database.")
        self.assertEqual(result[0], 12, "The current streak was not calculated correctly.")
        self.assertEqual(result[1], 16, "The longest streak was not calculated correctly.")

    def test_compute_weekly_streak(self):
        """
        Test computing the weekly streak for a habit.
        """
        period = "Weekly"
        cur_datetime = datetime.now().replace(second=0, microsecond=0).isoformat()
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO habit (name, description, 'date_and_time_of_creation', period, completed_dates) VALUES (?,?,?,?,?) ''',
                (self.habit4.name, self.habit4.description, cur_datetime, period, self.habit4.completed_dates))
            conn.commit()

        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
        cursor.execute("""SELECT completed_dates FROM habit WHERE name = ? AND period = ?""", (self.habit4.name,self.habit4.period))
        result = cursor.fetchone()
        if result:
            completed_dates = json.loads(result[0]) # Extract the first element of the tuple
        else:
            completed_dates = []
        number = 7

        self.habit4.compute_streak(completed_dates, self.habit4.name, number)
        current_streak, longest_streak = self.habit4.compute_streak(completed_dates, self.habit4.name, number)

        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE habit SET current_streak = ?, longest_streak = ? WHERE name = ?''', (current_streak,longest_streak,self.habit4.name))
            conn.commit()

        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT current_streak, longest_streak FROM habit WHERE name = ?", (self.habit4.name,))
            result = cursor.fetchone()


        self.assertIsNotNone(result, "Streak values were not found in the database.")
        self.assertEqual(result[0], 2, "The current streak was not calculated correctly.")
        self.assertEqual(result[1], 4, "The longest streak was not calculated correctly.")

    def tearDown(self):

        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute('DROP TABLE IF EXISTS habit')
        self.habit1 = None
        self.habit2 = None
        self.habit3 = None
        self.habit4 = None
        self.habit5 = None