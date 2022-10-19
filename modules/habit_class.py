"""
The module containing the code for the main habit class
"""

# Datetime module to work with dates easily
from datetime import datetime

# Database to store habits in
import modules.database as database

# Rich prompt module to have user input a string from the options
from rich.prompt import Prompt

# Rich console to display strings with styling
from rich.console import Console

# Instantiate a default rich console
console = Console()


class Habit:
    """
    Habit class containing attributes and methods for working with habits

    ...

    Methods
    ---
    add_to_db
        Add this habit to the database
    remove_from_db
        Remove this habit from the database
    mark_as_done
        Mark this habit as done for its period
    set_status
        Set the users status of this habit

    Attributes
    ---
    name: str
        The name of the habit
    period: str
        The periodicity of the habit
    started_on: str, optional
        The date and time this habit was started
    last_checked_on: str, optional
        The date and time this habit was last marked as complete
    streak_longest: int, optional
        The longest streak of this habit
    streak_current: int, optional
        The current streak of this habit
    """

    def __init__(self, name: str, period: str, started_on: str = "None", last_checked_on: str = "None", streak_longest: int = 0, streak_current: int = 0):

        # The 2 required parameters for instantiating a habit class
        self.name = name
        self.period = period

        self.streak_longest = int(streak_longest)
        self.streak_current = int(streak_current)

        if started_on and started_on != "None":
            self.started_on = datetime.strptime(
                started_on, "%Y-%m-%d %H:%M:%S")
        else:
            self.started_on = datetime.strptime(
                datetime.today().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

        if last_checked_on and last_checked_on != "None":
            self.last_checked_on = datetime.strptime(
                last_checked_on, "%Y-%m-%d %H:%M:%S")
        else:
            self.last_checked_on = last_checked_on

        self.days_since_checked = ""

        # Everytime the class is instantiated, set its status
        self.set_status()

    # Check if user is overdue on their habit
    def set_status(self):
        """
        Set the users status of this habit to:
            - in time (if dsc <= period)
            - late (if dsc > period)
        """

        # Habits that havent been checked even once after being created
        if self.last_checked_on == "None":
            # in time status so it can be checked at anytime
            self.status = "in time"
            return

        self.days_since_checked = (
            datetime.today().date() - self.last_checked_on.date()).days

        if self.period == "day":
            if self.days_since_checked <= 1:
                self.status = "in time"
            else:
                self.status = "late"
        elif self.period == "week":
            if self.days_since_checked <= 14:
                self.status = "in time"
            else:
                self.status = "late"
        else:
            if self.days_since_checked <= 61:
                self.status = "in time"
            else:
                self.status = "late"

    def __restart(self):
        """
        Restart the streak and update the last checked on variable
        """
        self.streak_current = 1
        self.last_checked_on = datetime.strptime(
            datetime.today().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        response = database.update(self)
        if response == 'updated':
            console.print(
                f"\nYou did not check your \"{self.name}\" habit within the {self.period}, so it broke.\n", style='red')
            console.print("We've now reset your streak back to 1.\n",
                          style='yellow')
        else:
            console.print(f"\nThere was an error ({response})\n", style="red")

    def __check(self):
        """
        Increase the streak and update the last checked on variable
        """
        self.streak_current += 1
        self.last_checked_on = datetime.strptime(
            datetime.today().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        console.print(
            f"\nSuccessfully marked your \"{self.name}\" habit as done for the {self.period}\nYou are now at a streak of {self.streak_current}\n", style="green")

        if self.streak_current > self.streak_longest:
            self.streak_longest = self.streak_current
            console.print(
                "This is now your new longest streak!\n", style="green")
        database.update(self)

    def prompt_to_check(self):
        """
        Prompt the user to mark this habit as complete for the first 
        time in their chosen period
        """
        if Prompt.ask(
                f"\nType \"mark done\" to mark your \"{self.name}\" habit as done for the {self.period}\n", choices=["mark done", "leave unchecked"]) == 'mark done':
            self.__check()
        else:
            console.print(
                "\nYour habit was not marked as done\n", style="yellow")

    def add_to_db(self):
        """
        Add this habit class to the database
        """
        response = database.add(self)
        if response == 'added':
            console.print(
                "\nSuccessfully created and added:", style="green")
            console.print(
                f"\n\tHabit Name: {self.name}\n\tRepeat once every: {self.period}\n")
            console.print("to the database\n", style="green")
            console.print(
                f"\nYou must now mark this habit as done atleast once within a {self.period} to keep it going\n", style="yellow")
        else:
            console.print(
                f"\nYour habit could not be added ({response})\n", style="red")

    def remove_from_db(self):
        """
        Remove this habit class from the database
        """
        response = database.delete(self)
        if response == 'deleted':
            console.print(
                f"\nSuccessfully deleted your \"{self.name}\" habit from the database\n", style="green")
        else:
            console.print(
                f"\nYour habit could not be deleted from the database ({response})\n", style="red")

    def mark_as_done(self):
        """
        Mark this habit as complete for the period
        """

        # If the status for this habit is "late"
        # Restart this habit
        if self.status == "late":
            self.__restart()
            return 'restarted and checked'

        # Otherwise, mark it as complete
        self.__check()
        return 'checked'
