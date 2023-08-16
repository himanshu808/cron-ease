from .cronjob import CronJob
from . import is_container_running, exec_cmd
from .constants import *


class CronTab:
    def __init__(self, container_id: str, container_name: str):
        self.container_id: str = container_id
        self.container_name: str = container_name
        self.cronjobs: list[CronJob] = []
        self.get_cronjobs()

    def get_cronjobs(self):
        if not is_container_running(self.container_id):
            return
        exit_code, output = exec_cmd(self.container_id, LIST_CRONTAB)
        output = output.decode("utf-8")
        if exit_code == 1:
            if output.strip().startswith("no crontab for"):
                return
            raise Exception("error while fetching cronjobs!")

        for cronjob in output.splitlines():
            self.cronjobs.append(CronJob.create_cronjob(cronjob))

    def add_cronjob(self):
        pass

    def delete_cronjob(self):
        pass

    def delete_all_cronjobs(self):
        pass

    def update_cronjob(self):
        pass



