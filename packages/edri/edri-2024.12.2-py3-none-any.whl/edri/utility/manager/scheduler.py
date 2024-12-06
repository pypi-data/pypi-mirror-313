from dataclasses import dataclass
from datetime import datetime, timedelta
from logging import getLogger
from multiprocessing.queues import Queue
from typing import Optional

from edri.abstract import ManagerBase
from edri.dataclass.event import Event
from edri.dataclass.response import ResponseStatus
from edri.events.edri.scheduler import Set, Update, Cancel
from edri.config.constant import SCHEDULER_TIMEOUT_MAX
from edri.utility import Storage


@dataclass
class Job:
    """
    Represents a scheduled task within the system.

    Attributes:
        event (Event): The event to be triggered when the job is executed.
        when (datetime): The specific time at which the job should be executed.
        repeat (Union[timedelta, bool]): Indicates how often the job should repeat.
            If False, the job does not repeat. If a timedelta, it repeats at the interval
            specified by the timedelta.
    """
    event: Event
    when: datetime
    repeat: Optional[timedelta] = None


class Scheduler(ManagerBase):
    """
    A scheduler for managing and executing timed tasks based on the Job dataclass.
    Inherits from ManagerBase to utilize a common management infrastructure for
    event processing.

    Attributes:
        jobs (Storage[Job]): A storage for managing jobs. Initialized as None and
        should be set to a Storage instance before starting the scheduler.
        initial_jobs (list[Job]): A list of jobs to be initially loaded into the
        scheduler upon start.

    Methods:
        after_start(): Initializes the jobs storage and loads initial jobs.
        solve_req_set(event: Set): Handles requests to set (schedule) new jobs.
        solve_req_update(event: Update): Handles requests to update existing jobs.
        solve_req_cancel(event: Cancel): Handles requests to cancel existing jobs.
        get_next_job(): Retrieves the next job to be executed, based on its scheduled time.
        run_pending(): Executes pending jobs based on the current time and schedules
        repeat executions if necessary.
        run_resolver(): Continuously checks for and executes pending jobs, and listens
        for incoming job management requests.
    """
    def __init__(self, router_queue: "Queue[Event]", jobs: list[Job]) -> None:
        """
         Initializes the Scheduler instance with a router queue and an initial list
         of jobs.

         Parameters:
             router_queue (Queue): The multiprocessing queue for receiving and routing
             events.
             jobs (list[Job]): An initial list of jobs to be scheduled upon startup.
         """
        super().__init__(router_queue, getLogger(__name__))
        self.jobs: Storage[Job]
        self.initial_jobs = jobs

    def after_start(self) -> None:
        """
        Prepares the scheduler for operation by initializing the jobs storage and
        loading the initial jobs.
        """
        self.jobs = Storage()
        for job in self.initial_jobs:
            self.jobs.append(job)

    def solve_req_set(self, event: Set) -> None:
        """
        Processes a request to schedule a new job. Adds the job to the scheduler's
        storage and assigns it a unique identifier. If the identifier is not None, there is no response made.

        Parameters:
            event (Set): An event containing the details of the job to be scheduled,
            including the event to trigger, when to trigger it, and whether it should
            repeat.

        Returns:
            None: This method does not return a value but updates the event's response
            with the identifier of the scheduled job.
        """
        try:
            key = self.jobs.append(Job(event.event, event.when, event.repeat), event.identifier)
        except KeyError as e:
            self.logger.warning("Scheduled task already exists: %s", event.identifier, exc_info=e)
            return

        if not event.identifier:
            event.response.identifier = key
        self.logger.debug("New scheduled task: %s", key)

    def solve_req_update(self, event: Update) -> None:
        """
        Processes a request to update an existing job. Allows updating the job's
        event, execution time, and repetition interval.

        Parameters:
            event (Update): An event containing the job's identifier and the new
            values for the events, execution time, and/or repetition interval.

        Returns:
            None: Updates the specified job and modifies the event's response status
            accordingly.
        """
        job = self.jobs.get(event.identifier, None)
        if not job:
            event.response.set_status(ResponseStatus.FAILED)
            self.logger.debug("Scheduled task %s was not found", event.identifier)
            return
        if event.event is not None:
            job.event = event.event
        if event.when is not None:
            job.when = event.when
        if event.repeat is not None:
            job.repeat = event.repeat
        event.response.set_status(ResponseStatus.OK)
        self.logger.debug("Scheduled task %s was updated", event.identifier)

    def solve_req_cancel(self, event: Cancel) -> None:
        """
        Processes a request to cancel an existing job. Removes the job from the
        scheduler's storage.

        Parameters:
            event (Cancel): An event containing the identifier of the job to be
            cancelled.

        Returns:
            None: Removes the specified job and modifies the event's response status
            accordingly.
        """
        try:
            del self.jobs[event.identifier]
        except KeyError:
            event.response.set_status(ResponseStatus.FAILED)
            self.logger.debug("Scheduled task %s was not found", event.identifier)
            return

        event.response.set_status(ResponseStatus.OK)
        self.logger.debug("Scheduled task %s was cancelled", event.identifier)

    def get_next_job(self) -> tuple[str, Optional[Job]]:
        """
        Identifies the next job that is scheduled to be executed.

        Returns:
            Optional[tuple[str, Job]]: A tuple containing the identifier of the next
            job and the job itself, if any jobs are scheduled; None otherwise.
        """
        if not self.jobs:
            return "", None
        if len(self.jobs) == 1:
            return next(iter(self.jobs.items()))
        jobs = iter(self.jobs.items())
        next_key, next_job = next(jobs)
        for key, job in jobs:
            if next_job.when > job.when:
                next_job = job
                next_key = key
        return next_key, next_job

    def run_pending(self) -> None:
        """
        Checks for and executes any jobs that are due to be run. If a job is set
        to repeat, it reschedules the job based on its repetition interval.

        Returns:
            None
        """
        now = datetime.now()
        for key, job in list(self.jobs.items()):
            if now >= job.when:
                self.router_queue.put(job.event)
                if job.repeat:
                    job.when = job.when + job.repeat
                else:
                    self.logger.debug("Scheduled task %s was completed", key)
                    del self.jobs[key]

    def run_resolver(self) -> None:
        """
        The main loop of the scheduler. Continuously checks for and executes pending
        jobs, listens for job management requests, and adjusts wait times dynamically
        based on the schedule.

        Returns:
            None
        """
        while True:
            try:
                self.run_pending()
                self.logger.debug("Count of scheduled task: %s", len(self.jobs))
                key, next_job = self.get_next_job()
                if not next_job:
                    timeout = SCHEDULER_TIMEOUT_MAX
                else:
                    now = datetime.now()
                    timeout = (next_job.when - now).total_seconds()
                    if timeout > SCHEDULER_TIMEOUT_MAX:
                        timeout = SCHEDULER_TIMEOUT_MAX
                    self.logger.debug("Next scheduled task %s will be executed after %ss", key, timeout)
                if self.router_pipe.poll(timeout=timeout):
                    event = self.router_pipe.recv()
                    self.logger.debug("Received event: %s", event)
                    self.resolve(event)
            except KeyboardInterrupt:
                return
