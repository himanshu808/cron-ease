import docker


def is_container_running(container_id: str) -> bool:
    if docker_client.containers.get(container_id).status.lower() != "running":
        return False
    return True


def exec_cmd(container_id: str, cmd: str):
    if not is_container_running(container_id):
        raise Exception("container not running!")

    container = docker_client.containers.get(container_id)
    return container.exec_run(cmd)


docker_client = docker.from_env()
