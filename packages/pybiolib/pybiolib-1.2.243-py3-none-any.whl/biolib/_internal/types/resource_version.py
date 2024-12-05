from .typing import Literal, TypedDict


class ResourceVersionDetailedDict(TypedDict):
    semantic_version: str
    state: Literal['published', 'unpublished']
    uuid: str
