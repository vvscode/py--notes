from reppy.robots import Robots
import logging


class RobotsChecker:
    def __init__(self, domain, agent_name="Py4Seo Parse"):
        self.robots_txt_url = f"{domain}/robots.txt".replace(
            "//robots.txt", "/robots.txt"
        )
        self.agent_name = agent_name
        self._agent = None

    @property
    def agent(self):
        if self._agent is not None:
            return self._agent
        try:
            self._agent = Robots.fetch(self.robots_txt_url)
            self._agent.agent(self.agent_name)
            return self._agent
        except Exception as e:
            logging.debug(
                f"Getting agent `{self.agent_name}` for `{self.robots_txt_url}` failed with {e}"
            )
            raise e

    def is_allowed(self, url):
        if self.agent is None:
            return True
        return self.agent.allowed(url, self.agent_name)
