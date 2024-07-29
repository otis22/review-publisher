import unittest
import datetime
from review.schedule import Schedule
from zoneinfo import ZoneInfo


class ScheduleCase(unittest.TestCase):

    def test_since_date_monday_for_tuesday(self):
        tuesday = datetime.datetime(2020, 7, 28)
        schedule = Schedule('mon-fri', 15)
        self.assertEqual(
            schedule.since_date(tuesday).strftime('%A'),
            'Monday'
        )

    def test_since_date_thursday_for_friday(self):
        friday = datetime.datetime(2020, 7, 31)
        schedule = Schedule('mon-fri', 15)
        self.assertEqual(
            schedule.since_date(friday).strftime('%A'),
            'Thursday'
        )

    def test_since_date_friday_for_monday(self):
        monday = datetime.datetime(2020, 7, 27)
        schedule = Schedule('mon-fri', 15)
        self.assertEqual(
            schedule.since_date(monday).strftime('%A'),
            'Friday'
        )

    def test_since_date_yesterday_for_monday(self):
        monday = datetime.datetime(2020, 7, 27)
        schedule = Schedule('tue-fri', 15)
        self.assertEqual(
            schedule.since_date(monday).strftime('%A'),
            'Sunday'
        )

    def test_since_time_datails(self):
        monday = datetime.datetime(2020, 7, 27)
        schedule = Schedule('mon-fri', 15)
        self.assertEqual(
            schedule.since_date(monday).strftime('%H:%M:%S'),
            '15:00:00'
        )

    def test_since_time_check_timezone_plus_exists(self):
        monday = datetime.datetime(2020, 7, 27, tzinfo=ZoneInfo('Europe/Kiev'))
        schedule = Schedule('mon-fri', 15)
        self.assertTrue(
            '+' in schedule.since_date(monday).isoformat()
        )


if __name__ == '__main__':
    unittest.main()
