import docker.errors
import falcon

from backend.src.models import CONTAINER_MODEL
from copy import deepcopy
from . import docker_client


class ContainerResource:
    def on_get(self, req, resp):
        # TODO: maybe add filter for getting running/all containers
        try:
            containers = docker_client.containers.list(all=True)
        except docker.errors.APIError as e:
            print(e)
            return
        except Exception as e:
            print(e)
            return

        resp.status = falcon.HTTP_200

        body = []
        for container in containers:
            data = deepcopy(CONTAINER_MODEL)
            data["id"] = container.id
            data["name"] = container.name
            data["running"] = container.status
            body.append(data)

        resp.body = body
