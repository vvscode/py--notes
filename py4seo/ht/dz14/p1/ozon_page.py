from urllib.parse import urljoin
import json

from page import Page
from safe_run_with_default import safe_run_with_default


class OzonPage(Page):
    @property
    def images(self):
        return [
            urljoin(self.normalized_url, element.attrs["src"])
            for element in self.response.html.find(f".gallery img")
        ][:3]

    @property
    def price(self):
        return list(self.json_data['state']['pdp']['webSale'].values())[0]["cellTrackingInfo"]["product"]["price"]

    @property
    def body(self):
        return safe_run_with_default(
            lambda: self.response.html.find("#section-description .a1r9", first=True).text, ""
        )

    @property
    def title(self):
        return safe_run_with_default(
            lambda: self.response.html.find("h1 span", first=True).text, ""
        )

    @property
    def categories(self):
        breadcrumbs = list(self.json_data['state']['catalog']['breadCrumbsPdp'].values())[0]['breadCrumbs']
        return [x['text'] for x in breadcrumbs]

    @property
    def json_data(self):
        json_body = self.response.html.search("window.__NUXT__=JSON.parse('{}');")[0]
        json_body = json_body.replace('\\"', '"')
        return json.loads(json_body)
