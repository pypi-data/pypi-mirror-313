from dataclasses import dataclass
from typing import Optional


@dataclass
class StreamedOutputPiece:
    content: str


@dataclass
class ShellExecutionResult:
    output: str
    cancelled_for_timeout: bool
    exit_code: Optional[int]
    halted: bool = False


@dataclass
class PythonExecutionResult:
    output: str
    halted: bool = False
