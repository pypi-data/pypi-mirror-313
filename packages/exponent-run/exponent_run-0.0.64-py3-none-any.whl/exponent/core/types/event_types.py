from typing import Literal, Optional, Union
from exponent.core.types.command_data import CommandDataType
from pydantic import BaseModel, Field, JsonValue


DEFAULT_CODE_BLOCK_TIMEOUT = 30

FileWriteStrategyName = Literal[
    "FULL_FILE_REWRITE", "UDIFF", "SEARCH_REPLACE", "NATURAL_EDIT"
]
WRITE_STRATEGY_NATURAL_EDIT: Literal["NATURAL_EDIT"] = "NATURAL_EDIT"
WRITE_STRATEGY_FULL_FILE_REWRITE: Literal["FULL_FILE_REWRITE"] = "FULL_FILE_REWRITE"
WRITE_STRATEGY_UDIFF: Literal["UDIFF"] = "UDIFF"
WRITE_STRATEGY_SEARCH_REPLACE: Literal["SEARCH_REPLACE"] = "SEARCH_REPLACE"


class ExponentEvent(BaseModel):
    chat_uuid: str
    event_uuid: str
    parent_uuid: Optional[str]
    turn_uuid: str

    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class CodeBlockEvent(ExponentEvent):
    language: str
    content: str
    timeout: int = DEFAULT_CODE_BLOCK_TIMEOUT
    require_confirmation: bool = False


class EditContent(BaseModel):
    content: str


class NaturalEditContent(BaseModel):
    natural_edit: str
    intermediate_edit: Optional[str]
    original_file: Optional[str]
    new_file: Optional[str]
    error_content: Optional[str]


class FileWriteEvent(ExponentEvent):
    file_path: str
    language: str
    write_strategy: FileWriteStrategyName
    write_content: Union[NaturalEditContent, EditContent]
    content: str
    require_confirmation: bool = False


class CommandEvent(ExponentEvent):
    data: CommandDataType = Field(..., discriminator="type")
    require_confirmation: bool = False


LocalEventType = Union[FileWriteEvent, CodeBlockEvent, CommandEvent]
