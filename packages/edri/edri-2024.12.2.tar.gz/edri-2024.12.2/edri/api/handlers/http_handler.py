from abc import ABC, abstractmethod
from base64 import b64decode
from binascii import Error
from collections import defaultdict
from http import HTTPStatus, HTTPMethod
from http.cookies import SimpleCookie, Morsel
from io import BytesIO
from json import loads, JSONDecodeError
from mimetypes import guess_type
from multipart import MultipartParser
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryFile
from typing import Callable, Type, Pattern, Any, Unpack, TypedDict, NotRequired, AnyStr, BinaryIO
from re import compile
from urllib.parse import parse_qs, unquote, parse_qsl, quote

from edri.api import Headers
from edri.api.dataclass import File
from edri.api.dataclass.api_event import api_events
from edri.api.handlers import BaseHandler
from edri.api.handlers.base_handler import BaseDirectiveHandlerDict
from edri.config.constant import ApiType
from edri.config.setting import MAX_BODY_SIZE, ASSETS_PATH, UPLOAD_FILES_PREFIX
from edri.dataclass.directive import HTTPResponseDirective, ResponseDirective
from edri.dataclass.directive.base import InternalServerErrorResponseDirective
from edri.dataclass.directive.http import CookieResponseDirective, AccessDeniedResponseDirective, NotFoundResponseDirective, \
    UnauthorizedResponseDirective
from edri.dataclass.event import Event
from edri.utility import NormalizedDefaultDict
from edri.utility.function import camel2snake


class EventTypesExtensionsDict(TypedDict):
    url: str
    url_re: NotRequired[Pattern[AnyStr]]
    url_original: NotRequired[str]
    method: HTTPMethod
    cookies: dict[str, str]
    headers: dict[str, str]
    scope: dict[str, str]
    template: str | None


type EventTypesExtensions = dict[Type[Event], EventTypesExtensionsDict]


class ResponseKW(TypedDict):
    headers: NormalizedDefaultDict[str, Headers]


class ResponseErrorKW(TypedDict):
    headers: NotRequired[NormalizedDefaultDict[str, Headers]]


class HTTPDirectiveHandlerDict[T](BaseDirectiveHandlerDict):
    routine: NotRequired[Callable[[T, dict[str, Headers]], NormalizedDefaultDict[str, Headers]] | Callable[[T], NormalizedDefaultDict[str, Headers]]]
    status: NotRequired[HTTPStatus]
    headers: NotRequired[list[str]]


