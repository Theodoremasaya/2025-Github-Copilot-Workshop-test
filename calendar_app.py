#!/usr/bin/env python3
"""
Python Calendar Application with Western and Japanese dates
Shows monthly calendar with both date formats and public holidays.
"""

import calendar
import datetime
import holidays
import japanera
import sys


def get_user_input():
    """Get year and month input from user."""
    try:
        year = int(input("Enter year (e.g., 2024): "))
        month = int(input("Enter month (1-12): "))
        
        if month < 1 or month > 12:
            print("Error: Month must be between 1 and 12")
            return None, None
            
        if year < 1:
            print("Error: Year must be positive")
            return None, None
            
        return year, month
    except ValueError:
        print("Error: Please enter valid numbers")
        return None, None


def format_date_info(date_obj, japan_holidays, us_holidays):
    """Format date information including Western, Japanese, and holiday info."""
    # Western date format
    western_date = date_obj.strftime("%Y-%m-%d")
    
    # Japanese date format using japanera
    era_date = japanera.EraDate.from_date(date_obj)
    japanese_date = str(era_date)  # This gives us the default Japanese format
    
    # Check for holidays
    holiday_info = []
    if date_obj in japan_holidays:
        holiday_info.append(f"🎌 {japan_holidays[date_obj]}")
    if date_obj in us_holidays:
        holiday_info.append(f"🇺🇸 {us_holidays[date_obj]}")
    
    return western_date, japanese_date, holiday_info


def display_calendar(year, month):
    """Display calendar with both Western and Japanese dates and holidays."""
    # Get holidays for the year
    japan_holidays = holidays.Japan(years=year)
    us_holidays = holidays.UnitedStates(years=year)
    
    # Get calendar for the month
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    print(f"\n{'='*80}")
    print(f"CALENDAR FOR {month_name.upper()} {year}")
    print(f"{'='*80}")
    
    # Header
    print(f"{'Day':<4} {'Western Date':<12} {'Japanese Date':<20} {'Holidays'}")
    print(f"{'-'*80}")
    
    # Days of week header
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Process each week
    for week in cal:
        for i, day in enumerate(week):
            if day == 0:  # Empty day
                continue
            
            # Create date object
            date_obj = datetime.date(year, month, day)
            
            # Get formatted information
            western_date, japanese_date, holiday_info = format_date_info(
                date_obj, japan_holidays, us_holidays
            )
            
            # Format holiday information
            holiday_str = " | ".join(holiday_info) if holiday_info else ""
            
            # Display day info
            weekday = weekdays[i]
            print(f"{day:2d} {weekday:<4} {western_date:<12} {japanese_date:<20} {holiday_str}")
    
    print(f"{'-'*80}")
    
    # Summary of holidays for the month
    month_holidays = []
    for date_obj in sorted(japan_holidays.keys()):
        if date_obj.year == year and date_obj.month == month:
            month_holidays.append((date_obj, f"🎌 Japan: {japan_holidays[date_obj]}"))
    
    for date_obj in sorted(us_holidays.keys()):
        if date_obj.year == year and date_obj.month == month:
            month_holidays.append((date_obj, f"🇺🇸 US: {us_holidays[date_obj]}"))
    
    if month_holidays:
        print(f"\nHOLIDAYS IN {month_name.upper()} {year}:")
        for date_obj, holiday_desc in sorted(month_holidays):
            western_date, japanese_date, _ = format_date_info(date_obj, japan_holidays, us_holidays)
            print(f"  {western_date} ({japanese_date}) - {holiday_desc}")
    else:
        print(f"\nNo holidays in {month_name} {year}")
    
    print(f"{'='*80}\n")


def main():
    """Main application function."""
    print("🗓️  Python Calendar Application")
    print("Displays Western and Japanese dates with public holidays")
    print()
    
    while True:
        year, month = get_user_input()
        
        if year is None or month is None:
            continue
        
        try:
            display_calendar(year, month)
        except Exception as e:
            print(f"Error displaying calendar: {e}")
            continue
        
        # Ask if user wants to continue
        while True:
            continue_choice = input("Would you like to view another month? (y/n): ").lower().strip()
            if continue_choice in ['y', 'yes']:
                break
            elif continue_choice in ['n', 'no']:
                print("Thank you for using the Calendar Application!")
                return
            else:
                print("Please enter 'y' for yes or 'n' for no.")


if __name__ == "__main__":
    main()