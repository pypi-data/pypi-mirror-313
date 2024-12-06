import contextvars
from copy import copy
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Union,
    cast,
)

from bs4 import BeautifulSoup, PageElement
from bs4.element import Tag

from ..env import env
from .mixins import TagMixins

if TYPE_CHECKING:
    from ..component import Component

weba_html_context: contextvars.ContextVar[Any] = contextvars.ContextVar("current_weba_html_context")


class TagContextManager(TagMixins):
    _html: "Component"
    _tag: Tag

    def __init__(self, tag: Tag, html: "Component", *_args: Any, **_kwargs: Any):
        self._tag = tag
        self._weba_html_context = html
        self._content = None

    def __enter__(self) -> "TagContextManager":  # Push the tag onto the instance's context stack
        self._weba_html_context._context_stack.append(self._tag)  # type: ignore (we need to access private property

        return self

    def __exit__(self, _exc_type: Any, _exc_value: Any, _traceback: Any):
        if not self._weba_html_context._after_render_called:  # type: ignore (we need to access private property)
            self._weba_html_context._last_component = self  # type: ignore (we need to access private property)

        # Pop the tag from the instance's context stack
        if hasattr(self._weba_html_context, "_context_stack") and self._weba_html_context._context_stack:  # type: ignore (we need to access private property
            self._weba_html_context._context_stack.pop()  # type: ignore (we need to access private property)

    def __getitem__(self, key: str) -> Union[Any, list[str]]:
        if key == "class":
            attr = self.get(key)

            if not attr:
                self["class"] = []
            elif not isinstance(attr, list):
                self[key] = attr.strip().split(" ")
            else:
                self["class"] = attr.copy()

        return super().__getitem__(key)

    def __getattr__(self, name: str) -> "TagContextManager | None":
        if "_tag" not in self.__dict__ or not hasattr(self.__dict__["_tag"], name):
            return None

        response = getattr(self.__dict__["_tag"], name)

        if response.__class__.__name__ == "Tag":
            return self._tag_context_manager(response)

        return response

    def __copy__(self) -> "TagContextManager":
        return self._tag_context_manager(copy(self._tag))

    def copy(self) -> "TagContextManager":
        return self.__copy__()

    def __deepcopy__(self, memo: dict[int, Any]) -> "TagContextManager":
        return self._tag_context_manager(self._tag.__deepcopy__(memo))  # type: ignore

    def insert(self, position: int, new_child: PageElement | str) -> None:
        if hasattr(new_child, "content") and new_child.content is not None:  # type: ignore
            self._tag.insert(position, new_child.content)  # type: ignore
        elif hasattr(new_child, "_tag") and new_child._tag is not None:  # type: ignore
            self._tag.insert(position, new_child._tag)  # type: ignore
        else:
            self._tag.insert(position, new_child)

    def insert_after(self, *args: Union[PageElement, str, "TagContextManager"]) -> None:
        """Makes the given element(s) the immediate successor of this one.
        The elements will have the same parent, and the given elements
        will be immediately after this one.
        :param args: One or more PageElements, strings, or TagContextManagers.
        """
        parent = self._tag.parent
        if parent is None:
            raise ValueError("Element has no parent, so 'after' has no meaning.")
        if any(x is self for x in args):
            raise ValueError("Can't insert an element after itself.")

        for offset, successor in cast(Any, enumerate(args)):
            if isinstance(successor, TagContextManager):
                successor = successor._tag
            elif hasattr(successor, "content") and successor.content is not None:
                successor = successor.content
            elif hasattr(successor, "_tag") and successor._tag is not None:
                successor = successor._tag

            if isinstance(successor, PageElement):
                successor.extract()

            index = parent.index(self._tag)
            parent.insert(index + 1 + offset, successor)

    def insert_before(self, *args: Union[PageElement, str, "TagContextManager"]) -> None:
        """Makes the given element(s) the immediate predecessor of this one.
        The elements will have the same parent, and the given elements
        will be immediately before this one.
        :param args: One or more PageElements, strings, or TagContextManagers.
        """
        parent = self._tag.parent
        if parent is None:
            raise ValueError("Element has no parent, so 'before' has no meaning.")
        if any(x is self for x in args):
            raise ValueError("Can't insert an element before itself.")

        for predecessor in cast(Any, reversed(args)):
            if isinstance(predecessor, TagContextManager):
                predecessor = predecessor._tag
            elif hasattr(predecessor, "content") and predecessor.content is not None:
                predecessor = predecessor.content
            elif hasattr(predecessor, "_tag") and predecessor._tag is not None:
                predecessor = predecessor._tag

            if isinstance(predecessor, PageElement):
                predecessor.extract()

            index = parent.index(self._tag)
            parent.insert(index, predecessor)

    def extract(self, self_index: Optional[int] = None):
        return self._tag_context_manager(self._tag.extract(self_index))

    def _tag_context_manager(self, tag: Tag) -> "TagContextManager":
        return (
            tag
            if tag._is_component  # type: ignore (we need to access private property)
            else TagContextManager(tag, self._weba_html_context)
        )

    # TODO: Fix typing
    def replace_with(self, tag: Any, *args: Any):  # type: ignore
        if tag._is_component:
            content = tag.content or tag._tag
            self._tag.replace_with(content, *args)
            self._content = content
        else:
            self._tag.replace_with(tag, *args)
            tag = self._tag_context_manager(tag)
            self._content = tag

        return tag

    async def __aenter__(self) -> Tag:
        return self.__enter__()

    async def __aexit__(self, _exc_type: Any, _exc_value: Any, _traceback: Any):
        self.__exit__(_exc_type, _exc_value, _traceback)
