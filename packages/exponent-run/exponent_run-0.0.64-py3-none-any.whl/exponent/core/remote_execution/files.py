from asyncio import gather, to_thread
from os import PathLike
from typing import Optional, Union, cast
from typing import Final

from anyio import Path as AsyncPath
from rapidfuzz import process
from typing_extensions import TypeAlias
from python_ripgrep import PySortMode, PySortModeKind, files, search

from exponent.core.remote_execution.types import (
    FileAttachment,
    GetAllTrackedFilesRequest,
    GetAllTrackedFilesResponse,
    GetFileAttachmentsRequest,
    GetFileAttachmentsResponse,
    GetMatchingFilesRequest,
    GetMatchingFilesResponse,
    ListFilesRequest,
    ListFilesResponse,
    RemoteFile,
    GetFileAttachmentRequest,
    GetFileAttachmentResponse,
)

MAX_MATCHING_FILES: Final[int] = 10
FILE_NOT_FOUND: Final[str] = "File {} does not exist"
MAX_FILES_TO_WALK: Final[int] = 10_000

FilePath: TypeAlias = Union[str, PathLike[str]]


class FileCache:
    """A cache of the files in a working directory.

    Args:
        working_directory: The working directory to cache the files from.
    """

    def __init__(self, working_directory: str) -> None:
        self.working_directory = working_directory
        self._cache: Optional[list[str]] = None

    async def get_files(self) -> list[str]:
        """Get the files in the working directory.

        Returns:
            A list of file paths in the working directory.
        """
        if self._cache is None:
            self._cache = await file_walk(self.working_directory)

        return self._cache


async def list_files(list_files_request: ListFilesRequest) -> ListFilesResponse:
    """Get a list of files in the specified directory.

    Args:
        list_files_request: An object containing the directory to list files from.

    Returns:
        A list of RemoteFile objects representing the files in the directory.
    """

    filenames = [
        entry.name async for entry in AsyncPath(list_files_request.directory).iterdir()
    ]

    return ListFilesResponse(
        files=[
            RemoteFile(
                file_path=filename,
                working_directory=list_files_request.directory,
            )
            for filename in filenames
        ],
        correlation_id=list_files_request.correlation_id,
    )


async def get_file_content(absolute_path: FilePath) -> tuple[str, bool]:
    """Get the content of the file at the specified path.

    Args:
        absolute_path: The absolute path to the file.

    Returns:
        A tuple containing the content of the file and a boolean indicating if the file exists.
    """
    file = AsyncPath(absolute_path)
    exists = await file.exists()

    content = await file.read_text() if exists else FILE_NOT_FOUND.format(absolute_path)

    return content, exists


async def get_file_attachments(
    get_file_attachments_request: GetFileAttachmentsRequest,
    client_working_directory: str,
) -> GetFileAttachmentsResponse:
    """Get the content of the files at the specified paths.

    Args:
        get_file_attachments_request: An object containing the file paths.
        client_working_directory:  The working directory of the client.

    Returns:
        A list of FileAttachment objects containing the content of the files.
    """
    remote_files = get_file_attachments_request.files
    attachments = await gather(
        *[
            get_file_content(
                AsyncPath(client_working_directory) / remote_file.file_path
            )
            for remote_file in remote_files
        ]
    )

    files = [
        FileAttachment(attachment_type="file", file=remote_file, content=content)
        for remote_file, (content, _) in zip(remote_files, attachments)
    ]

    return GetFileAttachmentsResponse(
        correlation_id=get_file_attachments_request.correlation_id,
        file_attachments=files,
    )


async def get_file_attachment(
    get_file_attachment_request: GetFileAttachmentRequest, client_working_directory: str
) -> GetFileAttachmentResponse:
    """Get the content of the file at the specified path.

    Args:
        get_file_attachment_request: An object containing the file path.
        client_working_directory: The working directory of the client.

    Returns:
        A FileAttachment object containing the content of the file.
    """
    file = get_file_attachment_request.file
    absolute_path = await file.resolve(client_working_directory)

    content, exists = await get_file_content(absolute_path)

    return GetFileAttachmentResponse(
        content=content,
        exists=exists,
        file=file,
        correlation_id=get_file_attachment_request.correlation_id,
    )


async def get_matching_files(
    search_term: GetMatchingFilesRequest,
    file_cache: FileCache,
) -> GetMatchingFilesResponse:
    """Get the files that match the search term.

    Args:
        search_term: The search term to match against the files.
        file_cache: A cache of the files in the working directory.

    Returns:
        A list of RemoteFile objects that match the search term.
    """
    # Use rapidfuzz to find the best matching files
    matching_files = await to_thread(
        process.extract,
        search_term.search_term,
        await file_cache.get_files(),
        limit=MAX_MATCHING_FILES,
        score_cutoff=0,
    )

    directory = file_cache.working_directory
    files: list[RemoteFile] = [
        RemoteFile(file_path=file, working_directory=directory)
        for file, _, _ in matching_files
    ]

    return GetMatchingFilesResponse(
        files=files,
        correlation_id=search_term.correlation_id,
    )


