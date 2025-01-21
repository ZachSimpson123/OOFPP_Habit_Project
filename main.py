import questionary
from habit_tracker import Habit, print_tables
import json

"""
Habit Tracker Command-Line Interface

This script provides an interactive command-line interface for managing habits, including creating, editing, deleting, checking off habits, and analyzing habit performance.

Modules:
    - questionary: Used for interactive command-line prompts.
    - habit_tracker: Custom module containing the Habit class and utility functions.

Functions:
    - main_menu(): Display the main menu and handle user actions.
    - create_habit(): Create a new habit and save it as either weekly or daily.
    - edit_habit(): Edit the name or description of an existing habit.
    - delete_habit(): Delete a habit from the database after user confirmation.
    - check_off_daily(): Mark a daily habit as completed and update its streaks.
    - check_off_weekly(): Mark a weekly habit as completed and update its streaks.
    - analyze_habit(): Analyze habits by viewing details, lists, or streak information.

Entry Point:
    The script starts execution with the `main_menu()` function.
"""

def main_menu():
    # Display the main menu and prompt the user to select an action
    choice = questionary.select(
       "Choose an action:",
        choices = ["Create Habit",
                   "Edit Habit",
                   "Delete Habit",
                   "Check-off Daily Habit",
                   "Check-off Weekly Habit",
                   "Analyze Habit",
                   "Exit"]
    ).ask()

    # Call appropriate function based on user selection
    if choice == "Create Habit":
        create_habit()
    elif choice == "Edit Habit":
        edit_habit()
    elif choice == "Delete Habit":
        delete_habit()
    elif choice == "Check-off Daily Habit":
        check_off_daily()
    elif choice == "Check-off Weekly Habit":
        check_off_weekly()
    elif choice == "Analyze Habit":
        analyze_habit()
    elif choice == "Exit":
        exit()


def create_habit():
    # Prompt the user to select the type of habit (weekly or daily)
    choice = questionary.select("Weekly or Daily Habit:",
                              choices= ["Weekly",
                                        "Daily"]
                                ).ask()
    if choice == "Weekly":
        # Gather habit details for a weekly habit
        name = (questionary.text("Enter the habit name:").ask()).strip().title()
        description = questionary.text("Enter the habit description:").ask()
        # Create a new Habit object and save it as weekly
        habit = Habit(name=name, description=description)

        habit.save_weekly()
        print("Habit saved successfully")
        main_menu()

    elif choice == "Daily":
        # Gather habit details for a daily habit
        name = (questionary.text("Enter the habit name:").ask()).strip().title()
        description = questionary.text("Enter the habit description:").ask()
        # Create a new Habit object and save it as daily
        habit = Habit(name=name, description=description)
        habit.save_daily()
        print("Habit saved successfully")
        main_menu()

def edit_habit():
    # Prompt the user for the name of the habit to edit
    name = questionary.text("Enter the name of the Habit to edit:").ask().strip().title()
    habit = Habit.load_one(name)

    # Check if the habit exists; if not, return to the main menu
    if not habit:
        print("Habit not found!:")
        main_menu()
        return

    # Prompt the user for new name and description
    new_name = questionary.text(f'Enter the new name(current:{habit.name}):').ask()
    description = questionary.text(f'Enter the new description (current: {habit.description})').ask()

    # Update the habit details
    habit.name = name
    habit.description = description
    habit.update(new_name, description, name)
    print("Habit updated sucessfully")
    main_menu()


def delete_habit():
    # Prompt the user for the name of the habit to delete
    name = questionary.text ("Enter the name of the habit you want to delete:").ask().strip().title()
    habit = Habit.load_one(name)

    # Check if the habit exists; if not, return to the main menu
    if not habit:
        print("Habit not found!")
        main_menu()
        return

    # Confirm the deletion with the user
    confirmation = questionary.confirm(f"Are you sure you want to delete habit '{habit.name}'?").ask()
    if confirmation:
        #Assuming a delete method in the habit class
        habit.delete()
        print("Habit deleted successfully")
    main_menu()


def check_off_daily():
    # Prompt the user for the name of the daily habit to check off
    name = questionary.text("Enter the daily habit name that you would like to check off:").ask().strip().title()
    habit = Habit.load_by_name(name)
    if not habit:
        print("Habit not found!")
        main_menu()
        return

    # Mark the habit as complete and compute the streak
    habit.mark_complete()
    period = 'Daily'
    completed_dates = Habit.load_completed_dates(name, period)

    # Check if completed dates exist for the habit
    if not completed_dates:
        print("Habit not found!  Make sure the habit name is spelt correctly and that you have the correct habit period.")
        main_menu()

    habit.compute_streak(completed_dates, name, number=1)

    print('Habit Checked off successfully')
    main_menu()

