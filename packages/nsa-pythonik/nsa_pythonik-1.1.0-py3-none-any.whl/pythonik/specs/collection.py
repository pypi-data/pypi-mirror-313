from pythonik.specs.base import Spec
from pythonik.models.base import Response
from pythonik.models.assets.collections import (
    Collection,
    CollectionContents,
    CollectionContentInfo,
    Content,
    AddContentResponse
)

BASE = "collections"
GET_URL = BASE + "/{}/"
GET_INFO = GET_URL + "content/info"
GET_CONTENTS = GET_URL + "contents"
POST_CONTENT = GET_CONTENTS


class CollectionSpec(Spec):
    server = "API/assets/"

    def delete(self, collection_id: str) -> Response:
        """
        Delete a collection

        Args:
            collection_id: The ID of the collection to delete

        Returns:
            Response with no data model (202 status code)

        Required roles:
            - can_delete_collections

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Collection does not exist
        """
        resp = self._delete(GET_URL.format(collection_id))
        return self.parse_response(resp, None)

    def get(self, collection_id: str) -> Response:
        """
        Retrieve a specific collection by ID

        Args:
            collection_id: The ID of the collection to retrieve

        Returns:
            Response(model=Collection)

        Required roles:
            - can_read_collections

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Collection does not exist
        """
        resp = self._get(GET_URL.format(collection_id))
        return self.parse_response(resp, Collection)

    def get_info(self, collection_id: str) -> Response:
        """
        Returns all sub-collections and assets count for a specific collection

        Args:
            collection_id: The ID of the collection to retrieve

        Response:
            Response(model=CollectionContentInfo)

        Required roles:
            - can_read_collections

        Raise:
            - 400 Bad request
            - 401 Token is invalid
        """
        resp = self._get(GET_INFO.format(collection_id))
        return self.parse_response(resp, CollectionContentInfo)

    def get_contents(self, collection_id: str, **kwargs) -> Response:
        """
        Retrieve the contents of a specific collection

        Args:
            collection_id: The ID of the collection
            kwargs: additional kwargs passed to the request

        Returns:
            Response(model=CollectionContents)

        Required roles:
            - can_read_collections
        
        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Collection does not exist
        """
        resp = self._get(GET_CONTENTS.format(collection_id), **kwargs)
        return self.parse_response(resp, CollectionContents)

    def create(self, body: Collection, exclude_defaults=True, **kwargs) -> Response:
        """
        Create a new collection

        Args:
            body: collection creation parameters
            exclude_defaults: If True, exclude default values from request
            kwargs: additional kwargs passed to the request
        
        Returns:
            Response(model=Collection)
        
        Required roles:
            - can_create_collections
        
        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        response = self._post(
            BASE, json=body.model_dump(exclude_defaults=exclude_defaults), **kwargs
        )
        return self.parse_response(response, Collection)
    
    def add_content(
        self, collection_id: str, body: Content, exclude_defaults=True, **kwargs
    ):
        """Add an object to a collection.


        Args:
            collection_id (str): The ID of the collection to add content to
            body (Content): The content object containing object_id and object_type
            exclude_defaults (bool, optional): Whether to exclude default values from the request. Defaults to True.
            **kwargs: Additional keyword arguments to pass to the request

        Returns:
            Response[Collection]: The updated collection object

        Response Codes:
            201: Content added successfully
            400: Bad request
            401: Token is invalid
            404: Collection not found
        """
        response = self._post(
            POST_CONTENT.format(collection_id),
            json=body.model_dump(exclude_defaults=exclude_defaults),
            **kwargs,
        )
        print(f"response: {response.json()}")
        return self.parse_response(response, AddContentResponse)
