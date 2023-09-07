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


