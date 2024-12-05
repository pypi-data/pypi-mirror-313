from edri.dataclass.event import event
from edri.dataclass.response import Response, response
from edri.events.edri.group import Router
from edri.dataclass.health_checker import Status


@response
class HealthCheckResponse(Response):
    name: str
    status: Status


@event
class HealthCheck(Router):
    response: HealthCheckResponse
