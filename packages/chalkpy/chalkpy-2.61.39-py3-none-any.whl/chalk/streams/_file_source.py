from typing import TYPE_CHECKING, Any

from chalk.streams.base import StreamSource

if TYPE_CHECKING:
    from pydantic import BaseModel
else:

    try:
        from pydantic.v1 import BaseModel
    except ImportError:
        from pydantic import BaseModel


class FileSource(BaseModel, StreamSource, frozen=True):
    path: str
    key_separator: str = "|"

    def config_to_json(self) -> Any:
        return self.json()
