import datetime

def night_name():
    """
    Determine the name for the current or previous night based on the time of day.

    If the current time is before noon, the function returns the date for the previous day 
    to ensure that data from late-night sessions are grouped correctly. Otherwise, it returns 
    the current date.

    Returns:
        str: A string formatted as 'YYYY_MM_DD' representing the night's date.
    """
    import datetime
    d = datetime.datetime.now()
    if d.hour < 12:
        d2  = d - datetime.timedelta(hours=12)
    else:
        d2 = d
    return f'{d2.year:4d}_{d2.month:02d}_{d2.day:02d}'

def utctime(h=None, m=None):
    t = datetime.datetime.utcnow()
    h = t.hour if h is None else h
    m = t.minute if m is None else m
    t2 = datetime.datetime(t.year, t.month, t.day, h, m, t.second, t.microsecond)
    if t2 < t:
        return t2+datetime.timedelta(days=1)
    else:
        return t2

