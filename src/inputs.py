import typing


class SearchInput(typing.NamedTuple):
    keywords: typing.List[str]
    proxies: typing.List[str]
    type: str
