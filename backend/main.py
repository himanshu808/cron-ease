from src.cron_api.crontab import CronTab
from src.cron_api.crontabs import CronTabs
from utils.docker_client import docker_client


crontabs = CronTabs()


def initialize_app():
    containers = docker_client.containers.list(all=True)
    for container in containers:
        crontabs.add_crontab(container.short_id, CronTab(container_id=container.short_id,
                                                         container_name=container.name))