def check_off_weekly():
    # Prompt the user for the name of the weekly habit to check off
    name = questionary.text("Enter the weekly habit name that you would like to check off:").ask().strip().title()
    habit = Habit.load_by_name(name)
    if not habit:
        print("Habit not found!")
        main_menu()
        return
    # Mark the habit as complete and compute the streak
    habit.mark_complete()
    period = 'Weekly'
    completed_dates = Habit.load_completed_dates(name, period)

    # Check if completed dates exist for the habit
    if not completed_dates:
        print("Habit not found!  Make sure the habit name is spelt correctly and that you have the correct habit period.")
        main_menu()

    habit.compute_streak(completed_dates, name, number=7)
    print('Habit Checked off successfully')
    main_menu()


def analyze_habit():
    # Provide options to analyze habits
    choice = questionary.select(
        "Choose an action:",
        choices=["View Habit",
                 "View a list of all Habits",
                 "View a list of Habits according to the period",
                 "Get current and longest recorded streak for a daily habit",
                 "Get current and longest recorded streak for a weekly habit",
                 "My longest recorded streak on record"]
    ).ask()

    if choice == "View Habit":
        # View details of a specific habit
        name = questionary.text("Enter the name of the habit you want to View:").ask().strip().title()
        habit = Habit.load_one(name)

        if not habit:
            print("Habit not found!  Make sure the habit name is spelt correctly.")
            main_menu()
            return

        print(f'Habit: {habit.name}')
        print(f'Description: {habit.description}')
        print(f'Date and Time of Creation: {habit.date_and_time_of_creation}')
        print(f'Period: {habit.period }')
        print(f'Completed Dates: {habit.completed_dates}')

        main_menu()

    elif choice == "View a list of all Habits":
        # View details of a specific habit
        column_names, rows = Habit.load_whole_list()
        print_tables(column_names, rows)
        if not rows:
            main_menu()
        main_menu()

    elif choice == "View a list of Habits according to the period":
        # Display habits filtered by their period (weekly or daily)
        choice = questionary.select(
            "Choose an action:",
            choices=["Weekly",
                     "Daily"]
        ).ask()

        if choice == "Weekly":
            column_names, rows = Habit.load_list('Weekly')
            print_tables(column_names, rows)
            if not rows:
                main_menu()
            main_menu()

        if choice =="Daily":
            column_names, rows = Habit.load_list('Daily')
            print_tables(column_names, rows)
            if not rows:
                main_menu()
            main_menu()


    elif choice == "Get current and longest recorded streak for a daily habit":
        # Get streak information for a daily habit
        name = questionary.text("Enter the name of the habit that you want to find a daily streaks for:").ask().strip().title()
        period = 'Daily'
        habit = Habit.load_streaks(name, period)
        if not habit:
            print("Habit not found!  Make sure the habit name is spelt correctly and that you have the correct habit period.")
            main_menu()
        _, current_streak, longest_streak = habit
        print(f'Longest Streak: {longest_streak}')
        print(f'Current Streak: {current_streak}')
        main_menu()

    elif choice == "Get current and longest recorded streak for a weekly habit":
        # Get streak information for a weekly habit
        name = questionary.text("Enter the name of the habit that you want to find a weekly streaks for:").ask().strip().title()
        period = 'Weekly'
        habit = Habit.load_streaks(name, period)
        if not habit:
            print("Habit not found!  Make sure the habit name is spelt correctly and that you have the correct habit period.")
            main_menu()
        _, current_streak, longest_streak = habit
        print(f'Longest Streak: {longest_streak}')
        print(f'Current Streak: {current_streak}')
        main_menu()

    elif choice == "My longest recorded streak on record":
        # Display the longest recorded streak across all habits
        habit = Habit.load_longest_streak()
        if habit:
            longest_streak, name = habit  # Unpack the tuple
            print(f"Your longest all-time streak is '{longest_streak}' for the habit '{name}'")
        else:
            print("No habit data found.")
        main_menu()


if __name__ == '__main__':
    # Start the program with the main menu
    main_menu()

