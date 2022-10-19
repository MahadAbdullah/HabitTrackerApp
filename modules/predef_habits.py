"""
The module containing example habits that can be viewed to see what an active habit tracker might look like.
Also used for testing purposes.
"""

from modules.habit_class import Habit

# Datetime package to work with relative dates
# so the tests can work properly by having the same 
# time difference everytime
from datetime import datetime, timedelta

predefined_habits = [
    Habit("walk the dog",
          "day",
          datetime(2022, 8, 13).strftime("%Y-%m-%d %H:%M:%S"),
          datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
          31,
          31),
    Habit("exercise",
          "day",
          datetime(2022, 7, 5).strftime("%Y-%m-%d %H:%M:%S"),
          (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
          5,
          2),
    Habit("laundry",
          "week",
          datetime(2022, 8, 29).strftime("%Y-%m-%d %H:%M:%S"),
          ((datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")),
          1,
          1),
    Habit("clean the house",
          "week",
          datetime(2022, 4, 29).strftime("%Y-%m-%d %H:%M:%S"),
          ((datetime.today() - timedelta(days=15)).strftime("%Y-%m-%d %H:%M:%S")),
          99,
          40),
    Habit("review budget & finances",
          "month",
          datetime(2022, 1, 16).strftime("%Y-%m-%d %H:%M:%S"),
          ((datetime.today() - timedelta(days=17)).strftime("%Y-%m-%d %H:%M:%S")),
          65,
          65),
    Habit("review your inbox",
          "month",
          datetime(2022, 1, 21).strftime("%Y-%m-%d %H:%M:%S"),
          ((datetime.today() - timedelta(days=63)).strftime("%Y-%m-%d %H:%M:%S")),
          132,
          90),
    Habit("plan the month",
          "month",
          datetime(2022, 1, 21).strftime("%Y-%m-%d %H:%M:%S"),
          'None',
          0,
          0)
]