async def get_all_tracked_files(
    request: GetAllTrackedFilesRequest,
    working_directory: str,
) -> GetAllTrackedFilesResponse:
    return GetAllTrackedFilesResponse(
        correlation_id=request.correlation_id,
        files=await get_all_non_ignored_files(working_directory),
    )


async def search_files(
    path_str: str,
    file_pattern: Optional[str],
    regex: str,
    working_directory: str,
) -> list[str]:
    path = AsyncPath(working_directory) / path_str
    path_resolved = await path.resolve()
    globs = [file_pattern] if file_pattern else None

    return await to_thread(
        search,
        patterns=[regex],
        paths=[str(path_resolved)],
        globs=globs,
        after_context=2,
        before_context=2,
        heading=True,
        separator_field_context="|",
        separator_field_match="|",
        separator_context="\n...\n",
    )


async def get_all_file_contents(
    working_directory: str,
) -> list[list[str]]:
    path_resolved = await AsyncPath(working_directory).resolve()

    results = await to_thread(
        search,
        patterns=[".*"],
        paths=[str(path_resolved)],
        globs=["!**/poetry.lock", "!**/pnpm-lock.yaml"],
        heading=True,
        line_number=False,
    )

    result_sizes = [len(result) for result in results]
    total_size = sum(result_sizes)
    batch_size = total_size // 10

    batches = []
    current_batch: list[str] = []
    current_size = 0

    for i, result in enumerate(results):
        if current_size + result_sizes[i] > batch_size:
            batches.append(current_batch)
            current_batch = []
            current_size = 0

        current_batch.append(result)
        current_size += result_sizes[i]

    batches.append(current_batch)

    return batches


async def normalize_files(
    working_directory: str, file_paths: list[FilePath]
) -> list[RemoteFile]:
    """Normalize file paths to be relative to the working directory.

    Args:
        working_directory: The working directory to normalize the file paths against.
        file_paths: A list of file paths to normalize.

    Returns:
        A list of RemoteFile objects with normalized file paths.
    """
    working_path = await AsyncPath(working_directory).resolve()
    normalized_files = []

    for file_path in file_paths:
        path = AsyncPath(file_path)

        if path.is_absolute():
            path = path.relative_to(working_path)

        normalized_files.append(
            RemoteFile(
                file_path=str(path),
                working_directory=working_directory,
            )
        )

    return sorted(normalized_files)


def _get_safe_relative_path(path: FilePath, parent: FilePath) -> Optional[AsyncPath]:
    try:
        return AsyncPath(path).relative_to(AsyncPath(parent))
    except ValueError:
        return None


def _format_ignore_globs(ignore_extra: Optional[list[str]]) -> list[str]:
    if ignore_extra is None:
        return []

    return [f"!**/{ignore}" for ignore in ignore_extra]


async def file_walk(
    directory: str,
    ignore_extra: Optional[list[str]] = None,
    max_files: int = MAX_FILES_TO_WALK,
) -> list[str]:
    """
    Walk through a directory and return all file paths, respecting .gitignore and additional ignore patterns.

    Args:
        directory: The directory to walk through
        ignore_extra: Additional directory paths to ignore, follows the gitignore format.
        max_files: The maximal number of files to return

    Returns:
        A list of file paths in the directory.
    """
    working_path = str(await AsyncPath(directory).resolve())

    results: list[str] = await to_thread(
        files,
        patterns=[""],
        paths=[working_path],
        globs=_format_ignore_globs(ignore_extra),
        sort=PySortMode(kind=PySortModeKind.Path),
        max_count=max_files,
    )

    results = [result.removeprefix(working_path + "/") for result in results]

    return results


async def get_all_non_ignored_files(working_directory: str) -> list[RemoteFile]:
    file_paths = await file_walk(working_directory, ignore_extra=DEFAULT_IGNORES)

    return await normalize_files(working_directory, cast(list[FilePath], file_paths))


DEFAULT_IGNORES = [
    "**/.git/",
    ".venv/",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules/",
    "venv/",
    ".pyenv",
    "__pycache__",
    ".ipynb_checkpoints",
    ".vercel",
    "__pycache__/",
    "*.py[cod]",
    "*$py.class",
    ".env",
    "*.so",
    ".Python",
    "build/",
    "develop-eggs/",
    "dist/",
    "downloads/",
    "eggs/",
    ".eggs/",
    "lib/",
    "lib64/",
    "parts/",
    "sdist/",
    "var/",
    "wheels/",
    "pip-wheel-metadata/",
    "share/python-wheels/",
    "*.egg-info/",
    ".installed.cfg",
    "*.egg",
    "MANIFEST",
]
