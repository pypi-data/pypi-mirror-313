from django.http import Http404
from orjson import JSONDecodeError
from rest_framework import status


class Service:

    def get(self):
        pass

    def normalize_response(self, response):
        from django.http.response import HttpResponseRedirect
        from rest_framework.response import Response

        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise Http404()

        if response.is_redirect:
            url = response.headers["location"]
            if url.rfind("format") > 0:
                url = url[:url.rfind("format")]
            return HttpResponseRedirect(url, status=response.status_code)

        acceptable_statuses = [status.HTTP_429_TOO_MANY_REQUESTS]

        if response.status_code > status.HTTP_406_NOT_ACCEPTABLE and \
                response.status_code not in acceptable_statuses:
            response.raise_for_status()

        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response(status=status.HTTP_204_NO_CONTENT)

        data = self.normalize(response)

        return Response(data=data, status=response.status_code)

    @staticmethod
    def normalize(response):
        data = {}
        if response.content:
            try:
                data = response.json()
            except JSONDecodeError as exc:
                data = {"content": response.content}
        return data
