import falcon

from . import docker_client



class CronJobResource:
    def on_get(self, req, resp):
        containers = docker_client.containers()
        # cronjobs =
