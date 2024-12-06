from typing import Union

from tableauserverclient import ServerResponseError  # type: ignore
from typing_extensions import Literal

from .errors import TableauErrorCode

PageReturn = Union[
    tuple[list[dict], Literal[None]],
    tuple[Literal[None], Union[TableauErrorCode, ServerResponseError]],
]
