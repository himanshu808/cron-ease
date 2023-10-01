from .cronjob import CronJob
from . import is_container_running, exec_cmd
from .constants import *
from typing import Optional
from .helpers import create_bash_cmd
from copy import deepcopy
import re


class CronTab:
    def __init__(self, container_id: str, container_name: str):
        self.container_id: str = container_id
        self.container_name: str = container_name
        self.cronjobs: list[CronJob] = []
        self.get_cronjobs()

    def get_cronjobs(self) -> None:
        self.cronjobs = []

        if not is_container_running(self.container_id):
            return
        exit_code, output = exec_cmd(self.container_id, LIST_CRONTAB)
        output = output.decode("utf-8")
        if exit_code == 1:
            if output.strip().lower().startswith("no crontab for"):
                return
            raise Exception("error while fetching cronjobs!")

        for cronjob in output.splitlines():
            self.cronjobs.append(CronJob.get_cronjob_obj(cronjob))

    def get_cronjobs_as_list(self) -> list[str]:
        crons: list[str] = []
        self.get_cronjobs()

        for cron in self.cronjobs:
            crons.append(repr(cron))
        return crons

    def add_cronjob(self, minute: str, hour: str, day_of_month: str, month: str, day_of_week: str, cmd: str,
                    is_commented: bool = False, comments: Optional[str] = None):
        cronjob = CronJob(minute=minute, hour=hour, day_of_month=day_of_month, month=month, day_of_week=day_of_week,
                          cmd=cmd, is_commented=is_commented, comments=comments)
        try:
            cronjob = CronJob.get_cronjob_obj(repr(cronjob))
        except Exception as e:
            print(e)
            return False

        append_cmd = APPEND_CRONJOB_CMD.format(cronjob=repr(cronjob))
        exit_code, output = exec_cmd(self.container_id, create_bash_cmd(append_cmd))
        if exit_code:
            print(f"error: {output}")
            return False

        self.cronjobs.append(cronjob)

        return True

    def delete_cronjob(self, job_id: int):
        cronjob = self.cronjobs[job_id]

        delete_cmd = DELETE_CRONJOB_CMD.format(cronjob=repr(cronjob))
        exit_code, output = exec_cmd(self.container_id, create_bash_cmd(delete_cmd))
        if exit_code:
            print(f"error: {output}")
            return False

        self.cronjobs.pop(job_id)
        return True

    def toggle_cronjob(self, job_id: int):
        original_cronjob = self.cronjobs[job_id]
        updated_cronjob = deepcopy(original_cronjob)
        updated_cronjob.is_commented = not updated_cronjob.is_commented

        toggle_cmd = UPDATE_CRONJOB_CMD.format(line_no=job_id+1,
                                               original_cronjob=re.escape(repr(original_cronjob)),
                                               updated_cronjob=repr(updated_cronjob))
        exit_code, output = exec_cmd(self.container_id, create_bash_cmd(toggle_cmd))
        if exit_code:
            print(f"error: {output}")
            return False, original_cronjob.is_commented
        return True, original_cronjob.is_commented

