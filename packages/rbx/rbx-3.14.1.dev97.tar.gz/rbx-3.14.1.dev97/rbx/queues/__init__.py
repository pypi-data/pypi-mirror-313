from datetime import timedelta
from functools import wraps
import logging
import threading
import traceback
import warnings

from redis import StrictRedis
from rq import Queue as RQ, SimpleWorker, get_current_job
from rq.job import cancel_job
from rq.registry import ScheduledJobRegistry

from .scheduler import Scheduler

connection = threading.local()
logger = logging.getLogger(__name__)


class Queue:
    """The Queue provides an interface to farm out jobs to be processed asynchronously."""

    def __init__(
        self,
        name=None,
        host="0.0.0.0",
        port=6379,
        db=0,
        module=None,
        conn=None,
        is_async=True,
        no_delay=False,
    ):
        """Initialise the Job Queue.

        Parameters:
            name (str):
                An optional queue name. Defaults to "default".

            host (str):
                The Redis cluster host.
                Uses '0.0.0.0' by default.
            port (int):
                The Redis cluster port.
                Uses port 6379 by default.
            db (int):
                The Redis cluster db.
                Uses 0 by default.
            module:
                The default Queue uses either a method, or as string reference to an importable
                method.
                For string references, this paramater can be used to always load the job method
                from a specific module.

                >>> queue = Queue(module='src.tasks')
                >>> queue.enqueue('method')
                Job(function='src.tasks.method', ...)

            conn (StrictRedis):
                A redis connection may be provided instead of the host/port/db combination.
            is_async (bool):
                Set to True to skip the workers and perform the job instantly.
            no_delay (bool):
                Use this flag to cancel the scheduled/delaying feature, and enqueue a delayed job
                immediately. Useful for testing purposes.
        """
        if conn:
            connection.redis = conn
        else:
            connection.redis = StrictRedis(host=host, port=port, db=db)
        self.connection = connection.redis

        if name:
            self.queue = RQ(name, connection=self.connection, is_async=is_async)
        else:
            self.queue = RQ(connection=self.connection, is_async=is_async)

        self.module = module
        self.no_delay = no_delay

    @property
    def count(self):
        return self.queue.count

    @property
    def is_async(self):
        return self.queue.is_async

    @property
    def name(self):
        return self.queue.name

    @property
    def exception_handlers(self):
        """The handlers must be listed in order of expected execution."""
        return [self._retry_on_failure, self._requeue_job, self._move_to_failed_queue]

    @property
    def failed_queue(self):
        return self.queue.failed_job_registry

    def _move_to_failed_queue(self, job, *exc_info):
        """This handler moves the job to the failed queue."""
        exc_string = "".join(traceback.format_exception(*exc_info))
        logger.debug("Moving job to failed queue")
        self.failed_queue.add(job, ttl=job.failure_ttl, exc_string=exc_string)

        logger.debug(
            "Job {} failed <{}>.".format(job.id, job.func_name),
            exc_info=exc_info,
            extra={"arguments": job.args},
        )

    def _requeue_job(self, job, *exc_info):
        """This handler does the requeuing, according to the 'failures' meta data set by the
        previous handler.

        If the retry is given a sequence of exception types, the method will only be retried if the
        exception raised is of one of these types.

        When the maximum retry attempts has been reached, we make sure to clear the 'failures'
        flag, and move the job to the next handler in the stack (which will move it to the failed
        queue).
        """
        failures = job.meta.get("failures", 0)
        retries = job.meta.get("retries", 3)
        if "retry" not in job.meta or failures >= retries:
            job.meta.pop("failures", None)
            job.save_meta()
            return True

        exceptions = job.meta.get("exceptions")
        if exceptions and not isinstance(exc_info[1], exceptions):
            logger.debug("Un-retryable exception")
            return True

        logger.debug("Requeuing {!r}".format(job))
        self.requeue_job(job)

        return False

    def _retry_on_failure(self, job, *exc_info):
        """This handler flags jobs which are retry-able ('retry' = True) by incrementing the
        'failures' meta data.

        It will then pass on the handling of the requeuing itself to the next handler in the stack.
        If we were to requeue the job at this stage, what would happen is the job would be queued
        up before the next handler had the chance to fallback to the next, ending in an infinite
        loop of failing jobs with the same ID.

        The retry() decorator is provided to flag any method as retry-able.

        Also note that scheduled jobs do never get retried, and skip the failed queue entirely.
        They will get retried at the next run anyway.
        """
        if "scheduled" in job.meta:
            # This is a scheduled job failing. Skip the error handling.
            return False

        job.meta.setdefault("failures", 0)
        logger.debug("META: {}".format(job.meta))

        if "retry" in job.meta:
            job.meta["failures"] += 1
            logger.debug("Failures: {}".format(job.meta["failures"]))

        job.save_meta()

        return True

    def as_sync(self):
        """Return a Queue instance with the is_async flag set to False."""
        return Queue(
            conn=self.connection,
            is_async=False,
            module=self.module,
            no_delay=self.no_delay,
        )

    def cancel_job(self, job):
        """Cancel the given job."""
        cancel_job(job.id, connection=self.connection)
        job.delete()

    def cancel_jobs(self, job_ids):
        """Cancel of bunch of jobs given their IDs."""
        for job_id in job_ids:
            self.cancel_job(self.fetch_job(job_id))

    def empty(self):
        """Empty all queues."""
        self.queue.empty()

        for job_id in self.failed_queue.get_job_ids():
            job = self.queue.fetch_job(job_id=job_id)
            self.failed_queue.remove(job)

        self.cancel_jobs([job.id for job in self.get_scheduled_jobs()])

    def enqueue(self, function, *args, enqueue_in=None, **kwargs):
        """Register a job to be processed.

        Parameters:
            function (str|function):
                A function, or a string reference to a function. If self.module is set, it is used
                as the default location for looking up method names.
            enqueue_in (int):
                By default, jobs are scheduled to be executed as soon as a worker is available. The
                execution can be further delayed by specifying how to long to wait. The value is
                expressed in seconds.
            args (tuple):
                The positional arguments to pass on to the function.
            kwargs (dict):
                The keyword arguments to pass on to the function.

        Returns:
            The job to be executed.
        """
        if self.module and isinstance(function, str):
            function = f"{self.module}.{function}"

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning, module="rq")

            if (
                enqueue_in
                and isinstance(enqueue_in, int)
                and self.is_async
                and not self.no_delay
            ):
                logger.debug(
                    f"Job scheduled in {enqueue_in}s: {function}, {args}, {kwargs}"
                )
                return self.queue.enqueue_in(
                    timedelta(seconds=enqueue_in), function, *args, **kwargs
                )
            else:
                logger.debug(f"Job queued: {function}, {args}, {kwargs}")
                return self.queue.enqueue(function, *args, **kwargs)

    def fetch_job(self, job_id):
        """Fetch a job for a Job ID."""
        return self.queue.fetch_job(job_id)

    def get_jobs(self, *args, **kwargs):
        """Get all jobs."""
        return self.queue.get_jobs(*args, **kwargs)

    def get_scheduled_jobs(self):
        """Get all scheduled jobs."""
        registry = ScheduledJobRegistry(queue=self.queue)
        return [self.fetch_job(job_id=job_id) for job_id in registry.get_job_ids()]

    def get_worker(self, *args, **kwargs):
        """Return an instance of a worker."""

        class Worker(SimpleWorker):
            def work(self, *args, **kwargs):
                with warnings.catch_warnings():
                    warnings.filterwarnings(
                        "ignore", category=DeprecationWarning, module="rq"
                    )
                    super().work(*args, **kwargs)

        return Worker(
            [self.queue],
            *args,
            connection=self.connection,
            disable_default_exception_handler=True,
            exception_handlers=self.exception_handlers,
            **kwargs,
        )

    def requeue_failed_job(self, job_id):
        """Requeue a failed job to its original queue."""
        logger.debug("Requeuing job {}".format(job_id))
        self.failed_queue.requeue(job_id)

    def requeue_failed_jobs(self, job_ids):
        """Requeue of bunch of failed jobs given their IDs."""
        for job_id in job_ids:
            self.requeue_failed_job(job_id)

    def requeue_job(self, job):
        """Requeue a job that is due to be re-tried after a failure.

        These jobs are pushed back into the queue without having made it to the failed queue.

        The requeue_job method provided by the Queue class does not keep the meta data, which we
        use to check how often the job has been tried. We therefore requeue these jobs by enqueing
        the original signature, including the meta data and the original Job ID.
        """
        self.queue.enqueue(
            job.func, args=job.args, kwargs=job.kwargs, job_id=job.id, meta=job.meta
        )

    def with_no_delay(self):
        """Return a Queue instance with the no_delay flag set to True."""
        return Queue(
            conn=self.connection,
            is_async=self.is_async,
            module=self.module,
            no_delay=True,
        )


def retry(exceptions=None, max_retries=3):
    """Decorator used to move a failing job back into the queue.

    Parameters:
        exceptions (Exception):
            An exception type, or a tuple of types, used to determine whether, when raised from
            within a job, the method should be considered retryable.

            e.g.:
            >>> retry(exceptions=ValueError)
            >>> retry(exceptions=(TransientError, ValueError))

        max_retries (int):
            The number of attempts before giving up. Defaults to 3.
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            job = get_current_job(connection=connection.redis)
            job.meta["retry"] = True
            job.meta["retries"] = max_retries
            job.meta["exceptions"] = exceptions
            job.save()

            return function(*args, **kwargs)

        return wrapper

    return decorator


__all__ = ["get_current_job", "Queue", "retry", "Scheduler"]
