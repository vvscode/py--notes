from urllib.parse import urljoin

from page import Page
from safe_run_with_default import safe_run_with_default


class OlxPage(Page):
    @property
    def images(self):
        return [
            urljoin(self.normalized_url, element.attrs["src"])
            for element in self.response.html.find(f"img.bigImage")
        ]

    @property
    def price(self):
        return safe_run_with_default(
            lambda: self.response.html.find(".price-label strong", first=True).text, ""
        )

    @property
    def body(self):
        return safe_run_with_default(
            lambda: self.response.html.find("#textContent", first=True).text, ""
        )
