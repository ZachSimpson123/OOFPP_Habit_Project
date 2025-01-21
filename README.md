# My Habit Tracking App
## What is it?

This Habit Tracking App is a command-line application designed to help users create, track, and manage their habits. Users can create Daily and Weekly habits and perform several actions such as:

* Marking habits as complete (check-off).
* Viewing current streaks and longest streaks for habits.
* Retrieving a list of all created habits.
* Editing or deleting habits.

The app uses SQLite3 to store and manage habit data, ensuring persistence across sessions.
### 'main.py'
This file serves as the entry point of the application. It contains the main menu implemented as a Command Line Interface (CLI), which guides the user through various options. Additional non-class-related utility functions are also stored here.

### 'habit_tracker.py'
This file defines the Habit class and its methods. It encapsulates the core functionality for habit creation, modification, tracking, and analysis.

### 'db.py'
This file handles database setup. It initializes the SQLite3 database and creates the required table structure to store habit data.

### 'requirements.txt' 
Lists the dependencies for the app. The main dependencies are:

* #### questionary: For creating an interactive CLI.
* #### pytest: For running tests to ensure the application works correctly.

### 'test_project.py'
Contains tests for the core functionality of the application. It ensures the app performs as expected and helps catch potential bugs.

## Installation

```shell
pip install -r requirements.txt
```
## Usage
Initialize the database
```shell
python db.py
```

Start:
```shell
python main.py
```
And then follow the instructions that appear.

## View Database
Quickly view the habit database and its contents

```shell
python view.py
```

## Tests

```shell
pytest
```
## Re-set Database
if you would like to re-set the database.
#### Note: You will lose all habit data
```shell
python re-set.py
```


### Thank you for using our app!