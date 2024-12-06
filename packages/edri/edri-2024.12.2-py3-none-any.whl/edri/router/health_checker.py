from datetime import datetime, timedelta
from logging import getLogger
from multiprocessing.connection import Connection
from multiprocessing.queues import Queue
from typing import Optional

from edri.abstract import ManagerBase
from edri.config.constant import HEALTH_CHECK_STORE
from edri.config.setting import HEALTH_CHECK_TIMEOUT
from edri.dataclass.directive.base import InternalServerErrorResponseDirective
from edri.dataclass.event import Event
from edri.dataclass.health_checker import Record, Status
from edri.dataclass.response import ResponseStatus
from edri.events.edri.router import HealthCheck, HealthCheckStatus
from edri.events.edri.scheduler import Set as SchedulerSet


class HealthChecker:
    """
    Monitors and records the health status of components within the system, scheduling regular
    health checks and storing the results for analysis and system management.

    Attributes:
        router_queue (Queue[Event]): The messaging queue used to communicate with the scheduler and store.
        logger (Logger): Logger instance for logging health check operations and outcomes.
        statuses (Dict[str, Record]): A dictionary storing the health status records for each component.
        last_check (Optional[datetime]): The timestamp of the last initiated health check cycle.
        components (Set[ManagerBase]): A set of component instances that are monitored by the HealthChecker.
    """

    def __init__(self, router_queue: Queue[Event], components: set[ManagerBase]) -> None:
        """
        Initializes the HealthChecker with a set of components to monitor and the queue for communication.

        :param router_queue: The messaging queue used to communicate with the scheduler and store.
        :type router_queue: Queue[Event]
        :param components: A set of component instances that are monitored by the HealthChecker.
        :type components: Set[ManagerBase]
        """
        self.router_queue = router_queue
        self.logger = getLogger(__name__)
        self.statuses: dict[str, Record] = {}
        self.last_check: Optional[datetime] = None
        self.components = components
        self.set_task()

    def set_task(self) -> None:
        """
        Schedules the health check operation at a regular interval defined by ``HEALTH_CHECK_TIMEOUT``.
        """
        scheduler_set = SchedulerSet(
            event=HealthCheck(),
            when=datetime.now() + timedelta(seconds=HEALTH_CHECK_TIMEOUT),
            repeat=timedelta(seconds=HEALTH_CHECK_TIMEOUT),
            identifier=f"{self.__class__.__name__}Task"
        )
        self.router_queue.put(scheduler_set)

    def component_add(self, name: str, pipe: Connection) -> None:
        """
        Registers a new component for health monitoring.

        :param name: The name of the component to add.
        :type name: str
        :param pipe: The connection associated with the component.
        :type pipe: Connection
        """
        if name not in self.statuses:
            found = None
            for component in self.components:
                if component.name == name:
                    found = component
                    break
            self.statuses[name] = Record(name, pipe, found)
            self.logger.debug("Manager was added %s %s", name, pipe)

    def control_start(self) -> None:
        """
        Marks the start of a health check cycle, updating records and preparing for result collection.
        """
        if self.last_check:
            self.check_status()
        self.last_check = datetime.now()

    def control_result(self, event: HealthCheck) -> None:
        """
        Records the health check result for a specific component.

        :param name: The name of the component that was checked.
        :type name: str
        :param status: The health status returned by the component.
        :type status: ResponseStatus
        """
        self.logger.debug("Add status record to %s - %s", event.response.name, event.response.status)
        record = self.statuses[event.response.name]
        record.timestamp = datetime.now()
        record.status = event.response.status

    def check_status(self) -> None:
        """
        Compiles and stores the health status of all monitored components.
        """
        now = datetime.now()
        for name, record in self.statuses.items():
            if (record.timestamp + timedelta(seconds=HEALTH_CHECK_TIMEOUT * 4)) < now:
                self.logger.error(
                    "%s did not send a status message 3x - last status %s - %s",
                    record.name, record.status, record.event
                )
                record.status = Status.ERROR
            elif (record.timestamp + timedelta(seconds=HEALTH_CHECK_TIMEOUT * 2)) < now:
                self.logger.warning(
                    "%s did not send a status message - last status %s - %s",
                    record.name, record.status, record.event
                )
                record.status = Status.WARNING


    def restart_component(self, pipe: Connection, time: datetime) -> None:
        """
        Attempts to restart a component that is not responding or is reported to have issues.

        :param pipe: The connection associated with the component to restart.
        :type pipe: Connection
        :param time: The timestamp indicating when the restart was initiated.
        :type time: datetime
        """
        self.logger.warning("Restarting component")
        for name, component in self.statuses.items():
            if component.pipe == pipe:
                if component.definition:
                    component.status = Status.WARNING
                    component.definition.__class__(router_queue=self.router_queue, from_time=time).start()
                    self.logger.info("Component restarted")
                else:
                    component.status = Status.ERROR
                    self.logger.error("Component was found - definition was missing")
                del self.statuses[name]
                break
        else:
            self.logger.error("Component was not found")

    def send_status(self, event: HealthCheckStatus):
        event.response.statuses = [Record(name=record.name, timestamp=record.timestamp, status=record.status) for name, record in self.statuses.items()]
        event.response.set_status(ResponseStatus.OK)
        self.router_queue.put(event)
