import contextvars

# from copy import copy
from copy import copy
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)

from bs4 import NavigableString

# from bs4.element import Tag
from .context_manager import TagContextManager as Tag

weba_html_context: contextvars.ContextVar[Any] = contextvars.ContextVar("current_weba_html_context")

if TYPE_CHECKING:
    from ..component import Component

# Define a type variable with an upper bound of `Component`
T = TypeVar("T", bound="Component")


class WebaTagError(Exception):
    pass


class TagDescriptor(Generic[T]):
    def __init__(
        self,
        method: Callable[[T], Tag],
        selector: Optional[str] = None,
        extract: bool = False,
        clear: bool = False,
        strict: bool = True,
        src_tag: bool = False,
        comment: Optional[str] = None,
    ):
        self._method = method
        self._method_name = method.__name__
        self._selector = selector
        self._extract = extract
        self._clear = clear
        self._strict = strict
        self._comment = comment
        self._src_tag = src_tag

    def __get__(self, instance: Union[T, None], owner: Type[T]) -> Tag:
        # sourcery skip: remove-redundant-if
        if instance is None:
            class_path = f"{instance.__class__.__module__}.{instance.__class__.__qualname__}"
            raise WebaTagError(f"{self._method_name} is only accessible on instances of {class_path}")

        tag = instance._tags.get(self._method_name)  # type: ignore (we need to access private property)

        if tag is None and self._method_name not in instance._tags_called:  # pyright: ignore[reportPrivateUsage]
            found_tag = None

            if self._selector or self._comment:
                if self._comment and not self._selector:
                    found_tag = instance.select_comment(self._comment, remove_comment=self._extract)
                elif self._selector:
                    found_tag = instance.select_one(self._selector)

                    if self._comment:
                        found_tag = instance.select_comment(self._comment)

                if self._strict and not found_tag:
                    class_path = f"{instance.__class__.__module__}.{instance.__class__.__qualname__}"

                    raise WebaTagError(f"No tag with selector {self._selector or self._comment} found in {class_path}")

                if self._extract:
                    if found_tag:
                        if self._clear:
                            found_tag.clear()

                        found_tag = found_tag.extract()

                    if self._selector:
                        [t.decompose() for t in instance.select(self._selector)]
                    elif self._comment:
                        for comment in instance.select_comments(self._comment, remove_comments=True):
                            if not comment or isinstance(comment, NavigableString):
                                continue

                            comment.decompose()

                if found_tag and not self._extract and self._clear:
                    found_tag.clear()  # type: ignore

                if found_tag:
                    # TODO: Write test to check for this
                    if self._src_tag:
                        if not instance._has_src_tag_or_comment_component:  # type: ignore (we need to access private property)
                            instance._has_src_tag_or_comment_component = True  # type: ignore (we need to access private property)
                            instance._content = instance.src = found_tag  # type: ignore (we need to access private property)
                        else:
                            raise WebaTagError("Source tag has already been defined")

                    if not instance._is_component:  # type: ignore (we need to access private property)
                        found_tag = instance._tag_context_manager(found_tag)  # type: ignore (we need to access private property)

                    # check if method takes a tag as an argument
                    if len(self._method.__code__.co_varnames) > 1:
                        tag = self._method(instance, found_tag)  # type: ignore
                    if tag is None:
                        tag = found_tag

            else:
                tag = self._method(instance)

            instance._tags[self._method_name] = tag  # type: ignore (we need to access private property)
            instance._tags_called.add(self._method_name)  # type: ignore (we need to access private property)

        return cast(Tag, tag)
