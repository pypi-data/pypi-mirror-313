from enum import Enum
from pythonik.models.base import Response
from pythonik.models.jobs.job_body import JobBody
from pythonik.models.jobs.job_response import JobResponse
from pythonik.specs.base import Spec


CREATE_JOB_PATH = "jobs/"
UPDATE_JOB_PATH = "jobs/{}"


class JobSpec(Spec):
    server = "API/jobs/"

    def create(self, body: JobBody, exclude_defaults=True, **kwargs) -> Response:
        """
        Create a job
        """

        resp = self._post(
            CREATE_JOB_PATH,
            json=body.model_dump(exclude_defaults=exclude_defaults),
            **kwargs
        )

        return self.parse_response(resp, JobResponse)

    def update(
        self, job_id: str, body: JobBody, exclude_defaults=True, **kwargs
    ) -> Response:
        """
        update a job
        """

        resp = self._patch(
            UPDATE_JOB_PATH.format(job_id),
            json=body.model_dump(exclude_defaults=exclude_defaults),
            **kwargs
        )

        return self.parse_response(resp, JobResponse)
