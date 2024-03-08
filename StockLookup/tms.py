"""
    Made by Monnapse

    Get timestamp seconds for dates/times, seconds minutes, hours, days, weeks, months, years.
"""

import time as t

class period_times:
    days_year = 365 # Days in a year
    days_month = 30 # Days in a month
    days_week = 7 # Days in a week
    hours_day = 24 # Hours in a day
    minute_hour = 60 # Minutes in an hour
    seconds_minute = 60 # Seconds in a minute

class time_type:
    """
        Period times in seconds, for timestamp
    """
    minute = period_times.minute_hour # Seconds in a minute
    hour = period_times.minute_hour * minute # Seconds in an hour
    day = period_times.hours_day * hour # Seconds in a day
    week = period_times.days_week * day # Seconds in a week
    month = period_times.days_month * day # Seconds in a week
    year = period_times.days_year * day # Seconds in a year

class timestamp_times:
    def time(amount: float=0, time_type: int=0) -> int:
        """
            Returns seconds in amount time_type
        """
        return amount * time_type
    
class time_direction:
    away = 1
    before = -1

class time:
    def now() -> int:
        """
            Returns the current time in seconds since the Epoch.
        """
        return int(t.time())
    def time(amount: float=0, time_type: int=0, direction: int=time_direction.away) -> int:
        """
            Returns the current time in seconds since the Epoch subtracted or added by seconds in amount time_type
        """
        return time.now() + (amount * time_type) * direction