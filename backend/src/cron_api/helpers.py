from . import WHITESPACE, MONTHS, DAYS
from typing import Optional


def check_int(inp: str) -> bool:
    try:
        int(inp)
        return True
    except:
        return False


def validate_minute(minute: str) -> bool:
    temp: list[str]

    if minute == "*":
        return True
    elif check_int(minute):
        if "0" <= minute <= "59":
            return True
        return False

    temp = minute.split("/")
    if len(temp) > 2:
        return False
    elif len(temp) == 2:
        for m in temp:
            return validate_minute(m)

    temp = minute.split("-")
    if len(temp) != 2:
        return False

    for m in temp:
        return validate_minute(m)


def validate_hour(hour: str) -> bool:
    temp: list[str]

    if hour == "*":
        return True
    elif check_int(hour):
        if "0" <= hour <= "23":
            return True
        return False

    temp = hour.split("/")
    if len(temp) > 2:
        return False
    elif len(temp) == 2:
        for h in temp:
            return validate_hour(h)

    temp = hour.split("-")
    if len(temp) != 2:
        return False

    for h in temp:
        return validate_hour(h)


def validate_day_of_month(day: str) -> bool:
    temp: list[str]

    if day == "*":
        return True
    elif check_int(day):
        if "0" <= day <= "31":
            return True
        return False

    temp = day.split("/")
    if len(temp) > 2:
        return False
    elif len(temp) == 2:
        for d in temp:
            return validate_day_of_month(d)

    temp = day.split("-")
    if len(temp) != 2:
        return False

    for d in temp:
        return validate_day_of_month(d)


def validate_month(month: str) -> bool:
    temp: list[str]

    if month == "*":
        return True
    elif check_int(month):
        if "1" <= month <= "12":
            return True
        return False
    elif month.upper() in MONTHS:
        return True

    temp = month.split("/")
    if len(temp) > 2:
        return False
    elif len(temp) == 2:
        for m in temp:
            return validate_month(m)

    temp = month.split("-")
    if len(temp) != 2:
        return False

    for m in temp:
        return validate_month(m)


def validate_day_of_week(day: str) -> bool:
    temp: list[str]

    if day == "*":
        return True
    elif check_int(day):
        if "0" <= day <= "7":
            return True
        return False
    elif day.upper() in DAYS:
        return True

    temp = day.split("/")
    if len(temp) > 2:
        return False
    elif len(temp) == 2:
        for m in temp:
            return validate_day_of_week(m)

    temp = day.split("-")
    if len(temp) != 2:
        return False

    for m in temp:
        return validate_day_of_week(m)


def parse_minute(cronjob: str) -> tuple[str, str]:
    temp: list[str]
    minutes: list[str]

    cronjob = cronjob.lstrip(WHITESPACE)
    temp = cronjob.split(" ", 1)
    if len(temp) != 2:
        raise Exception(f"invalid minute in {cronjob}!")

    minutes = temp[0].split(",")
    for m in minutes:
        if not validate_minute(m):
            raise Exception(f"invalid minute: {m} in {cronjob}!")

    return temp[0].strip(WHITESPACE), temp[1].strip(WHITESPACE)


def parse_hour(cronjob: str) -> tuple[str, str]:
    temp: list[str]
    hour: str
    hours: list[str]

    cronjob = cronjob.lstrip(WHITESPACE)
    temp = cronjob.split(" ", 2)

    if len(temp) != 3:
        raise Exception(f"invalid hour in {cronjob}!")

    hour = temp[1]
    hours = hour.split(",")
    for h in hours:
        if not validate_hour(h):
            raise Exception(f"invalid hour: {h} in {cronjob}!")

    return hour.strip(WHITESPACE), temp[2].strip(WHITESPACE)


def parse_day_of_month(cronjob: str) -> tuple[str, str]:
    temp: list[str]
    day: str
    days: list[str]

    cronjob = cronjob.lstrip(WHITESPACE)
    temp = cronjob.split(" ", 3)

    if len(temp) != 4:
        raise Exception(f"invalid day of month in {cronjob}!")

    day = temp[2]
    days = day.split(",")
    for d in days:
        if not validate_day_of_month(d):
            raise Exception(f"invalid day of month: {d} in {cronjob}!")

    return day.strip(WHITESPACE), temp[3].strip(WHITESPACE)


def parse_month(cronjob: str) -> tuple[str, str]:
    temp: list[str]
    month: str
    months: list[str]

    cronjob = cronjob.lstrip(WHITESPACE)
    temp = cronjob.split(" ", 4)

    if len(temp) != 5:
        raise Exception(f"invalid month in {cronjob}!")

    month = temp[3]
    months = month.split(",")
    for m in months:
        if not validate_month(m):
            raise Exception(f"invalid month: {m} in {cronjob}!")

    return month.strip(WHITESPACE), temp[4].strip(WHITESPACE)


def parse_day_of_week(cronjob: str) -> tuple[str, str]:
    temp: list[str]
    day: str
    days: list[str]

    cronjob = cronjob.lstrip(WHITESPACE)
    temp = cronjob.split(" ", 5)

    if len(temp) != 6:
        raise Exception(f"invalid day of week in {cronjob}!")

    day = temp[4]
    days = day.split(",")
    for d in days:
        if not validate_day_of_week(d):
            raise Exception(f"invalid day of week: {d} in {cronjob}!")

    return day.strip(WHITESPACE), temp[5].strip(WHITESPACE)


def parse_cmd_and_comments(cronjob: str) -> tuple[str, Optional[str]]:
    temp: list[str]

    temp = cronjob.split("#", 1)
    if len(temp) != 2:
        return temp[0].strip(WHITESPACE), None
    return temp[0].strip(WHITESPACE), temp[1].strip(WHITESPACE)
