from timeit import default_timer as timer
from safe_run_with_default import safe_run_with_default
from requests_html import HTMLSession


class Page:
    _response = None
    response_time = None

    def __init__(self, url, client=None):
        self.original_url = url
        self.client = client

    def get_client(self):
        if self.client is None:
            self.client = HTMLSession()
        return self.client

    @property
    def normalized_url(self):
        return self.original_url.split("#")[0]

    @property
    def response(self):
        if self._response is not None:
            return self._response

        start_request_time = timer()
        self._response = self.get_client().get(self.normalized_url)
        end_request_time = timer()
        self.response_time = end_request_time - start_request_time
        return self._response

    @property
    def title(self):
        return safe_run_with_default(
            lambda: self.response.html.find("title", first=True).text, ""
        )

    @property
    def h1(self):
        return safe_run_with_default(
            lambda: self.response.html.find("h1", first=True).text, ""
        )

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def links(self):
        return self.response.html.absolute_links
