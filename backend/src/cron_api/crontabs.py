from .crontab import CronTab
from typing import Optional


class CronTabs:
    def __init__(self):
        self.crontabs: dict[str, CronTab] = {}

    def add_crontab(self, container_id: str, crontab: CronTab):
        self.crontabs[container_id] = crontab

    def get_container_crontab(self, container_id: str) -> Optional[CronTab]:
        return self.crontabs.get(container_id)
