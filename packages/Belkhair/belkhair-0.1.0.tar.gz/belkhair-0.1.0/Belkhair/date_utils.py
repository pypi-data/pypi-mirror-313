from datetime import datetime

def current_date():
    """Get the current date."""
    return datetime.now().strftime("%Y-%m-%d")

def days_between(date1, date2):
    """Calculate the number of days between two dates."""
    d1 = datetime.strptime(date1, "%Y-%m-%d")
    d2 = datetime.strptime(date2, "%Y-%m-%d")
    return abs((d2 - d1).days)
