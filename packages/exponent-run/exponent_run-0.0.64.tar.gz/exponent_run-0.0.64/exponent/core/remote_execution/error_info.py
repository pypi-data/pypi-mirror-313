from typing import Any, Optional

from pydantic import BaseModel
import traceback


class SerializableErrorInfo(BaseModel):
    message: str
    stack: list[str]
    cls_name: Optional[str]
    cause: Any
    context: Any

    def __str__(self) -> str:
        return self.to_string()

    def to_string(self) -> str:
        stack_str = "\nStack Trace:\n" + "".join(self.stack) if self.stack else ""
        cause_str = (
            "\nThe above exception was caused by the following exception:\n"
            + self.cause.to_string()
            if self.cause
            else ""
        )
        context_str = (
            "\nThe above exception occurred during handling of the following exception:\n"
            + self.context.to_string()
            if self.context
            else ""
        )

        return f"{self.message}{stack_str}{cause_str}{context_str}"


def serialize_error_info(error: BaseException) -> SerializableErrorInfo:
    return SerializableErrorInfo(
        message=str(error),
        stack=traceback.format_tb(error.__traceback__),
        cls_name=error.__class__.__name__,
        cause=serialize_error_info(error.__cause__) if error.__cause__ else None,
        context=serialize_error_info(error.__context__) if error.__context__ else None,
    )
