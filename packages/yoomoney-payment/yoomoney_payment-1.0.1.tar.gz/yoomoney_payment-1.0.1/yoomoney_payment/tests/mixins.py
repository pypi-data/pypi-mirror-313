import os

import requests
from rest_framework import status


class MockResponseMixin:
    @staticmethod
    def _get_response(file_name, extension="json"):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir_path, "response/{}.{}".format(file_name, extension))
        with open(file_path) as f:
            return f.read()

    @staticmethod
    def _mock_response(status_code=status.HTTP_200_OK, content=None, headers=None):
        response = requests.models.Response()
        response.status_code = status_code
        response._content = content.encode() if isinstance(content, str) else content
        response.headers = headers or {}
        return response
