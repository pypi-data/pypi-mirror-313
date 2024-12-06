import uuid
import requests_mock
from pythonik.client import PythonikClient

from pythonik.models.metadata.views import ViewMetadata
from pythonik.models.mutation.metadata.mutate import (
    UpdateMetadata,
    UpdateMetadataResponse,
)
from pythonik.models.search.search_body import Filter, SearchBody, SortItem, Term
from pythonik.specs.metadata import (
    ASSET_METADATA_FROM_VIEW_PATH,
    UPDATE_ASSET_METADATA,
    MetadataSpec,
)
from pythonik.specs.search import SEARCH_PATH, SearchSpec


def test_search_assets():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())

        # needs model
        params = {"generate_signed_url": "true", "generate_signed_download_url": "true"}

        # search criteria
        search_chriteria = SearchBody()
        search_chriteria.doc_types = ["assets"]
        search_chriteria.query = f"id:{asset_id}"

        search_chriteria.filter = Filter(
            operator="AND", terms=[Term(name="status", value="active")]
        )
        # get only active assets

        search_chriteria.sort = [SortItem(name="date_created", order="desc")]

        mock_address = SearchSpec.gen_url(SEARCH_PATH)
        m.post(mock_address, json=search_chriteria.model_dump())
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.search().search(search_chriteria, params=params)
