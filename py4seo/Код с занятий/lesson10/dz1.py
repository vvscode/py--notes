class Page:
    _response = None
    response_time = None

    def __init__(self, url, client=None):
        self.original_url = url
        self.client = client

    def get_client(self):
        if self.client is None:
            self.client = 12312312
        return self.client


p1 = Page('url1', 'client1')
p2 = Page('url1', 'client1')
p3 = Page('url1', 'client1')
