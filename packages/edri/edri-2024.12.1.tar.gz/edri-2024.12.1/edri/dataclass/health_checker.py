from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from multiprocessing.connection import Connection
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from edri.abstract import ManagerBase


class Status(Enum):
    OK = auto()


@dataclass
class Record:
    """
    Represents the health status of a system component.

    Attributes:
        name (str): The name of the component.
        pipe (Connection): A connection object used for communicating with the component.
        definition (Optional[ManagerBase]): The class definition of the component, if available.
        timestamp (datetime): The timestamp of the last health check.
        status (Optional[int]): The health status returned by the component, typically aligning
            with HTTP status codes or custom application-defined codes.
        event (Optional[str]): Additional event or information about the component's health.
    """
    name: str
    pipe: Connection
    definition: Optional["ManagerBase"] = None
    timestamp: datetime = datetime.now()
    status: Optional[Status] = None
    event: Optional[str] = None
