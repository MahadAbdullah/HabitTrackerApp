"""
The module containing analysis and habit viewing functions
"""

# Database module to store habits in
import modules.database as database

from modules.habit_class import Habit

# Rich table module to easily render tables
from rich.table import Table

# Rich console module to display tables and other things with styling
from rich.console import Console

# Instantiate a default rich console
console = Console()


def make_class(arr: list):
    """
    Convert the provided list to a habit class

    ...

    Parameter
    ---
    arr: list
        The habit class, currently in an iterable format, containing the
        data in the following order:

        arr[0] -> name,
        arr[1] -> period,
        arr[2] -> started_on,
        arr[3] -> last_checked_on,
        arr[4] -> longest_streak,
        arr[5] -> current_streak
    
    Usage
    ---
    Since you can't store classes in the database directly, everything gets
    converted to a string. Therefore, the database returns each habit as a
    tuple and since we know what each element is, we can use those to convert
    that tuple to a habit class with this function.
    """
    return Habit(arr[0], arr[1], arr[2], arr[3],
                 arr[4], arr[5])


all_habits = []

# Convert each habit returned by the database.get_habits() function to a habit class using the map function
all_habits.extend(map(make_class, database.get_habits()))

# Setup the table with all the fields
# Data is added to this table when the user calls
habits_table = Table(show_lines=True)
habits_table.add_column("Name", justify="center", vertical="middle")
habits_table.add_column("Repeat once every",
                        justify="center", vertical="middle")
habits_table.add_column("Started on", justify="center", vertical="middle")
habits_table.add_column("Last checked on", justify="center", vertical="middle")
habits_table.add_column("Longest streak", justify="center", vertical="middle")
habits_table.add_column("Current streak", justify="center", vertical="middle")


def show(arr: list, iter: int = 0):
    """
    Recursively loop through a list of all the user habit classes and add each habit to the table.
    Print the table to the console after looping through all the habits.

    ...

    Parameter
    ---
    arr: list
        The list containing habit classes to loop through
    """

    if iter == len(arr):
        # Print the table after going through all habits
        console.print(habits_table)
        return
    else:
        habits_table.add_row(
            str(arr[iter].name),
            str(arr[iter].period),
            str(arr[iter].started_on),
            str(arr[iter].last_checked_on),
            str(arr[iter].streak_longest),
            str(arr[iter].streak_current)
        )
        iter += 1
        show(arr, iter)


def show_habits(period: str = ""):
    """
    View all currently tracked habits

    ...

    Parameter
    ---
    period: str, optional
      View only habits that have this periodicity
    """

    # Check if the user has any habits at all
    if len(all_habits) == 0:
        console.print(
            "\nYou have no habits to view, get started by typing \"create habit\" to create and start tracking a new habit\n")
    else:

        # If they do, check if they provided a period
        if period:

            # If they did, check if this period is valid
            if period in ['day', 'week', 'month']:

                # If it is, check if user has any habits with this periodicity
                if len(database.get_habits(period)) == 0:

                    # Display this information stating that they don't
                    # have any habits with this periodicity
                    console.print(
                        f"\nYou have no habits that repeat once every {period}\n")
                    return
                else:

                    # If they do, retrieve all the habits with this
                    # periodicity from the database and add them to the
                    # specific_habits list after converting each one to
                    # a class
                    specific_habits = []
                    specific_habits.extend(
                        map(make_class, database.get_habits(period)))
                    console.print(
                        f"\nYou have {len(specific_habits)} habits that repeat once every {period}\n")

                    # Display this specific_habits list
                    show(specific_habits)
            else:
                # If the period provided is not day/week/month
                console.print(f"\n\"{period}\" is not a valid period.\n")
        else:

            # If the user did not provide a specific periodicity, print
            # all the currently tracked habits
            console.print(
                f"\nYou currently have {len(all_habits)} tracked habits\n")

            show(all_habits)


def find_habit_longest(name: str, iter: int = 0):
    """
    Recursively loop through all habits and find the longest streak for the given habit

    ...

    Parameter
    name: str
        The name of the habit to be found
    """

    # Found variable indicating whether a habit with this name
    # even exists in the database or not
    found = False
    if iter == len(all_habits):

        # If no habit with this name was found in all the habits at the
        # end of the loop, display this information
        if not found:
            console.print(f"\nYou do not have a habit called \"{name}\"\n")
        return
    else:

        # If a habit with this name is found in all the habits
        if name == all_habits[iter].name:

            # Set the found variable to True and display this
            # information
            found = True
            console.print(
                f"\nThe longest streak for your \"{name}\" habit is {all_habits[iter].streak_longest}\n")
            return
        iter += 1
        find_habit_longest(name, iter)


# Set up the table to display all the habits longest streaks
longest_table = Table(show_lines=True)
longest_table.add_column("Name", justify="center", vertical="middle")
longest_table.add_column("Longest Streak", justify="center", vertical="middle")


def show_all_habits_longest(iter: int = 0):
    """
    Recursively loop through all the habits and find each habits longest streak and add it to the table.
    Print the table to the console when finished looping.
    """

    if iter == len(all_habits):

        # Print the table when finished
        console.print(longest_table)
        return
    else:
        longest_table.add_row(str(all_habits[iter].name), str(
            all_habits[iter].streak_longest))
        iter += 1
        show_all_habits_longest(iter)


def show_longest(name: str = ""):
    """
    View the longest streak of all habits

    ...

    Parameters
    ---
    name: str
        The name of the habit you want to see the longest streak of
    """
    if name:
        find_habit_longest(name)
    else:
        show_all_habits_longest()

