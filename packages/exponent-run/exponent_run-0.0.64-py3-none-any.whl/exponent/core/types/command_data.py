from enum import Enum
from typing import Any, ClassVar, Literal, Union

from pydantic import BaseModel


class CommandType(str, Enum):
    THINKING = "thinking"
    FILE_READ = "file_read"
    PROTOTYPE = "prototype"


class CommandData(BaseModel):
    executable: ClassVar[bool]


class FileReadCommandData(CommandData):
    executable: ClassVar[bool] = True
    type: Literal[CommandType.FILE_READ] = CommandType.FILE_READ

    file_path: str
    language: str


class ThinkingCommandData(CommandData):
    executable: ClassVar[bool] = False
    type: Literal[CommandType.THINKING] = CommandType.THINKING

    content: str


class PrototypeCommandData(CommandData):
    executable: ClassVar[bool] = True
    type: Literal[CommandType.PROTOTYPE] = CommandType.PROTOTYPE

    command_name: str
    # Structured data extracted from LLM output
    content_json: dict[str, Any]
    # Raw text extracted from LLM output
    content_raw: str
    # Rendered LLM output for frontend display
    content_rendered: str


CommandDataType = Union[FileReadCommandData, ThinkingCommandData, PrototypeCommandData]
