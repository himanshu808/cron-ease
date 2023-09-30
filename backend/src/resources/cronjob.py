import falcon

from backend.main import crontabs
from .container import ContainerResource
from backend.src.models import CRONJOB
from docker.models.containers import Container
from copy import deepcopy


class CronJobResource:
    def on_get(self, req, resp):
        containers: list[Container] = []

        if not req.has_param("container"):
            containers = ContainerResource.get_containers()
        else:
            container = ContainerResource.get_container_by_name(req.get_param("container"))
            if container is not None:
                containers.append(container)

        body = []
        for container in containers:
            data = deepcopy(CRONJOB)
            data["container"] = container.name
            data["jobs"] = crontabs.get_container_crontab(container.short_id).get_cronjobs_as_list()
            body.append(data)

        resp.body = body
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        minute = req.get_param("minute", required=True)
        hour = req.get_param("hour", required=True)
        day_of_month = req.get_param("day_of_month", required=True)
        month = req.get_param("month", required=True)
        day_of_week = req.get_param("day_of_week", required=True)
        cmd = req.get_param("cmd", required=True)
        is_commented = req.get_param_as_bool("is_commented", default=False)
        comments = req.get_param("comments")
        container = req.get_param("container", required=True)

        container_obj = ContainerResource.get_container_by_name(container)
        crontab = crontabs.get_container_crontab(container_obj.short_id)
        successful = crontab.add_cronjob(minute=minute, hour=hour, day_of_month=day_of_month, month=month,
                                         day_of_week=day_of_week, cmd=cmd, is_commented=is_commented, comments=comments)

        if not successful:
            resp.body = "failed to create cronjob"
            resp.status = falcon.HTTP_500
        else:
            resp.body = "cronjob added successfully"
            resp.status = falcon.HTTP_200

