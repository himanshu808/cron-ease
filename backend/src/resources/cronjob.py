import falcon

from backend.main import crontabs
from .container import ContainerResource
from backend.src.models import CRONJOB
from docker.models.containers import Container
from copy import deepcopy


class CronJobResource:
    def on_get_all(self, req, resp):
        containers: list[Container]
        containers = ContainerResource.get_containers()

        body = []
        for container in containers:
            data = deepcopy(CRONJOB)
            data["container"] = container.name
            data["jobs"] = crontabs.get_container_crontab(container.short_id).get_cronjobs_as_list()
            body.append(data)

        resp.body = body
        resp.status = falcon.HTTP_200

    def on_get(self, req, resp, c_id):
        container = ContainerResource.get_container_by_name(c_id)

        if container is None:
            resp.body = f"{c_id} not found"
            resp.status = falcon.HTTP_200
            return

        body = deepcopy(CRONJOB)
        body["container"] = container.name
        body["jobs"] = crontabs.get_container_crontab(container.short_id).get_cronjobs_as_list()

        resp.body = body
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, c_id):
        minute = req.get_param("minute", required=True)
        hour = req.get_param("hour", required=True)
        day_of_month = req.get_param("day_of_month", required=True)
        month = req.get_param("month", required=True)
        day_of_week = req.get_param("day_of_week", required=True)
        cmd = req.get_param("cmd", required=True)
        is_commented = req.get_param_as_bool("is_commented", default=False)
        comments = req.get_param("comments")

        container_obj = ContainerResource.get_container_by_name(c_id)
        crontab = crontabs.get_container_crontab(container_obj.short_id)
        successful = crontab.add_cronjob(minute=minute, hour=hour, day_of_month=day_of_month, month=month,
                                         day_of_week=day_of_week, cmd=cmd, is_commented=is_commented, comments=comments)

        if not successful:
            resp.body = "failed to create cronjob"
            resp.status = falcon.HTTP_500
        else:
            resp.body = "cronjob added successfully"
            resp.status = falcon.HTTP_200

    def on_delete_id(self, req, resp, c_id, job_id):
        container_obj = ContainerResource.get_container_by_name(c_id)
        crontab = crontabs.get_container_crontab(container_obj.short_id)

        cronjob_id = job_id - 1  # 0-indexing

        if cronjob_id >= len(crontab.cronjobs):
            resp.body = "cronjob not found"
            resp.status = falcon.HTTP_422
            return

        successful = crontab.delete_cronjob(cronjob_id)

        if not successful:
            resp.body = "failed to delete cronjob"
            resp.status = falcon.HTTP_500
        else:
            resp.body = "cronjob deleted successfully"
            resp.status = falcon.HTTP_200
        container_obj = ContainerResource.get_container_by_name(container)
        crontab = crontabs.get_container_crontab(container_obj.short_id)
        successful = crontab.delete_cronjob(minute=minute, hour=hour, day_of_month=day_of_month, month=month,
                                            day_of_week=day_of_week, cmd=cmd, is_commented=is_commented,
                                            comments=comments)

        if not successful:
            resp.body = "failed to delete cronjob"
            resp.status = falcon.HTTP_500
        else:
            resp.body = "cronjob deleted successfully"
            resp.status = falcon.HTTP_200

