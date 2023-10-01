from backend.src.resources import *

ROUTES = [
    ["/containers", ContainerResource],
    ["/crons", CronJobResource, "all"],
    ["/crons/{c_id}", CronJobResource],
    ["/crons/{c_id}/{job_id:int(min=1)}", CronJobResource, "id"],
    ["/crons/{c_id}/toggle/{job_id:int(min=1)}", CronJobResource, "toggle"]
]
