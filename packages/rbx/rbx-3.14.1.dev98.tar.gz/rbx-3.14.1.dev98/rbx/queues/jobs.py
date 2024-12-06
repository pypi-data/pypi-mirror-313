"""
Helper module to represent scheduled jobs.
"""


class JobSpec:
    """
    Represents a job spec.

    This is a Value Object, and doesn't convey any logic.
    All this does is some very limited field checking.
    """

    fields = ("task", "args", "kwargs", "schedule", "timeout")

    def __init__(self, name, fields):
        if not all([rv in fields.keys() for rv in ("task", "schedule")]):
            raise AttributeError("These fields are required: {}".format(self.fields))

        job_spec = dict([(k, v) for k, v in fields.items() if k in self.fields])
        if "args" not in job_spec.keys():
            job_spec["args"] = ()
        if "kwargs" not in job_spec.keys():
            job_spec["kwargs"] = {}
        if "timeout" not in job_spec.keys():
            job_spec["timeout"] = None

        self.__dict__ = job_spec

    def __str__(self):
        return "{schedule} {task}".format(**self.__dict__)

    def __repr__(self):
        return "<JobSpec [{}]>".format(str(self))


class Jobs(dict):
    """Iterable of JobSpecs."""

    def __setitem__(self, key, value):
        spec = JobSpec(key, value)
        super().__setitem__(key, spec)

    @staticmethod
    def from_dict(jobs_as_dict):
        """
        Constructor that creates a Jobs instance from a dictionary.
        The dict is expected to have be valid and have the following format:

        >>> {
        >>>     'job_name': {
        >>>         'task': 'full.path.to.method',
        >>>         'args': (1, 'arg2'),
        >>>         'kwargs': {'kw1': 'value1'}
        >>>         'schedule': 'CRON expression',
        >>>         'timeout': 180,
        >>>     },
        >>>     ...
        >>> }

        """
        jobs = Jobs()
        for key, value in jobs_as_dict.items():
            jobs[key] = value
        return jobs
