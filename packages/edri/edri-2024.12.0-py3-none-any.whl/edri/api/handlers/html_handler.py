from http import HTTPStatus
from os.path import abspath, dirname
from typing import Callable, Unpack, TypedDict, Type

from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError, TemplateNotFound, TemplateRuntimeError

from edri.api import Headers
from edri.api.handlers import HTTPHandler
from edri.api.extensions.url_extension import URLExtension
from edri.api.handlers.http_handler import ResponseErrorKW, HTTPDirectiveHandlerDict
from edri.config.constant import ApiType
from edri.config.setting import TEMPLATE_PATH, ENVIRONMENT
from edri.dataclass.directive import HTMLResponseDirective
from edri.dataclass.directive.html import RedirectResponseDirective
from edri.dataclass.event import Event
from edri.utility import NormalizedDefaultDict


class ResponseKW(TypedDict):
    headers: NormalizedDefaultDict[Headers]


def redirect_response_directive_handler():
    pass


class HTMLHandler[T](HTTPHandler):
    _directive_handlers: dict[Type[T], HTTPDirectiveHandlerDict[T]] = {
        RedirectResponseDirective: {
            "status": HTTPStatus.FOUND,
            "routine": lambda directive: {"location": [directive.location]},
        }
    }
    environment = Environment(loader=FileSystemLoader([TEMPLATE_PATH, dirname(abspath(__file__)) + "/../static_pages"]),
                              extensions=[URLExtension])
    environment.auto_reload = ENVIRONMENT == "development"

    @classmethod
    def api_type(cls) -> ApiType:
        return ApiType.HTML

    def __init__(self, scope: dict, receive: Callable, send: Callable, headers: NormalizedDefaultDict[str, Headers]):
        super().__init__(scope, receive, send, headers)
        self.directive_type = HTMLResponseDirective

    async def response(self, status: HTTPStatus, data: Event | bytes, *args, **kwargs: Unpack[ResponseKW]):
        headers = kwargs["headers"]
        if isinstance(data, Event):
            try:
                template = self.environment.get_template(self.event_type_extensions()[data.__class__]["template"])
            except TemplateNotFound as e:
                self.logger.error("Template was not found", exc_info=e)
                await self.response_error(HTTPStatus.INTERNAL_SERVER_ERROR, {
                    "reasons": [{
                        "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
                        "message": "Template was not found",
                    }]
                })
                return
            except TemplateSyntaxError as e:
                self.logger.error("Template syntax error", exc_info=e)
                await self.response_error(HTTPStatus.INTERNAL_SERVER_ERROR, {
                    "reasons": [{
                        "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
                        "message": "Template syntax error",
                    }]
                })
                return

            data = data.get_response().as_dict(transform=False, keep_concealed=True)
            data["scope"] = self.scope
            try:
                body = template.render(data).encode()
            except (TemplateRuntimeError, TemplateSyntaxError) as e:
                self.logger.error("Template could not be rendered", exc_info=e)
                await self.response_error(HTTPStatus.INTERNAL_SERVER_ERROR, {
                    "reasons": [{
                        "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
                        "message": str(e),
                    }]
                })
                return
            except TemplateNotFound as e:
                self.logger.error("Template was not found", exc_info=e)
                await self.response_error(HTTPStatus.INTERNAL_SERVER_ERROR, {
                    "reasons": [{
                        "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
                        "message": "Template was not found",
                    }]
                })
                return
            except Exception as e:
                self.logger.error("Unknown error", exc_info=e)
                await self.response_error(HTTPStatus.INTERNAL_SERVER_ERROR, {
                    "reasons": [{
                        "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
                        "message": "Unknown error",
                    }]
                })
                return
            if headers is None:
                headers = NormalizedDefaultDict[str, Headers](list)
            if "Content-Type" not in headers:
                headers["Content-Type"].append("text/html; charset=utf-8")
        else:
            body = data

        return await super().response(status, body, headers=headers)

    async def response_error(self, status: HTTPStatus, event: Event | dict | None = None, *args,
                             **kwargs: Unpack[ResponseErrorKW]):
        data = self.response_error_prepare(status, event)
        if status.is_redirection:
            if status in (HTTPStatus.MOVED_PERMANENTLY, HTTPStatus.FOUND, HTTPStatus.SEE_OTHER):
                directive = event.response._directives[0]
                data["redirect_location"] = directive.location if hasattr(directive, "location") else None
            template = self.environment.get_template("status_300.j2")
        elif status.is_client_error:
            template = self.environment.get_template("status_400.j2")
        else:
            template = self.environment.get_template("status_500.j2")
        event = template.render(data).encode()

        return await super().response_error(status, event, *args, **kwargs)
