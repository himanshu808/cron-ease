import docker.errors
import falcon

from backend.src.models import CONTAINER_MODEL
from copy import deepcopy
from . import docker_client
from typing import Optional
from docker.models.containers import Container


class ContainerResource:
    @staticmethod
    def get_containers(only_running: bool = False, before: Optional[str] = None, since: Optional[str] = None,
                       limit: int = -1) -> list[Container]:
        try:
            return docker_client.containers.list(all=only_running, before=before, since=since, limit=limit)
        except docker.errors.APIError as e:
            print(e)
            return []
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_container_by_name(name: str) -> Optional[Container]:
        try:
            return docker_client.containers.get(name)
        except docker.errors.NotFound as e:
            print(e)
        except docker.errors.APIError as e:
            print(e)
        except Exception as e:
            print(e)

    def on_get(self, req, resp):
        # TODO: maybe add filter for getting running/all containers
        containers = ContainerResource.get_containers()
        resp.status = falcon.HTTP_200

        body = []
        for container in containers:
            data = deepcopy(CONTAINER_MODEL)
            data["id"] = container.short_id
            data["name"] = container.name
            data["state"] = container.status
            body.append(data)

        resp.body = body
