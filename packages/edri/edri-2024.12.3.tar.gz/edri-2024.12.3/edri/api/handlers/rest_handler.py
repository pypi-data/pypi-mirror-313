from http import HTTPStatus
from json import dumps, JSONEncoder
from typing import Callable, Unpack, TypedDict, Type

from edri.api import Headers
from edri.api.handlers import HTTPHandler
from edri.api.handlers.http_handler import ResponseErrorKW
from edri.config.constant import ApiType
from edri.dataclass.directive import HTTPResponseDirective
from edri.dataclass.event import Event
from edri.utility import NormalizedDefaultDict


class ResponseKW(TypedDict):
    headers: NormalizedDefaultDict[str, Headers]


class RESTHandler[T: HTTPResponseDirective](HTTPHandler):
    _directive_handlers: dict[T, Callable[[T], tuple[int, Headers]]] = {}

    def __init__(self, scope: dict, receive: Callable, send: Callable, headers: NormalizedDefaultDict[str, Headers], json_encoder: Type[JSONEncoder]):
        super().__init__(scope, receive, send, headers)
        self.json_encoder = json_encoder

    @classmethod
    def api_type(cls) -> ApiType:
        return ApiType.REST

    async def response(self, status: HTTPStatus, data: Event | bytes, *args, **kwargs: Unpack[ResponseKW]):
        headers = kwargs["headers"]
        if isinstance(data, Event):
            response = data.get_response()
            if "Content-Type" not in headers:
                headers["Content-Type"].append("application/json")
            try:
                body = dumps(response.as_dict(transform=True, keep_concealed=False), ensure_ascii=False, cls=self.json_encoder).encode("utf-8")
            except TypeError as e:
                self.logger.error("Object is not JSON serializable", exc_info=e)
                await self.response_error(HTTPStatus.INTERNAL_SERVER_ERROR, {
                    "reasons": [{
                        "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
                        "message": "Object is not JSON serializable",
                    }]
                })
                return
        else:
            body = data

        return await super().response(status, body, headers=headers)

    async def response_error(self, status: HTTPStatus, data: Event | dict | None = None, *args, **kwargs: Unpack[ResponseErrorKW]):
        data = self.response_error_prepare(status, data)
        data = dumps(data, ensure_ascii=False, cls=self.json_encoder).encode("utf-8")
        return await super().response_error(status, data, *args, **kwargs)
