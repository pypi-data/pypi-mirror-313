import typing as t

from markupsafe import Markup


class BodyContent:
    div_id: str
    noscript_message: str

    def __init__(
        self,
        div_id: str = "root",
        noscript_message: str = "You need to enable JavaScript to run this app.",
    ) -> None:
        self.div_id = div_id
        self.noscript_message = noscript_message

    def __repr__(self) -> str:
        return (
            "BodyContent< "
            f"id = {self.div_id} "
            f"noscript = {self.noscript_message} "
            ">"
        )

    def __str__(self) -> Markup:
        return Markup(self._compile())

    def __call__(self, *args: t.Any, **kwargs: t.Any) -> Markup:
        return Markup(self._compile())

    def _compile(self) -> Markup:
        return Markup(
            f'<div id="{self.div_id}"></div>\n'
            f"<noscript>{self.noscript_message}</noscript>"
        )
