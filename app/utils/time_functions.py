"""
Time generation related functions
"""
import datetime


def current_utc_time():
    """
    Returns current utc epoch
    """
    return f'{datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z'