class HTTPHandler[T: HTTPResponseDirective](BaseHandler, ABC):
    _directive_handlers: dict[Type[T], HTTPDirectiveHandlerDict[T]] = {
        CookieResponseDirective: {
            "routine": lambda directive, headers: (
                {"cookie": HTTPHandler._create_cookie(directive, headers)}
            ),
            "headers": ["cookie"],
        },
        AccessDeniedResponseDirective: {
            "status": HTTPStatus.FORBIDDEN,
        },
        InternalServerErrorResponseDirective: {
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
        },
        UnauthorizedResponseDirective: {
            "status": HTTPStatus.UNAUTHORIZED,
        },
        NotFoundResponseDirective: {
            "status": HTTPStatus.NOT_FOUND,
        },
    }

    _event_types = None
    _event_type_extensions = None
    _event_type_names = None

    def __init__(self,
                 scope: dict,
                 receive: Callable,
                 send: Callable,
                 headers: NormalizedDefaultDict[str, Headers]):
        super().__init__(scope, receive, send)
        self.headers = headers
        self.cookies = self.parse_cookies(self.headers.get("cookie", ""))
        self.parameters: dict[str, Any] = self.parse_url_parameters()
        self.body = BytesIO()

    @classmethod
    @abstractmethod
    def api_type(cls) -> ApiType:
        pass

    @classmethod
    def event_types(cls):
        if cls._event_types is None:
            cls._event_types, cls._event_type_extensions, cls._event_type_names = cls.sort_events(cls.api_type())
        return cls._event_types

    @classmethod
    def event_type_extensions(cls) -> EventTypesExtensions:
        if cls._event_type_extensions is None:
            cls._event_types, cls._event_type_extensions, cls._event_type_names = cls.sort_events(cls.api_type())
        return cls._event_type_extensions

    @classmethod
    def event_type_names(cls) -> dict[str, Type[Event]]:
        if cls._event_type_names is None:
            cls._event_types, cls._event_type_extensions, cls._event_type_names = cls.sort_events(cls.api_type())
        return cls._event_type_names

    @classmethod
    def directive_handlers(cls) -> dict[Type[ResponseDirective], HTTPDirectiveHandlerDict]:
        handlers = {}
        for class_obj in reversed(cls.mro()):
            if hasattr(class_obj, "_directive_handlers"):
                # noinspection PyProtectedMember
                handlers.update(class_obj._directive_handlers)
        return handlers

    @staticmethod
    def _create_cookie(directive: CookieResponseDirective, headers: NormalizedDefaultDict[str, Headers]) -> SimpleCookie:
        """
        Creates a SimpleCookie object using the attributes from the CookieResponseDirective.

        Args:
            directive (CookieResponseDirective): The directive containing cookie attributes.
            headers (Dict[str, Any]): The current headers, potentially containing existing cookies.

        Returns:
            SimpleCookie: A SimpleCookie object with the cookie set according to the directive.
        """

        # Initialize the SimpleCookie object with existing cookies, if any
        if headers["cookie"]:
            cookie = headers["cookie"]
            cookie[directive.name] = directive.value
        else:
            cookie = SimpleCookie({directive.name: directive.value})

        # Set additional attributes for the specified cookie name
        if directive.path:
            cookie[directive.name]['path'] = directive.path
        if directive.expires:
            cookie[directive.name]['expires'] = directive.expires.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
        if directive.comment:
            cookie[directive.name]['comment'] = directive.comment
        if directive.domain:
            cookie[directive.name]['domain'] = directive.domain
        if directive.max_age is not None:
            cookie[directive.name]['max-age'] = directive.max_age
        if directive.secure:
            cookie[directive.name]['secure'] = 'True'
        if directive.version is not None:
            cookie[directive.name]['version'] = directive.version
        if directive.httponly:
            cookie[directive.name]['httponly'] = 'True'
        if directive.samesite:
            cookie[directive.name]['samesite'] = directive.samesite

        return cookie

    @staticmethod
    def sort_events(handler_type: ApiType) -> tuple[
        dict[str, dict[HTTPMethod | str, Type[Event] | Pattern[str]]], dict[Type[Event], dict[str, Any]], dict[str, Type[Event]]]:
        """
        Organizes API events by their URL and HTTP method for efficient lookup.

        Returns:
            A dictionary organizing events by URL and method.
        """
        sorted_event_types: dict[str, dict] = defaultdict(dict)
        event_type_extensions: dict[Type[Event], dict[str, Any]] = defaultdict(dict)
        event_names: dict[str, Type[Event]] = {}
        url_replace = compile(r"{([^}]+)}")
        for api_event in api_events:
            if handler_type in api_event.exclude:
                continue
            url_key = ""
            is_first_part = True
            url_re = ""
            for url_part in api_event.url[1:].split("/"):
                position = url_part.find("{")
                if position == -1:
                    url_key += f"/{url_part}"
                    continue
                elif is_first_part and position > 0:
                    url_key += f"/{url_part[:position]}"
                if position == 0:
                    url_re += url_replace.sub(r"(/\\b(?P<\1>[^/]*))?", url_part)
                elif position > 0 and not is_first_part:
                    url_re += url_replace.sub(fr"/{url_part[:position]}(?P<\1>[^/]+)", url_part[position:])
                elif position > 0 and is_first_part:
                    url_re += url_replace.sub(r"(?P<\1>[^/]+)", url_part[position:])
                is_first_part = False
            events = sorted_event_types[url_key]
            if url_re:
                event_type_extensions[api_event.event]["url_re"] = compile(url_key + url_re + "$")
                event_type_extensions[api_event.event]["url_original"] = api_event.url

            if api_event.event.method in events:
                raise ValueError("Method %s was already set.", api_event.event.method)
            events[api_event.event.method] = api_event.event
            event_type_extensions[api_event.event]["url"] = url_key
            event_type_extensions[api_event.event]["method"] = api_event.event.method
            event_type_extensions[api_event.event]["cookies"] = api_event.cookies
            event_type_extensions[api_event.event]["headers"] = api_event.headers
            event_type_extensions[api_event.event]["scope"] = api_event.scope
            event_type_extensions[api_event.event]["template"] = api_event.template
            event_names[api_event.event.__name__] = api_event.event

        return (dict(sorted(sorted_event_types.items(), key=lambda item: len(item[0]), reverse=True)),
                dict(sorted(event_type_extensions.items(), key=lambda item: len(item[1]["url"]), reverse=True)),
                event_names)

    def get_headers_binary(self, headers: NormalizedDefaultDict[str, Headers]) -> list[tuple[bytes, bytes]]:
        response_headers = self.get_default_headers()
        response_headers.update(headers)
        headers_list = []
        for header, values in response_headers.items():
            if header == "cookie" and isinstance(values, SimpleCookie):
                for cookie in values.values():
                    headers_list.append((b"Set-Cookie", cookie.OutputString().encode(errors="replace")))
                continue
            for value in values:
                headers_list.append((header.encode(errors="replace"), value.encode(errors="replace")))
        return headers_list

    def get_default_headers(self) -> NormalizedDefaultDict[str, Headers]:
        response_headers = NormalizedDefaultDict[str, Headers](list)
        response_headers["Access-Control-Allow-Headers"].append(
            "Accept,Accept-Language,Content-Language,Content-Type,Filename")
        response_headers["Access-Control-Allow-Origin"].extend(self.headers.get("origin", []))
        return response_headers

    async def response_error(self, status, data: bytes | None = None, *args, **kwargs: Unpack[ResponseErrorKW]) -> None:
        headers = kwargs.get("headers", None)
        if headers is None:
            headers = NormalizedDefaultDict[str, Headers](list)
        if data is None:
            data = 'No more information'.encode("utf-8")
        if "Content-Type" not in headers:
            headers["Content-Type"].append("text/html")
        await self.response(status, data, headers=headers)

    @staticmethod
    def parse_cookies(cookie: str) -> SimpleCookie[str]:
        return SimpleCookie(cookie)

    def parse_url_parameters(self) -> dict[str, Any]:
        url_parameters = parse_qs(unquote(self.scope["query_string"].decode()), keep_blank_values=True)
        return {
            camel2snake(key.strip("[]")): value if key.endswith("[]") else value[-1] for key, value in
            url_parameters.items()
        }

    def handle_multipart(self, data: BinaryIO) -> None:
        try:
            content_type = self.headers.get("content-type", [])
            if len(content_type) < 2:
                raise ValueError("Boundary not found in content-type header")
            boundary = content_type[1].split("=")[1] if "=" in content_type[1] else None
            if not boundary:
                raise ValueError("Boundary not found in content-type header")
            multipart = MultipartParser(data, boundary, charset="utf-8")
            found_files = []
            for part in multipart:
                self.logger.warning(part)
                if not (part.filename or part.content_type):
                    self.parameters[part.name] = part.file.read().decode("utf-8", errors="replace")
                else:
                    with NamedTemporaryFile(prefix=UPLOAD_FILES_PREFIX, delete=False) as received_temp_file:
                        received_temp_file.write(part.file.read())
                        received_file = File(
                            file_name=part.filename,
                            mime_type=part.content_type,
                            path=Path(received_temp_file.name),
                        )
                        found_files.append(received_file)
            if len(found_files) == 1:
                # If it's only one file, then don't return list, but only the single file
                self.parameters["path"] = found_files[0]
            elif len(found_files) > 1:
                self.parameters["path"] = found_files
        except ValueError as e:
            raise Exception("Input values not in expected format") from e
        except Exception as e:
            raise Exception("Unknown error") from e

    def handle_json(self) -> None:
        self.body.seek(0, 2)
        if self.body.tell() == 0:
            return
        self.body.seek(0)
        try:
            self.parameters.update({camel2snake(key): value for key, value in loads(self.body.read()).items()})
        except JSONDecodeError as e:
            self.logger.warning("Cannot process json data", exc_info=e)
            raise e
        except Exception as e:
            self.logger.error("Unknown error", exc_info=e)
            raise e

    def handle_url_encoded(self, data: BinaryIO) -> None:
        body_parsed = parse_qsl(
            self.body.read().decode(errors="ignore") if self.body else data.read().decode(
                errors="ignore"),
            keep_blank_values=True,
        )
        for key, value in body_parsed:
            if key.endswith("[]"):
                key = key[:-2]
                if key not in self.parameters:
                    self.parameters[key] = [value]
                else:
                    self.parameters[key].append(value)
            else:
                self.parameters[key] = value

    def handle_custom(self, data: BinaryIO) -> None:
        with NamedTemporaryFile(prefix=UPLOAD_FILES_PREFIX, delete=False) as received_temp_file:
            received_temp_file.write(data.read())
            file_name: str | None = None
            try:
                file_names = self.headers["filename"]
            except KeyError as e:
                self.logger.warning("Filename header is missing", exc_info=e)
            else:
                if len(file_names) == 1:
                    try:
                        file_name = b64decode(file_names[0]).decode(errors="replace")
                    except Error as e:
                        self.logger.warning("Filename header not in base64", exc_info=e)
                else:
                    self.logger.warning("Filename header in wrong format")

            self.parameters["file"] = File(
                file_name=file_name,
                mime_type=self.headers["content-type"][0],
                path=Path(received_temp_file.name),
            )

    async def parse_body(self) -> None:
        if not self.headers["content-type"]:
            return
        more_data = True
        while self.body.tell() < MAX_BODY_SIZE:
            body = await self.receive()
            data = body.get("body", None)
            self.body.write(data)
            if not body["more_body"]:
                if "application/json" in self.headers["content-type"]:
                    self.handle_json()
                    self.body.close()
                    return
                elif "application/x-www-form-urlencoded" in self.headers["content-type"]:
                    self.handle_url_encoded(self.body)
                    self.body.close()
                    return

                more_data = False
                break

        temporary_file = TemporaryFile(prefix=UPLOAD_FILES_PREFIX)
        self.body.seek(0)
        temporary_file.write(self.body.read())
        self.body.close()
        if more_data:
            while data := await self.receive():
                temporary_file.write(data.get("body", None))
                if not data["more_body"]:
                    break
        temporary_file.flush()
        temporary_file.seek(0)
        if "multipart/form-data" in self.headers["content-type"]:
            self.handle_multipart(temporary_file)
        else:
            self.handle_custom(temporary_file)
        temporary_file.close()

    async def response(self, status: HTTPStatus, data: bytes, *args, **kwargs: Unpack[ResponseKW]):
        headers = kwargs["headers"]
        if headers is None:
            headers = NormalizedDefaultDict(list)
        headers["Content-Length"].append(str(len(data)))
        await self.send({
            'type': 'http.response.start',
            'status': status,
            'headers': self.get_headers_binary(headers),
        })

        await self.send({
            'type': 'http.response.body',
            'body': data,
            'more_body': False
        })

    def response_error_prepare(self, status: HTTPStatus, response: bytes | dict | None) -> dict:
        data = {
            "status_code": status.value,
            "status": status.name,
            "description": status.description,
            "reasons": []
        }

        if isinstance(response, Event):
            directives = response.get_response().get_directives()
            for directive in directives:
                handler: HTTPDirectiveHandlerDict | None = self.directive_handlers().get(directive.__class__, None)
                if not handler:
                    continue
                handler_status = handler.get("status", None)
                if not handler_status:
                    continue
                if handler_status.is_client_error:
                    message = getattr(directive, "message", None)
                    if message:
                        data["reasons"].append({"message": message, "status_code": handler_status.value})
        elif isinstance(response, dict):
            data.update(response)
        return data

    async def response_assets(self, file) -> bool:
        asset_file = Path(ASSETS_PATH, file if file[0] != "/" else file[1:])
        if not asset_file.is_file():
            self.logger.warning("File not found", exc_info=True)
            return False
        mime_types = guess_type(asset_file)
        headers = NormalizedDefaultDict[str, Headers](list)
        headers["Content-Type"].append(mime_types[0] if mime_types[0] else "text/html")
        headers["Content-Length"].append(str(asset_file.lstat().st_size))

        with asset_file.open("rb") as asset_file_descriptor:
            await self.response_file(asset_file_descriptor, headers)
        return True

    async def response_file_prepare(self, event: Event, *args, **kwargs: Unpack[ResponseKW]):
        headers = kwargs["headers"]
        file_name = quote(event.response.file.file_name, encoding='utf-8')
        headers["Content-Type"].append(event.response.file.mime_type)
        headers["Content-Disposition"].append(f"attachment;filename*=UTF-8''{file_name}")
        with event.response.file.path.open("rb") as file:
            await self.response_file(file, headers)

    async def response_file(self, file: BinaryIO, headers: NormalizedDefaultDict[str, Headers]):
        try:
            await self.send({
                'type': 'http.response.start',
                'status': HTTPStatus.OK,
                'headers': self.get_headers_binary(headers),
            })
            chunk_size = 1024 * 1024
            while data := file.read(chunk_size):
                await self.send({
                    'type': 'http.response.body',
                    'body': data,
                    'more_body': len(data) == chunk_size
                })
        except Exception as e:
            self.logger.error(e, exc_info=e)

    def get_event_constructors(self):
        constructors = self.event_types().get(self.scope["path"], [])
        for event, extensions in self.event_type_extensions().items():
            url_re = extensions.get("url_re", None)
            if url_re:
                match = url_re.match(self.scope["path"])
                if match:
                    constructors.append(event)
        return constructors

    def get_event_constructor(self) -> Type[Event] | None:
        event_constructors = self.event_types().get(self.scope["path"], [])
        method = HTTPMethod(self.scope["method"])
        if not event_constructors:
            url_found = False
            for event_constructor, extensions in self.event_type_extensions().items():
                url_re = extensions.get("url_re", None)
                if not url_re:
                    continue
                url = extensions.get("url", None)
                if self.scope["path"].startswith(url):
                    match = url_re.match(self.scope["path"])
                    if match and method != extensions["method"]:
                        url_found = True
                    elif match:
                        self.parameters.update(match.groupdict())
                        return event_constructor
                    else:
                        raise ResourceWarning("Unknown url %s", self.scope["path"])

            else:
                if url_found:
                    return None
                else:
                    raise ResourceWarning("Unknown url %s", self.scope["path"])

        return event_constructors.get(method, None)

    def create_event(self, event_constructor: Type[Event]) -> Event:
        event_extension = self.event_type_extensions().get(event_constructor, None)
        if event_extension:
            headers = event_extension.get("headers", None)
            if headers:
                for event_argument, header_name in headers.items():
                    header_data = self.headers.get(header_name)
                    if not header_data:
                        position = 0
                        header_data_split = ""
                        while header_name + f".{position}" in self.headers:
                            header_data_split += self.headers.get(header_name + f".{position}")[0]
                            position += 1
                        if position > 0:
                            self.parameters[event_argument] = [header_data_split]
                            continue
                    self.parameters[event_argument] = header_data
            cookies = event_extension.get("cookies", None)
            if cookies:
                for event_argument, cookie_name in cookies.items():
                    cookie_data = self.cookies.get(cookie_name)
                    if not cookie_data:
                        position = 0
                        cookie_data_split = ""
                        while cookie_name + f".{position}" in self.cookies:
                            cookie_data_split += self.cookies.get(cookie_name + f".{position}").value
                            position += 1
                        if position > 0:
                            self.parameters[event_argument] = cookie_data_split
                            continue
                    self.parameters[event_argument] = cookie_data
            scope = event_extension.get("scope", None)
            if scope:
                self.parameters.update({k: self.scope.get(v, None) for k, v in scope.items()})
        return super().create_event(event_constructor)

    def handle_directives(self, directives: list[ResponseDirective]) -> tuple[HTTPStatus, NormalizedDefaultDict[str, Headers]]:
        status, headers = HTTPStatus.OK, NormalizedDefaultDict[str, Headers](list)
        for directive in directives:
            try:
                directive_handler = self.directive_handlers()[directive.__class__]
            except KeyError as e:
                self.logger.warning("Unknown directive: %s", directive, exc_info=e)
            else:
                if "status" in directive_handler:
                    status = directive_handler["status"]
                if "routine" in directive_handler:
                    if "headers" in directive_handler:
                        headers_demand = directive_handler["headers"]
                        partial_headers = directive_handler["routine"](directive, {k: headers[k] for k in headers_demand})
                        headers.update(partial_headers)
                    else:
                        partial_headers = directive_handler["routine"](directive)
                        for key, value in partial_headers.items():
                            headers[key].extend(value)

        return status, headers

    def convert_type(self, value: Any, annotation: Type) -> Any:
        if isinstance(value, Morsel):
            if annotation == Morsel:
                return value
            else:
                return super().convert_type(value.value, annotation)

        return super().convert_type(value, annotation)
