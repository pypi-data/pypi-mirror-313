import logging
import warnings

from rq_scheduler import Scheduler as RQScheduler

from .jobs import Jobs

logger = logging.getLogger(__name__)


class Scheduler(RQScheduler):
    def __init__(self, queue, interval=60):
        """Initialise the Job Scheduler.

        Parameters:
            queue (rbx.queue.Queue):
                The queue scheduled jobs will be submitted to.
            interval (int):
                How often the scheduler checks for new jobs to add to the queue (in seconds, can
                be floating-point for more precision).
                Defaults to 60 seconds.

        """
        super().__init__(connection=queue.queue.connection, interval=interval)

    def register_death(self):
        """Extend what is executed when death is coming.

        More specifically, make sure all scheduled jobs are cancelled.
        They will be re-created upon re-birth.
        """
        super().register_death()

        for job in self.get_jobs():
            logger.debug("Removing {!r}".format(job))
            self.cancel(job)

    def register_jobs_from_settings(self, schedules):
        """Given a set of scheduled jobs, register them."""
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning, module="rq")
            for job in Jobs.from_dict(schedules).values():
                logger.debug("Scheduling {!r}".format(job))
                self.cron(
                    cron_string=job.schedule,
                    func=job.task,
                    args=job.args,
                    kwargs=job.kwargs,
                    meta={"scheduled": True},
                    timeout=job.timeout,
                )
