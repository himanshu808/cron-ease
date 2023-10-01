from __future__ import annotations
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
    def get_cronjob_obj(cronjob: str) -> CronJob:
        original_cronjob: str

        cronjob = cronjob.lstrip(WHITESPACE)
        if cronjob[0] == "#":
            is_commented = True
            cronjob = cronjob.lstrip("#"+WHITESPACE)
        else:
            is_commented = False

        original_cronjob = cronjob

        minute, cronjob = parse_minute(original_cronjob)
        hour, cronjob = parse_hour(original_cronjob)
        day_of_month, cronjob = parse_day_of_month(original_cronjob)
        month, cronjob = parse_month(original_cronjob)
        day_of_week, cronjob = parse_day_of_week(original_cronjob)
        cmd, comments = parse_cmd_and_comments(cronjob)

        return CronJob(minute, hour, day_of_month, month, day_of_week, cmd, is_commented, comments)

    def __repr__(self) -> str:
        repr_str = f"{self.minute} {self.hour} {self.day_of_month} {self.month} {self.day_of_week} {self.cmd}"
        if self.comments:
            repr_str += f"#{self.comments}"
        if self.is_commented:
            repr_str = "# " + repr_str

        return repr_str
