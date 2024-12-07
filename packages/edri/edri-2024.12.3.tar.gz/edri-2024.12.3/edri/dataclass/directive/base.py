from dataclasses import dataclass

from edri.dataclass.directive import ResponseDirective


@dataclass
class InternalServerErrorResponseDirective(ResponseDirective):
    message: str | None = None
