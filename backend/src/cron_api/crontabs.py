from .crontab import CronTab


class CronTabs:
    def __init__(self):
        self.crontabs: dict[str, CronTab] = {}

    def add_crontab(self, container_id: str, crontab: CronTab):
        self.crontabs[container_id] = crontab
