from multiprocessing.connection import Connection
from typing import Optional

from edri.dataclass.event import event
from edri.dataclass.response import Response, response
from edri.events.edri.group import Router
from edri.events.edri.router import Demands


@response
class SubscribedAllResponse(Response):
    demands: Demands


@event
class SubscribedAll(Router):
    pipe: Optional[Connection]
    response: SubscribedAllResponse
