from urllib.parse import urljoin

from pydantic import BaseModel
from requests import Request, Response, Session

from pythonik.models.base import Response as PythonikResponse


class Spec:
    server: str = ""
    api_version = "v1"
    base_url = f"https://app.iconik.io"

    def __init__(self, session: Session, timeout: int = 3):
        self.session = session
        self.timeout = timeout

    @staticmethod
    def parse_response(response: Response, model: BaseModel) -> PythonikResponse:
        """
        Return an ErrorResponse object if the response error code is >=400, an instance of "model", or the status code
        """
        # try to populate the model
        if response.ok:
            print(response.text)
            if model:
                data = response.json()
                model = model.model_validate(data)

        # else we just let the dev decide what to do
        # can call resp.raise_for_status
        return PythonikResponse(response=response, data=model)

    @classmethod
    def gen_url(cls, path):
        url = urljoin(cls.server, f"{cls.api_version}/")
        url = urljoin(cls.base_url, url)
        return urljoin(url, path)

    def send_request(self, method, path, **kwargs) -> Response:
        """
        Send an http request to a particular URL with a particular method and arguments
        """

        url = self.gen_url(path)
        print(url)
        request = Request(
            method=method, url=url, headers=self.session.headers, **kwargs
        )
        prepped_request = self.session.prepare_request(request)
        response = self.session.send(prepped_request, timeout=self.timeout)

        return response

    def _delete(self, path, **kwargs):
        """DELETE http request"""
        return self.send_request("DELETE", path, **kwargs)

    def _get(self, path, **kwargs):
        """GET http request"""
        return self.send_request("GET", path, **kwargs)

    def _patch(self, path, **kwargs):
        """PATCH http request"""
        return self.send_request("PATCH", path, **kwargs)

    def _post(self, path, **kwargs):
        """POST http request"""
        return self.send_request("POST", path, **kwargs)

    def _put(self, path, **kwargs):
        """PUT http request"""
        return self.send_request("PUT", path, **kwargs)
