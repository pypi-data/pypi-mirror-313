import typing as t

from markupsafe import Markup


class ScriptTag:
    src: str
    type: t.Optional[str] = None
    async_: bool = False
    defer: bool = False
    crossorigin: t.Optional[str] = None
    integrity: t.Optional[str] = None
    nomodule: bool = False
    referrerpolicy: t.Optional[str] = None

    _src: str
    _type: t.Optional[str] = None
    _async: t.Optional[str] = None
    _defer: t.Optional[str] = None
    _crossorigin: t.Optional[str] = None
    _integrity: t.Optional[str] = None
    _nomodule: t.Optional[str] = None
    _referrerpolicy: t.Optional[str] = None

    def __init__(
        self,
        src: str,
        type_: t.Optional[str] = None,
        async_: bool = False,
        defer: bool = False,
        crossorigin: t.Optional[str] = None,
        integrity: t.Optional[str] = None,
        nomodule: bool = False,
        referrerpolicy: t.Optional[str] = None,
    ) -> None:
        self.src = src
        self.type = type_
        self.async_ = async_
        self.defer = defer
        self.crossorigin = crossorigin
        self.integrity = integrity
        self.nomodule = nomodule
        self.referrerpolicy = referrerpolicy

        self._src = f'src="{self.src}" '
        self._type = f'type="{self.type}" ' if self.type is not None else ""
        self._async = f'async="{str(self.async_).lower()}" ' if self.async_ else ""
        self._defer = "defer " if self.defer else ""
        self._crossorigin = (
            f'crossorigin="{self.crossorigin}" ' if self.crossorigin is not None else ""
        )
        self._integrity = (
            f'integrity="{self.integrity}" ' if self.integrity is not None else ""
        )
        self._nomodule = "nomodule " if self.nomodule else ""
        self._referrerpolicy = (
            f'referrerpolicy="{self.referrerpolicy}" '
            if self.referrerpolicy is not None
            else ""
        )

    def __repr__(self) -> Markup:
        return Markup(
            (
                f"<ScriptTag {self._src}{self._type}"
                f"{self._async}{self._defer}{self._crossorigin}"
                f"{self._integrity}{self._nomodule}{self._referrerpolicy}>"
            ).replace(" >", ">")
        )

    def __str__(self) -> Markup:
        return Markup(self._compile())

    def __call__(self, *args: t.Any, **kwargs: t.Any) -> Markup:
        return Markup(self._compile())

    def raw(self) -> str:
        return self._compile()

    def _compile(self) -> str:
        return (
            f"<script {self._src}{self._type}"
            f"{self._async}{self._defer}{self._crossorigin}"
            f"{self._integrity}{self._nomodule}{self._referrerpolicy}></script>"
        ).replace(" >", ">")
