from pythonik.client import PythonikClient
import requests_mock
import uuid

from pythonik.models.jobs.job_body import JobBody, JobStatus, JobTypes
from pythonik.specs.jobs import CREATE_JOB_PATH, UPDATE_JOB_PATH, JobSpec


def test_create_job():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        # job_id = str(uuid.uuid4())

        model = JobBody()

        model.title = "The custom job"
        model.type = JobTypes.CUSTOM.value
        model.status = JobStatus.STARTED.value

        data = model.model_dump()
        mock_address = JobSpec.gen_url(CREATE_JOB_PATH)

        m.post(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)

        client.jobs().create(model)


def test_update_job():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        job_id = str(uuid.uuid4())

        model = JobBody()
        model.title = "The custom job update"
        model.status = JobStatus.FINISHED.value

        data = model.model_dump()
        mock_address = JobSpec.gen_url(UPDATE_JOB_PATH.format(job_id))

        m.patch(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)

        client.jobs().update(job_id, model)
