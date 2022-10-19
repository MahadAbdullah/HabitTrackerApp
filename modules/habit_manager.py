"""
The module that contains the code which the users indirectly interact with to manage their habits
i.e creating, deleting & updating habits in a clean and simple way
"""

# Rich prompts to have the user input only the allowed values
from rich.prompt import IntPrompt, Prompt

# Rich console to print things with styling
from rich.console import Console

from modules.habit_class import Habit
from modules.habit_analysis import all_habits
from modules.database import indexed_habits, habit_ids

# Instantiate a default rich console
console = Console()

# Variable to store the error message incase something goes wrong
error_message = ""


def validate_inputs(name: str, period: str) -> bool:
    """
    Make sure the inputs are valid to be entered into the database

    ...

    Parameters
    ---
    name: str
        The name to be validated
    period: str
        The period to be validated
    """

    # Make sure the error_message variable is the global one to access
    # it outside of this function
    global error_message

    # Check if a habit with this name already exists in the database
    # if it does, return false and set error message = already existing habit
    for habit in all_habits:
        if name == habit.name:
            error_message = f"\nYour habit was not created because you already have a habit called \"{habit.name}\".\n"
            return False

    # Check if the period is one of the 3 options [day/week/month]
    # if it isn't, return false and set error message = wrong period
    if period not in ["day", "week", "month"]:
        error_message = "\nPlease enter one of the following time periods:\n\n- day\n- week\n- month\n"
        return False

    return True


def init_habit(name: str, period: str):
    """
    If all inputs are valid, initialize a habit class with this data.
    Required to make sure all inputs are valid regardless of how the
    data was input.

    ...

    Parameters
    ---
    name: str
        The name of the habit to be created
    period: str
        The periodicity of the habit to be created
    """

    # Check if user provided inputs are valid and then instantiate a
    # new habit class with that data
    if validate_inputs(name, period) is True:
        habit = Habit(name, period)

        # Add this newly created habit class to the database
        habit.add_to_db()

        # Prompt the user to check this habit to show them how to mark
        # habits as complete in the future
        habit.prompt_to_check()

    # Otherwise print the error message that was set
    else:
        console.print(error_message, style="red")


def create_habit(name: str = "", period: str = ""):
    """
    Create and start tracking a new habit

    ...

    Parameters
    ---
    name : str
        The name you want to give this habit
    period : str
        How often you'd like to repeat this habit. i.e once every ___ [day/week/month]
    """

    # Seperate function so the user has the option of not providing
    # any values and be guided through the function automatically

    # If the user has not specified a habit name parameter
    try:
        if not name:
            console.print(
                '\nCreate a new habit from the following\n\n[1] walk the dog (daily)\n[2] exercise (daily)\n[3] laundry (weekly)\n[4] clean the house (weekly)\n[5] review budget & finances (monthly)\n------------\n[6] custom habit\n\nBy typing a number from 1 to 6\n')
            res = (IntPrompt.ask("Your response\n", choices=[
                '1', '2', '3', '4', '5', '6']))
            if res == 1:
                name = 'walk the dog'
                period = 'day'
            elif res == 2:
                name = 'exercise'
                period = 'day'
            elif res == 3:
                name = 'laundry'
                period = 'week'
            elif res == 4:
                name = 'clean the house'
                period = 'week'
            elif res == 5:
                name = 'review budget & finances'
                period = 'month'
            else:
                name = Prompt.ask(
                    "\nWhat would you like to do?\nEx. read a book, meditate, etc...\n").lower()

        # If the user has not specified a habit periodicity
        if not period:
            res = IntPrompt.ask(
                "\nHow often would you like to repeat this habit?\nOnce per ___\n\n[1] Day\n[2] Week\n[3] Month\n\n", choices=["1", "2", "3"])
            if res == 1:
                period = "day"
            elif res == 2:
                period = "week"
            else:
                period = "month"

        init_habit(name.lower(), period.lower())

    # If user presses CTRL + C during the function, exit immediately
    except KeyboardInterrupt:
        console.print(
            "\nKeyboardInterrupt detected. Exiting Function", style="yellow")
        return
    except Exception as e:
        console.print(f"There was an error ({e})", style="red")


def delete_habit(name: str = ""):
    """
    Delete a habit.
    """
    try:
        if len(all_habits) != 0:
            if name:
                for habit in all_habits:
                    if habit.name == name:
                        habit.remove_from_db()
                        return
                console.print(
                    f"\nYou have no habit called {name}", style="yellow")
            else:
                console.print("\nWhich habit would you like to delete?\n")
                console.print(indexed_habits)
                del_index: int = IntPrompt.ask(
                    "\nYour habit", choices=habit_ids)
                all_habits[del_index].remove_from_db()
        else:
            console.print(
                "\nYou have no habits to delete. Get started by typing \"create habit\" to create and start tracking a new habit.\n")
    except KeyboardInterrupt:
        console.print(
            "\nKeyboardInterrupt detected. Exiting function.\n", style="yellow")


def mark_done(name: str = ""):
    try:
        if len(all_habits) != 0:
            if name:
                for habit in all_habits:
                    if habit.name == name:
                        habit.mark_as_done()
                        return
            else:
                console.print(
                    "\nWhich habit would you like to mark as done?\n")
                console.print(indexed_habits)
                mark_index = IntPrompt.ask("\nYour habit", choices=habit_ids)
                all_habits[mark_index].mark_as_done()
        else:
            console.print(
                "\nYou have no habits to mark as done. Get started by typing \"create habit\" to create and start tracking a new habit.\n")
    except KeyboardInterrupt:
        console.print(
            "\nKeyboardInterrupt detected. Exiting function.\n", style="yellow")

