from dataclasses import dataclass, field
from multiprocessing import Process
from multiprocessing.connection import Connection
from threading import Thread
from typing import Union, Type, Dict

from edri.dataclass.event import Event


@dataclass
class Worker:
    pipe: Connection
    event: Event
    worker: Union[Thread, Process]
    streams: Dict[Type[Event], str] = field(default_factory=dict)
