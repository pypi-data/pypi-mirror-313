import os
from collections.abc import Callable
from pathlib import Path
from typing import Optional, Union, cast
from anyio import Path as AsyncPath

import pygit2
from pygit2 import Tree
from pygit2.repository import Repository
from pygit2.enums import DiffOption
from gitignore_parser import (
    IgnoreRule,
    handle_negation,
    parse_gitignore,
    rule_from_pattern,
)

from exponent.core.remote_execution.types import (
    GitInfo,
)

GIT_OBJ_COMMIT = 1


async def git_file_walk(
    repo: Repository,
    directory: str,
) -> list[str]:
    """
    Walk through a directory and return all file paths, respecting .gitignore and additional ignore patterns.
    """
    tree = get_git_subtree_for_dir(repo, directory)

    if not tree:
        return []

    # diff to the empty tree to see all files
    tracked_diff = tree.diff_to_tree()

    tracked_files = [delta.new_file.path for delta in tracked_diff.deltas]

    # Find untracked files relative to the root
    untracked_diff = repo.diff(flags=DiffOption.INCLUDE_UNTRACKED)
    untracked_files_from_root = [
        AsyncPath(delta.new_file.path) for delta in untracked_diff.deltas
    ]

    # Current working directory relative to the repo root
    dir_path = await AsyncPath(directory).resolve()
    repo_path = await AsyncPath(repo.workdir).resolve()

    if repo_path == dir_path:
        relative_directory = str(repo_path)
    else:
        relative_directory = str(dir_path.relative_to(repo_path))

    # Resolve all untracked files that are within the current working directory
    untracked_files = []
    for untracked_file in untracked_files_from_root:
        if not untracked_file.is_relative_to(relative_directory):
            continue

        untracked_files.append(str(untracked_file.relative_to(relative_directory)))

    # Combine both as sets to remove duplicates
    return list(set(tracked_files) | set(untracked_files))


def get_repo(working_directory: str) -> Optional[Repository]:
    try:
        return Repository(working_directory)
    except pygit2.GitError:
        return None


def get_git_info(working_directory: str) -> Optional[GitInfo]:
    try:
        repo = Repository(working_directory)
    except pygit2.GitError:
        return None

    return GitInfo(
        branch=_get_git_branch(repo) or "<unknown branch>",
        remote=_get_git_remote(repo),
    )


def get_tracked_files_in_dir(
    repo: Repository,
    dir: Union[str, Path],
    filter_func: Optional[Callable[[str], bool]] = None,
) -> list[str]:
    rel_path = get_path_relative_to_repo_root(repo, dir)
    dir_tree = get_git_subtree_for_dir(repo, dir)
    entries: list[str] = []
    if not dir_tree:
        return entries
    for entry in dir_tree:
        if not entry.name:
            continue
        entry_path = str(Path(f"{repo.workdir}/{rel_path}/{entry.name}"))
        if entry.type_str == "tree":
            entries.extend(get_tracked_files_in_dir(repo, entry_path, filter_func))
        elif entry.type_str == "blob":
            if not filter_func or filter_func(entry.name):
                entries.append(entry_path)
    return entries


def get_git_subtree_for_dir(repo: Repository, dir: Union[str, Path]) -> Optional[Tree]:
    rel_path = get_path_relative_to_repo_root(repo, dir)

    try:
        head_commit = repo.head.peel(GIT_OBJ_COMMIT)
    except pygit2.GitError:
        # If the repo is empty, then the head commit will not exist
        return None
    head_tree: Tree = head_commit.tree

    if rel_path == Path("."):
        # If the relative path is the root of the repo, then
        # the head_tree is what we want. Note we do this because
        # Passing "." or "" as the path into the tree will raise.
        return head_tree
    return cast(Tree, head_tree[str(rel_path)])


def get_path_relative_to_repo_root(repo: Repository, path: Union[str, Path]) -> Path:
    path = Path(path).resolve()
    return path.relative_to(Path(repo.workdir).resolve())


def get_local_commit_hash() -> str:
    try:
        # Open the repository (assumes the current working directory is within the git repo)
        repo = Repository(os.getcwd())

        # Get the current HEAD commit
        head = repo.head

        # Get the commit object and return its hash as a string
        return str(repo[head.target].id)
    except pygit2.GitError:
        return "unknown-local-commit"


def _get_git_remote(repo: Repository) -> Optional[str]:
    if repo.remotes:
        return str(repo.remotes[0].url)
    return None


def _get_git_branch(repo: Repository) -> Optional[str]:
    try:
        # Look for HEAD file in the .git directory
        head_path = os.path.join(repo.path, "HEAD")
        with open(head_path) as head_file:
            # The HEAD file content usually looks like: 'ref: refs/heads/branch_name'
            head_content = head_file.read().strip()
            if head_content.startswith("ref:"):
                return head_content.split("refs/heads/")[-1]
            else:
                return None
    except Exception:  # noqa: BLE001
        return None


class GitIgnoreHandler:
    def __init__(
        self, working_directory: str, default_ignores: Optional[list[str]] = None
    ):
        self.checkers = {}

        if default_ignores:
            self.checkers[working_directory] = self._parse_ignore_extra(
                working_directory, default_ignores
            )

    async def read_ignorefile(self, path: str) -> None:
        new_ignore = await self._get_ignored_checker(path)

        if new_ignore:
            self.checkers[path] = new_ignore

    def filter(
        self,
        relpaths: list[str],
        root: str,
    ) -> list[str]:
        result = []

        for relpath in relpaths:
            if relpath.startswith(".git"):
                continue

            path = os.path.join(root, relpath)

            if self.is_ignored(path):
                continue

            result.append(relpath)

        return result

    def is_ignored(self, path: str) -> bool:
        return any(
            self.checkers[dp](path)
            for dp in self.checkers
            if self._is_subpath(path, dp)
        )

    def _parse_ignore_extra(
        self, working_directory: str, ignore_extra: list[str]
    ) -> Callable[[str], bool]:
        rules: list[IgnoreRule] = []

        for pattern in ignore_extra:
            if (
                rule := rule_from_pattern(pattern, base_path=working_directory)
            ) is not None:
                rules.append(rule)

        def rule_handler(file_path: str) -> bool:
            nonlocal rules
            return bool(handle_negation(file_path, rules))

        return rule_handler

    async def _get_ignored_checker(
        self, dir_path: str
    ) -> Optional[Callable[[str], bool]]:
        new_ignore = self._parse_gitignore(dir_path)

        existing_ignore = self.checkers.get(dir_path)

        if existing_ignore and new_ignore:
            return self._or(new_ignore, existing_ignore)

        return new_ignore or existing_ignore

    @staticmethod
    def _parse_gitignore(directory: str) -> Optional[Callable[[str], bool]]:
        gitignore_path = os.path.join(directory, ".gitignore")

        if os.path.isfile(gitignore_path):
            return cast(Callable[[str], bool], parse_gitignore(gitignore_path))

        return None

    @staticmethod
    def _or(
        a: Callable[[str], bool], b: Callable[[str], bool]
    ) -> Callable[[str], bool]:
        def or_handler(file_path: str) -> bool:
            return a(file_path) or b(file_path)

        return or_handler

    @staticmethod
    def _is_subpath(path: str, parent: str) -> bool:
        """
        Check if a path is a subpath of another path.
        """
        return os.path.commonpath([path, parent]) == parent
