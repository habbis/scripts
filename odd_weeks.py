#!/usr/bin/env python3

Always show details
from datetime import datetime, timedelta



# Function to print all odd-numbered weeks in 2024

def print_odd_weeks(year):

    first_day_of_year = datetime(year, 1, 1)

    # Start with the first Monday of the year (week start)

    current_week_start = first_day_of_year + timedelta(days=(7 - first_day_of_year.weekday()))

    

    odd_weeks = []

    while current_week_start.year == year:

        week_number = current_week_start.isocalendar()[1]

        if week_number % 2 != 0:  # Check if the week is odd

            odd_weeks.append(week_number)

        current_week_start += timedelta(weeks=1)

    

    return odd_weeks



odd_weeks_2024 = print_odd_weeks(2024)

odd_weeks_2024
