import typing as t

from markupsafe import Markup


class LinkTag:
    rel: str
    href: t.Optional[str] = None
    sizes: t.Optional[str] = None
    type: t.Optional[str] = None
    hreflang: t.Optional[str] = None

    _rel: str
    _href: t.Optional[str] = None
    _sizes: t.Optional[str] = None
    _type: t.Optional[str] = None
    _hreflang: t.Optional[str] = None

    def __init__(
        self,
        rel: str,
        href: t.Optional[str] = None,
        sizes: t.Optional[str] = None,
        type_: t.Optional[str] = None,
        hreflang: t.Optional[str] = None,
    ) -> None:
        self.rel = rel
        self.href = href
        self.sizes = sizes
        self.type = type_
        self.hreflang = hreflang

        self._rel = f'rel="{self.rel}" '
        self._href = f'href="{self.href}" ' if self.href is not None else ""
        self._sizes = f'sizes="{self.sizes}" ' if self.sizes is not None else ""
        self._type = f'type="{self.type}" ' if self.type is not None else ""
        self._hreflang = (
            f'hreflang="{self.hreflang}" ' if self.hreflang is not None else ""
        )

    def __repr__(self) -> Markup:
        return Markup(
            f"<LinkTag {self._rel}{self._href}{self._sizes}{self._type}{self._hreflang}>".replace(
                " >", ">"
            )
        )

    def __str__(self) -> Markup:
        return Markup(self._compile())

    def __call__(self, *args: t.Any, **kwargs: t.Any) -> Markup:
        return Markup(self._compile())

    def raw(self) -> str:
        return self._compile()

    def _compile(self) -> str:
        return f"<link {self._rel}{self._href}{self._sizes}{self._type}{self._hreflang}>".replace(
            " >", ">"
        )
