"""
The module used to store user habits to a database
"""

# SQLite 3 module to work with a database
import sqlite3

# Rich console to print out strings with styles
from rich.console import Console

# Instantiate a default rich console
console = Console()

# 'With' is used to close the connection after doing an action
with sqlite3.connect('habits.db') as connection:
    cursor = connection.cursor()

    # If table doesn't exist make it. if it does, move on.
    try:
        cursor.execute(
            "CREATE TABLE habits (name text, period text, started_on text, last_checked_on text, streak_longest integer, streak_current integer)")
        connection.commit()
    except:
        pass

    # This string contains all the user habits with an index number
    # Which is used wherever the user has to select one of their habits
    indexed_habits = ""

    # This list is neccessary to restrict the user choices to 
    # only their tracked habits wherever applicable
    habit_ids = []

    def get_habits(period: str = "") -> list:
        """
        Returns a list of user habits matching the arguments passed that are
        currently in the database sorted by descending order of longest streak.
        If no arguments are passed, then it returns all user habits

        ...

        Parameter
        ---
        period: str, optional
            Return only a list of habits that have this periodicity
        """
        if period:
            cursor.execute(f"""
            SELECT * 
            FROM habits
            WHERE period="{period}"
            ORDER BY streak_longest DESC
            """)
        else:
            cursor.execute("SELECT * FROM habits ORDER BY streak_longest DESC")

        return cursor.fetchall()

    for index, habit in enumerate(get_habits()):
        # Populate the list and string with the current user habits
        # easily
        # using a loop and the enumerate function
        indexed_habits += f"[{index}] {habit[0]}\n"
        habit_ids.append(str(index))

    def add(habit_cls: object):
        """
        Add a habit class instance to the database habits table

        ...

        Parameter
        ---
        habit_cls: Habit
            The habit class to be added to the database
        """
        try:
            cursor.execute(f"""
            INSERT INTO habits
            VALUES (
            "{habit_cls.name}",
            "{habit_cls.period}",
            "{habit_cls.started_on}",
            "{habit_cls.last_checked_on}",
            "{habit_cls.streak_longest}",
            "{habit_cls.streak_current}"
            )
            """)
            connection.commit()

            return 'added'
        except Exception as e:
            return e

    def delete(habit_cls: object):
        """
        Delete a habit class from the database habits table

        ...

        Parameter
        ---
        habit_cls: Habit
            The habit class to be removed from the database
        """
        try:
            cursor.execute(f"""
            DELETE FROM habits
            WHERE name="{habit_cls.name}"
            """)
            connection.commit()
            return 'deleted'
        except Exception as e:
            return e

    def update(habit_cls: object):
        """
        Update the values of a habit class in the database habits table

        ...

        Parameter
        ---
        habit_cls: Habit
            The habit class to be updated in the database
        """
        try:
            cursor.execute(f"""
            UPDATE habits
            SET 
                last_checked_on = "{habit_cls.last_checked_on}",
                streak_current = "{habit_cls.streak_current}",
                streak_longest = "{habit_cls.streak_longest}"
            WHERE name = "{habit_cls.name}"
            """)
            connection.commit()
            return 'updated'
        except Exception as e:
            return e

