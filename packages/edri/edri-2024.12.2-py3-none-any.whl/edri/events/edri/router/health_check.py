from http import HTTPMethod

from edri.api.dataclass.api_event import api
from edri.dataclass.event import event
from edri.dataclass.response import Response, response
from edri.events.edri.group import Router
from edri.dataclass.health_checker import Status, Record


@response
class HealthCheckResponse(Response):
    name: str
    status: Status


@event
class HealthCheck(Router):
    response: HealthCheckResponse


@response
class HealthCheckStatusResponse(Response):
    statuses: dict[str, Record]


@api(url="/health-check-status", resource="health-check-status", template="health_check_status.j2")
class HealthCheckStatus(Router):
    method: HTTPMethod = HTTPMethod.GET
    response: HealthCheckStatusResponse