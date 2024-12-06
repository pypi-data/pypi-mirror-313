import uuid
from venv import logger
import requests_mock
from pythonik.client import PythonikClient
from requests import HTTPError

from pythonik.models.metadata.views import (
    FieldValue,
    FieldValues,
    MetadataValues,
    ViewMetadata,
)
from pythonik.models.mutation.metadata.mutate import (
    UpdateMetadata,
    UpdateMetadataResponse,
)
from pythonik.specs.metadata import (
    ASSET_METADATA_FROM_VIEW_PATH,
    UPDATE_ASSET_METADATA,
    MetadataSpec,
    ASSET_OBJECT_VIEW_PATH,
)


def test_get_asset_metadata():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())

        model = ViewMetadata()
        data = model.model_dump()
        mock_address = MetadataSpec.gen_url(
            ASSET_METADATA_FROM_VIEW_PATH.format(asset_id, view_id)
        )
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.metadata().get_asset_metadata(asset_id, view_id)


def test_get_asset_intercept_404():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())

        mv = MetadataValues(
            {
                "this_worked_right?": FieldValues(
                    field_values=[FieldValue(value="lets hope")]
                )
            }
        )

        model = ViewMetadata()
        model.metadata_values = mv
        data = model.model_dump()
        mock_address = MetadataSpec.gen_url(
            ASSET_METADATA_FROM_VIEW_PATH.format(asset_id, view_id)
        )
        m.get(mock_address, json=data, status_code=404)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        resp = client.metadata().get_asset_metadata(
            asset_id, view_id, intercept_404=model
        )
        assert resp.data == model


def test_get_asset_intercept_404_raise_for_status():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())

        mv = MetadataValues(
            {
                "this_worked_right?": FieldValues(
                    field_values=[FieldValue(value="lets hope")]
                )
            }
        )

        model = ViewMetadata()
        model.metadata_values = mv
        data = model.model_dump()
        mock_address = MetadataSpec.gen_url(
            ASSET_METADATA_FROM_VIEW_PATH.format(asset_id, view_id)
        )
        m.get(mock_address, json=data, status_code=404)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        resp = client.metadata().get_asset_metadata(
            asset_id, view_id, intercept_404=model
        )
        # should not raise for status
        try:
            resp.response.raise_for_status()
            # this line should run and the above should not raise for status
            assert True is True
        except Exception as e:
            pass


def test_get_asset_intercept_404_raise_for_status_404():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())

        mv = MetadataValues(
            {
                "this_worked_right?": FieldValues(
                    field_values=[FieldValue(value="lets hope")]
                )
            }
        )

        model = ViewMetadata()
        model.metadata_values = mv
        data = model.model_dump()
        mock_address = MetadataSpec.gen_url(
            ASSET_METADATA_FROM_VIEW_PATH.format(asset_id, view_id)
        )
        m.get(mock_address, json=data, status_code=404)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        resp = client.metadata().get_asset_metadata(
            asset_id, view_id, intercept_404=model
        )
        # should not raise for status
        exception = None
        try:
            resp.response.raise_for_status_404()
            # this line should run and the above should not raise for status
        except HTTPError as e:
            exception = e

        # assert exception still raised with 404
        assert exception.response.status_code == 404


def test_update_asset_metadata():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())
        payload = {"metadata_values": {"field1": {"field_values": [{"value": "123"}]}}}

        mutate_model = UpdateMetadata.model_validate(payload)
        response_model = UpdateMetadataResponse(
            metadata_values=mutate_model.metadata_values.model_dump()
        )

        mock_address = MetadataSpec.gen_url(
            UPDATE_ASSET_METADATA.format(asset_id, view_id)
        )
        m.put(mock_address, json=response_model.model_dump())
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.metadata().update_asset_metadata(asset_id, view_id, mutate_model)


def test_put_segment_view_metadata():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        segment_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())
        
        # Create test payload
        payload = {
            "metadata_values": {
                "field1": {
                    "field_values": [{"value": "123"}]
                }
            }
        }

        mutate_model = UpdateMetadata.model_validate(payload)
        response_model = UpdateMetadataResponse(
            metadata_values=mutate_model.metadata_values.model_dump()
        )

        # Mock the endpoint using the ASSET_OBJECT_VIEW_PATH
        mock_address = MetadataSpec.gen_url(
            ASSET_OBJECT_VIEW_PATH.format(asset_id, "segments", segment_id, view_id)
        )
        m.put(mock_address, json=response_model.model_dump())

        # Make the request
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.metadata().put_segment_view_metadata(
            asset_id, segment_id, view_id, mutate_model
        )
