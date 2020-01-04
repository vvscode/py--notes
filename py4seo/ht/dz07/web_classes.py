import re


class Text(str):
    """Represents generic html"""

    @property
    def html(self):
        return f"<p>{self}</p>"

    @property
    def text(self):
        return re.sub(r"<.*?>", "", self.html)


class Link(Text):
    def with_anchor(self, anchor):
        self.anchor = anchor
        return self

    @property
    def html(self):
        return f'<a href="{self.anchor}">{self}</a>'


class Image(Text):
    def __init__(self, name):
        self.name = name
        self.address = "#"

    def with_address(self, address):
        self.address = address
        return self

    @property
    def html(self):
        return f'<img src="{self.address}" alt="{self.name}" title="{self.name}" />'

    @property
    def text(self):
        return f"{self.address} [{self.name}]"


class Title(Text):
    level = 1

    def with_level(self, level):
        self.level = level
        return self

    @property
    def html(self):
        return f"<h{self.level}>{self}</h{self.level}>"


class Description(Text):
    @property
    def html(self):
        return f'<meta name="description" content="{self}">'


class Page:
    def __init__(self, *args):
        self.header_elements = []
        self.body_elements = list(filter(lambda x: isinstance(x, Text), args))

    def add_to_header(self, *args):
        self.body_elements.extend(filter(lambda x: isinstance(x, Text), args))

    def add_to_body(self, *args):
        self.body_elements.extend(filter(lambda x: isinstance(x, Text), args))

    def remove(self, *args):
        for el in args:
            if el in self.elements:
                self.body_elements.remove(el)

    @property
    def text(self):
        return "\n".join(map(str, self.body_elements))

    @property
    def html(self):
        return f"""
      <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <meta http-equiv="X-UA-Compatible" content="ie=edge">
          {"".join(map(lambda x: x.html, self.header_elements))}
          <title>Document</title>
        </head>
        <body>
          {"".join(map(lambda x: x.html, self.body_elements))}
        </body>
        </html>
        """


class Website:
    def __init__(self):
        self.structure = {}
        self.not_found = None

    def add_page(self, url, page):
        self.structure[url] = page
        return self

    def set_not_found(self, page):
        self.not_found = page
        return self

    def navigate(self, url):
        if url in self.structure:
            return self.structure[url]
        return self.not_found


class Book:
    def __init__(self, *args):
        self.pages = list(filter(lambda x: isinstance(x, Page), args))

    def __str__(self):
        return "\n\n\n".join(map(lambda x: x.text, self.pages))
