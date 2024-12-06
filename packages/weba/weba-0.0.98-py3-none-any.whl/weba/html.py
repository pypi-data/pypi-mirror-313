from typing import NotRequired, Optional, TypedDict, Unpack

from weba.component import Component, tag


class HTMLKwargs(TypedDict):
    title: NotRequired[str]
    lang: NotRequired[str]


class HTML(Component):
    src = """--html
        <!doctype html>
        <html lang="en-US">

        <head>
            <title>Weba</title>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        </head>

        <body></body>

        </html>
    """

    def __init__(self, src: Optional[str] = None, **kwargs: Unpack[HTMLKwargs]):
        self.src = src
        self.title = kwargs.get("title", "Weba")
        self.lang = kwargs.get("lang", "en-US")

    def render(self):
        if self.head.title:
            self.head.title.string = self.title

        self.html["lang"] = self.lang

    @tag("body")
    def body(self):
        pass

    @tag("head")
    def head(self):
        pass
