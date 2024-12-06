from typing import Optional
from pythonik.models.jobs.job_body import JobBody


class JobResponse(JobBody):
    id: Optional[str] = ""
