from typing import Optional
from . import parse_minute, parse_hour, parse_day_of_month, parse_month, parse_day_of_week, parse_cmd_and_comments, \
    WHITESPACE


class CronJob:
    def __init__(self, minute: str, hour: str, day_of_month: str, month: str, day_of_week: str, cmd: str,
                 is_commented: bool = False, comments: Optional[str] = None):
        self.minute = minute
        self.hour = hour
        self.day_of_month = day_of_month
        self.month = month
        self.day_of_week = day_of_week
        self.cmd = cmd
        self.is_commented = is_commented
        self.comments = comments

    @staticmethod
    def create_cronjob(cronjob: str):
        original_cronjob = cronjob
        cronjob = cronjob.lstrip(WHITESPACE)
        if cronjob[0] == "#":
            is_commented = True
            cronjob = cronjob.lstrip("#"+WHITESPACE)
        else:
            is_commented = False

        minute, cronjob = parse_minute(original_cronjob)
        hour, cronjob = parse_hour(original_cronjob)
        day_of_month, cronjob = parse_day_of_month(original_cronjob)
        month, cronjob = parse_month(original_cronjob)
        day_of_week, cronjob = parse_day_of_week(original_cronjob)
        cmd, comments = parse_cmd_and_comments(cronjob)

        return CronJob(minute, hour, day_of_month, month, day_of_week, cmd, is_commented, comments)
