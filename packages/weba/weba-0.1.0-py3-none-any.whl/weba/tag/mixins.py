import contextvars
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
)

from bs4.element import Comment, Tag

from weba.utils import update_kwargs

if TYPE_CHECKING:
    from ..component import Component, TagContextManager

weba_html_context: contextvars.ContextVar[Any] = contextvars.ContextVar("current_weba_html_context")


methods = [
    method
    for method in dir(Tag)
    if callable(getattr(Tag, method))
    # and not method.startswith("__")
    and method not in ["get", "find_comment", "find_comments"]
    and not method.startswith("_")
]


class TagMixins(Tag):
    _content: Optional["TagContextManager"]
    _html: "Component"
    _weba_html_context: "Component"
    _is_component = True

    def _wrap_result(self, result: "TagContextManager"):  # type: ignore
        if isinstance(result, list):
            return [self._wrap_result(item) for item in result]  # type: ignore
        elif isinstance(result, Tag) and callable(getattr(self, "_tag_context_manager", None)):  # type: ignore
            return self._tag_context_manager(result)  # type: ignore
        elif callable(result):

            def wrapped_method(*args: Any, **kwargs: Any):  # type: ignore
                if self._content is None:  # type: ignore
                    method_result = result(*args, **kwargs)
                else:
                    method_result = getattr(self._content, result.__name__)(*args, **kwargs)  # type: ignore
                return self._wrap_result(method_result)  # type: ignore

            return wrapped_method
        else:
            return result

    def __getattribute__(self, name: str) -> "TagContextManager":
        if name in methods:
            return self._wrap_result(super().__getattribute__(name))  # type: ignore

        return super().__getattribute__(name)

    def find_comment(self, string: str, remove_comment: bool = False) -> "TagContextManager | None":
        tag = self.find(string=lambda text: isinstance(text, Comment) and text.strip() == string.strip())

        if not tag:
            return None

        new_tag = self._wrap_result(  # type: ignore
            tag.find_next()  # type: ignore
        )

        if remove_comment:
            tag.extract()

        return new_tag  # type: ignore

    def select_comment(self, string: str, remove_comment: bool = False) -> "TagContextManager | None":
        return self.find_comment(string, remove_comment)

    def find_comments(self, string: str, remove_comments: bool = False) -> list["TagContextManager"]:
        comments = self.find_all(string=lambda text: isinstance(text, Comment) and text.strip() == string.strip())  # type: ignore

        tags: list["TagContextManager"] = []

        for comment in comments:
            if not comment:
                continue

            tags.append(self._wrap_result(comment.find_next()))  # type: ignore

            if remove_comments:
                comment.extract()

        return tags

    def select_comments(self, string: str, remove_comments: bool = False) -> list["TagContextManager"]:
        return self.find_comments(string, remove_comments=remove_comments)

    def new_tag(
        self,
        name_: str,
        namespace: Optional[str] = None,
        nsprefix: Optional[str] = None,
        attrs: Optional[dict[str, str]] = None,
        sourceline: Optional[int] = None,
        sourcepos: Optional[int] = None,
        **kwattrs: str,
    ) -> "TagContextManager":
        attrs = attrs or {}

        kwattrs.update(attrs)

        update_kwargs(kwattrs)

        tag = self.get(Tag, Tag)(  # type: ignore
            None,
            self.builder,
            name_,
            namespace,
            nsprefix,
            kwattrs,
            sourceline=sourceline,
            sourcepos=sourcepos,  # type: ignore
        )

        return self._wrap_result(tag)  # type: ignore
