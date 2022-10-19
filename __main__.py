"""
The Fire CLI code as well as the commands that the users type to get around the CLI
"""

from modules.habit_manager import create_habit, delete_habit, mark_done
from modules.habit_analysis import show_habits, show_longest
from modules.predef_habits import predefined_habits

# Rich modules to display formatted data in a table
from rich.console import Console
from rich.table import Table

# The python fire package to work with the CLI
import fire

# Initialize a default rich console
console = Console()

# Function to view the applications functionality
def app_help():
    """
    View the details of each function and it's parameters
    """
    print(
        f"\nTo use this application, enter one of these functions after the name of this file in \"quotations\" followed by the OPTIONAL parameters.\nIf you leave out the parameters, you will be prompted to enter the required values manually.")
    console.print("""
    "create habit"
        Create and start tracking a new habit

        PARAMETERS:
            --name="NAME"                   | Create a habit with this name,
            --period="PERIOD"               | Create a habit with this periodicity
    """)
    console.print("""
    "delete habit"
        Delete one of your habits from the database

        PARAMETERS:
            --name="NAME"                   | Delete this habit from the database
        """)
    console.print("""
    "mark done"
        Mark one of your habits as done

        PARAMETERS:
            --name="NAME"                   | Mark this habit as done for its period
        """)
    console.print("""
    "show habits"
        View all currently tracked habits

        PARAMETERS:
            --period="PERIOD"               | View only the habits that have this periodicity
        """)
    console.print("""
    "longest streak"
        View the longest streak of all currently tracked habits

        PARAMETERS:
            --name="NAME"               | View the longest streak for only this habit
        """)

# Function to view all the predefined habits
def view_predefined_habits():
    """
    View some predefined habits to see what an active habit tracker will look like
    """
    table = Table(show_lines=True)
    table.add_column("Name", justify="center", vertical="middle")
    table.add_column("Repeat once every", justify="center", vertical="middle")
    table.add_column("Started on", justify="center", vertical="middle")
    table.add_column("Last checked on", justify="center", vertical="middle")
    table.add_column("Longest streak", justify="center", vertical="middle")
    table.add_column("Current streak", justify="center", vertical="middle")
    for habit in predefined_habits:
        table.add_row(
            str(habit.name),
            str(habit.period),
            str(habit.started_on),
            str(habit.last_checked_on),
            str(habit.streak_longest),
            str(habit.streak_current)
        )

    console.print("\nThis is what an active habit tracker would look like.\n")
    console.print(table)


if __name__ == "__main__":
    fire.Fire({
        "help": app_help,
        "create habit": create_habit,
        "delete habit": delete_habit,
        "show habits": show_habits,
        "longest streak": show_longest,
        "view predef habits": view_predefined_habits,
        "mark done": mark_done
    })
