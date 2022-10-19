import unittest

from modules.predef_habits import predefined_habits
import modules.database as database


class Test(unittest.TestCase):
    """
    Tests:
        Creating a habit
        Deleting a habit
        Marking a habit as done

    """
    daily_inTime = predefined_habits[0]
    daily_late = predefined_habits[1]
    weekly_inTime = predefined_habits[2]
    weekly_late = predefined_habits[3]
    monthly_inTime = predefined_habits[4]
    monthly_late = predefined_habits[5]
    # This habit has never been checked after being created
    # Habits like this are always in time to be checked whenever
    # possible
    monthly_neverChecked = predefined_habits[6]

    def setUp(self):
        # Remove all the predefined habits from the database at the
        # start of each test
        database.delete(self.daily_inTime)
        database.delete(self.daily_late)
        database.delete(self.weekly_inTime)
        database.delete(self.weekly_late)
        database.delete(self.monthly_inTime)
        database.delete(self.monthly_late)

    # Habit status logic
    # Used for helping with marking a habit as done
    def test_status(self):
        self.assertEqual(self.daily_inTime.status, "in time")
        self.assertEqual(self.daily_late.status, "late")
        self.assertEqual(self.weekly_inTime.status, "in time")
        self.assertEqual(self.weekly_late.status, "late")
        self.assertEqual(self.monthly_inTime.status, "in time")
        self.assertEqual(self.monthly_late.status, "late")
        self.assertEqual(self.monthly_neverChecked.status, "in time")

    #  Marking habits as complete
    def test_mark_done(self):
        self.assertEqual(self.daily_inTime.mark_as_done(), 'checked')
        
        # This streak was previously on 31
        self.assertEqual(self.daily_inTime.streak_current, 32)
        
        self.assertEqual(self.daily_late.mark_as_done(),
                         'restarted and checked')
                         
        # Since this habit was restarted, the streak should restart from 1
        self.assertEqual(self.daily_late.streak_current, 1)
        
        self.assertEqual(self.weekly_inTime.mark_as_done(), 'checked')
        
        # This habit was previously on 1
        self.assertEqual(self.weekly_inTime.streak_current, 2)
        
        self.assertEqual(self.weekly_late.mark_as_done(),
                         'restarted and checked')
        
        # This habit was restarted and should now be at a streak of 1
        self.assertEqual(self.weekly_late.streak_current, 1)
        
        self.assertEqual(self.monthly_inTime.mark_as_done(), 'checked')
        
        # This habit was previously on 65
        self.assertEqual(self.monthly_inTime.streak_current, 66)
        
        self.assertEqual(self.monthly_late.mark_as_done(),
                         'restarted and checked')
                         
        # This habit was restarted and should now be at a streak of 1
        self.assertEqual(self.monthly_late.streak_current, 1)

        self.assertEqual(self.monthly_neverChecked.mark_as_done(), 'checked')
        
        # This habit was started from the beginning so it should now be at 1
        self.assertEqual(self.monthly_neverChecked.streak_current, 1)

    # Adding habits
    def test_db_add(self):
        self.assertEqual(database.add(self.daily_inTime), 'added')
        self.assertEqual(database.add(self.daily_late), 'added')
        self.assertEqual(database.add(self.weekly_inTime), 'added')
        self.assertEqual(database.add(self.weekly_late), 'added')
        self.assertEqual(database.add(self.monthly_inTime), 'added')
        self.assertEqual(database.add(self.monthly_late), 'added')

    # Deleting habits
    def test_db_delete(self):
        self.assertEqual(database.delete(self.daily_inTime), 'deleted')
        self.assertEqual(database.delete(self.daily_late), 'deleted')
        self.assertEqual(database.delete(self.weekly_inTime), 'deleted')
        self.assertEqual(database.delete(self.weekly_late), 'deleted')
        self.assertEqual(database.delete(self.monthly_inTime), 'deleted')
        self.assertEqual(database.delete(self.monthly_late), 'deleted')

    def tearDown(self):
        # Since every habit was removed from the 
        # database at the start, this adds them back    
        database.add(self.daily_inTime)
        database.add(self.daily_late)
        database.add(self.weekly_inTime)
        database.add(self.weekly_late)
        database.add(self.monthly_inTime)
        database.add(self.monthly_late)


if __name__ == "__main__":
    unittest.main()
