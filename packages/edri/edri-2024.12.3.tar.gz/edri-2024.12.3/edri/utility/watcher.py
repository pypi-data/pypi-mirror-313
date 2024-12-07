from dataclasses import dataclass
from inspect import getfile
from logging import Logger, getLogger
from multiprocessing import Queue
from threading import Timer
from typing import Type

from watchdog.events import FileSystemEventHandler, FileModifiedEvent, DirModifiedEvent
from watchdog.observers import Observer

from edri.abstract import ManagerBase
from edri.config.setting import ENVIRONMENT
from edri.events.edri.manager import Restart


@dataclass
class WatcherHandlerComponent:
    type: Type[ManagerBase]
    timer: Timer | None = None


class WatcherHandler(FileSystemEventHandler):
    def __init__(self, components: dict[str, Type[ManagerBase]], router_queue: Queue, logger: Logger):
        self.router_queue = router_queue
        self.components: dict[str, WatcherHandlerComponent] = {path: WatcherHandlerComponent(component) for path, component in
                                                               components.items()}
        self.logger = logger
        self.delay = 1 if ENVIRONMENT == "development" else 10

    def on_modified(self, event: FileModifiedEvent | DirModifiedEvent):
        if isinstance(event, FileModifiedEvent):
            component = self.components[event.src_path]
            self.logger.debug("Manager %s was changed", component.type.__name__)
            if component.timer is not None:
                self.logger.debug("Resetting timer: %s", component.type.__name__)
                component.timer.cancel()
            component.timer = Timer(self.delay, self._send_restart_event, args=(component.type,))
            component.timer.start()

    def _send_restart_event(self, manager_type: Type[ManagerBase]):
        self.logger.info("Restart event queued for manager: %s", manager_type.__name__)
        restart = Restart(manager=manager_type)
        self.router_queue.put(restart)

    def quit(self):
        for component in self.components.values():
            if component.timer:
                component.timer.cancel()


class Watcher:
    def __init__(self, router_queue: Queue, components: set[ManagerBase]) -> None:
        self.router_queue = router_queue
        self.logger = getLogger(__name__)
        self.observer = Observer()
        components = {getfile(component.__class__): component.__class__ for component in components}
        handler = WatcherHandler(components, self.router_queue, self.logger)
        for path in components.keys():
            self.observer.schedule(handler, path)
        self.observer.start()

    def quit(self) -> None:
        self.observer.stop()
