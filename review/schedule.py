from datetime import datetime, timedelta


def yesterday(now):
    return now - timedelta(days=1)


def friday_from_monday(now):
    assert now.weekday() == 0
    return now - timedelta(days=3)


class Schedule:
    __day_of_week: str
    __hours: int
    __minutes: int

    def __init__(self, day_of_week: str, hours: int, minutes=0):
        self.__day_of_week = day_of_week
        self.__hours = hours
        self.__minutes = minutes

    def day_of_week(self) -> str:
        return self.__day_of_week

    def hours(self) -> int:
        return self.__hours

    def minutes(self):
        return self.__minutes

    def since_date(self, now: datetime) -> datetime:
        if self.every_week_day() and now.weekday() == 0:
            since_date = friday_from_monday(now)
        else:
            since_date = yesterday(now)
        return since_date.replace(hour=self.hours(), minute=self.minutes())

    def every_week_day(self):
        return self.day_of_week() == 'mon-fri'
