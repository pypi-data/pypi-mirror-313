import inspect
import os
import re
import threading
import time
from copy import copy
from functools import lru_cache
from pathlib import Path
from typing import (
    IO,
    Any,
    Optional,
    Union,
)

from bs4 import BeautifulSoup, Tag

from .env import env

# html_regex = r"<!-{1,3}.*?-{1,3}>|^--html"
html_regex = r"^--html"
comment_regex = r"<!-{1,3}.*?-{1,3}>"

project_root = os.getcwd()

_cached_html: dict[str, Any] = {}


def clean_html(html: str) -> str:
    """
    Clean an HTML string by removing comments and extra whitespace.
    :param html: The HTML string to clean.
    :return: The cleaned HTML string.
    """
    # Remove comments
    html = re.sub(html_regex, "", html, flags=re.DOTALL)

    # remove extra returns
    html = re.sub(r"\n{1,}", "\n", html)

    return html.strip()


def clean_comments(html: str) -> str:
    """
    Clean an HTML string by removing comments and extra whitespace.
    :param html: The HTML string to clean.
    :return: The cleaned HTML string.
    """
    if env.is_dev:
        return html.strip()

    # Remove comments
    html = re.sub(comment_regex, "", html, flags=re.DOTALL)

    # remove extra returns
    html = re.sub(r"\n{1,}", "\n", html)

    return html.strip()


def resolve_path(path: Union[str, Path], base_dir: Optional[str] = None) -> Path:
    """
    Resolve the file path based on the given path and base directory.
    """
    if "~/" in str(path) or bool(re.match(r"^[a-zA-Z]", str(path))):
        path = Path(str(path).replace("~/", ""))
        base_path = project_root
    else:
        if not isinstance(path, Path):
            path = Path(path)

        base_path = None
        for frame_info in inspect.stack():
            frame_file = Path(frame_info.filename)
            if "weba" not in frame_file.parts:
                base_path = frame_file.parent
                break

        if base_path is None:
            base_path = Path.cwd()

    base_path = Path(base_path)
    resolved_path = (base_path / path).resolve()

    if not resolved_path.exists():
        if base_dir:
            resolved_path = (Path(base_dir) / path).resolve()
            if not resolved_path.exists():
                resolved_path = path.resolve()

        if not resolved_path.exists():
            raise FileNotFoundError(f"The file at {resolved_path} does not exist.")

    return resolved_path


class AdaptiveLRUCache:
    def __init__(self, initial_size: int = 128, min_size: int = 32, max_size: int = 1024):
        self.cache = lru_cache(maxsize=initial_size)(self._load_html)
        self.min_size = min_size
        self.max_size = max_size
        self.current_size = initial_size
        self.hits = 0
        self.misses = 0
        self.lock = threading.Lock()
        self.last_resize = time.time()

    def _load_html(self, path: str, parser: str, base_dir: Optional[str], last_modified: float) -> str:
        resolved_path = resolve_path(path, base_dir)
        current_mtime = os.path.getmtime(resolved_path)

        # Check if the file has been modified since last cache
        if current_mtime > last_modified:
            # File has been modified, need to reload
            with open(resolved_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Use the appropriate parser based on content
            if content.startswith("<?xml") and parser != "xml":
                parser = "xml"

            # Clean and parse the content
            cleaned_content = clean_html(content)

            # Parse with BeautifulSoup to ensure it's valid
            BeautifulSoup(cleaned_content, parser)

            return cleaned_content
        else:
            # File hasn't been modified, can use cached version
            with open(resolved_path, "r", encoding="utf-8") as file:
                return clean_html(file.read())

    def get(self, path: Union[str, Path], parser: str, base_dir: Optional[str]) -> str:
        resolved_path = resolve_path(path, base_dir)
        last_modified = os.path.getmtime(resolved_path)
        with self.lock:
            try:
                result = self.cache(str(resolved_path), parser, base_dir, last_modified)
                self.hits += 1
            except KeyError:
                result = self._load_html(str(resolved_path), parser, base_dir, last_modified)
                self.misses += 1

            self._maybe_resize()
            return result

    def _maybe_resize(self):
        now = time.time()
        if now - self.last_resize < 300:  # Only resize every 5 minutes at most
            return

        total = self.hits + self.misses
        if total > 1000:  # Only resize after a significant number of accesses
            hit_ratio = self.hits / total
            if hit_ratio > 0.9 and self.current_size < self.max_size:
                self.current_size = min(self.current_size * 2, self.max_size)
            elif hit_ratio < 0.5 and self.current_size > self.min_size:
                self.current_size = max(self.current_size // 2, self.min_size)
            else:
                return

            self.cache = lru_cache(maxsize=self.current_size)(self._load_html)
            self.hits = 0
            self.misses = 0
            self.last_resize = now


adaptive_cache = AdaptiveLRUCache()


def load_html_to_soup(
    path: Union[str, Path, BeautifulSoup, Tag], parser: str = env.html_parser, base_dir: Optional[str] = None
) -> BeautifulSoup | Tag:
    """
    Load an HTML file from a specified path and return a BeautifulSoup object.
    Uses adaptive caching for file content to improve performance.
    """
    if not parser:
        parser = env.html_parser

    if isinstance(path, (BeautifulSoup, Tag)):
        return copy(path)

    path_str = str(path)
    if "\n" in path_str or path_str.startswith("--html"):
        file_contents = clean_html(path_str)
        if file_contents.startswith("<?xml"):
            parser = env.xml_parser
        return BeautifulSoup(file_contents, parser)

    content = adaptive_cache.get(path_str, parser, base_dir)

    if content.startswith("<?xml"):
        parser = env.xml_parser

    return BeautifulSoup(content, parser)


def _load_file_contents_to_bs4(file: IO[str], parser: str, resolved_path: Path) -> BeautifulSoup:
    global _cached_html

    file_contents = clean_html(file.read())

    if file_contents.startswith("<?xml"):
        parser = env.xml_parser

    _cached_html[str(resolved_path)] = file_contents

    return BeautifulSoup(file_contents, parser)


def update_kwargs(kwargs: dict[str, Any]):
    """
    Update the kwargs dictionary in place to handle special cases:
    - Converts class variants to 'class'.
    - Converts 'hx_' prefixed keys to 'hx-'.
    - Converts 'for_' to 'for'.
    """
    # Handle different variations of the class attribute
    class_variants = ["_class", "class_", "klass", "cls"]

    for variant in class_variants:
        if variant in kwargs:
            kwargs["class"] = kwargs.pop(variant)
            break

    # Convert 'hx_' prefix to 'hx-' and 'for_' to 'for'
    for key in list(kwargs.keys()):
        if key == "for_":
            kwargs["for"] = kwargs.pop(key)

        if env.ui_attrs_to_dash and key in kwargs:
            new_key = key.replace("_", "-")
            kwargs[new_key] = kwargs.pop(key)

    return kwargs
