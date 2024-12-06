import asyncio
import contextvars
import inspect
import os
from typing import (
    Any,
    Callable,
    Coroutine,
    Iterable,
    Optional,
    Pattern,
    Protocol,
    Type,
    TypeAlias,
    TypeVar,
    Union,
    overload,
)

from bs4 import BeautifulSoup
from bs4.element import Tag

from .env import env
from .tag import TagContextManager, TagDescriptor, TagMixins
from .types import TypedDictClass
from .utils import clean_comments, load_html_to_soup

weba_html_context: contextvars.ContextVar[Any] = contextvars.ContextVar("current_weba_html_context")


Incomplete: TypeAlias = Any
_SimpleStrainable: TypeAlias = str | bool | None | bytes | Pattern[str] | Callable[[str], bool] | Callable[[Tag], bool]
_Strainable: TypeAlias = _SimpleStrainable | Iterable[_SimpleStrainable]
_SimpleNormalizedStrainable: TypeAlias = (
    str | bool | None | Pattern[str] | Callable[[str], bool] | Callable[[Tag], bool]
)
_NormalizedStrainable: TypeAlias = _SimpleNormalizedStrainable | Iterable[_SimpleNormalizedStrainable]

Render = None | Coroutine[Any, Any, None]

T = TypeVar("T", bound="Component")
Y = TypeVar("Y")


# Define the tag decorator with overloads to handle different usage patterns
@overload
def tag(method: Callable[[T], Tag | TagContextManager]) -> TagDescriptor[T]: ...


@overload
def tag(
    selector: str,
    *,
    extract: Optional[bool] = False,
    clear: Optional[bool] = False,
    strict: Optional[bool] = True,
    src_tag: Optional[bool] = True,
) -> Callable[
    [Callable[[T, TagContextManager], None | Tag | TagContextManager] | Callable[[T], None | Tag | TagContextManager]],
    TagDescriptor[T],
]: ...


def tag(*args: Any, **kwargs: Any) -> Union[TagDescriptor[T], Callable[[Callable[[T], Any]], TagDescriptor[T]]]:  # type: ignore
    if len(args) == 1 and callable(args[0]):
        method = args[0]
        Component._tag_methods.append(method.__name__)  # type: ignore (we need to access private property)
        # This is the decorator usage without arguments
        return TagDescriptor(method)  # pyright: ignore[reportArgumentType]  # FIXME: Fix typing issue
    else:
        # This is the decorator usage with arguments
        selector = args[0] if args else None
        extract = kwargs.get("extract", False)
        clear = kwargs.get("clear", False)
        strict = kwargs.get("strict", True)
        comment = kwargs.get("comment", None)
        src_tag = kwargs.get("src_tag", False)

        def decorator(method: Callable[[T], None]) -> TagDescriptor[T]:
            Component._tag_methods.append(method.__name__)  # type: ignore (we need to access private property)

            return TagDescriptor(
                method,  # type: ignore
                selector=selector,
                extract=extract,
                clear=clear,
                strict=strict,
                comment=comment,
                src_tag=src_tag,
            )

        return decorator


# Define the tag decorator with overloads to handle different usage patterns
# TODO: Remove this
@overload
def comment(method: Callable[[T], Tag | TagContextManager]) -> TagDescriptor[T]: ...


@overload
def comment(
    selector: str,
    *,
    extract: Optional[bool] = False,
    clear: Optional[bool] = False,
    strict: Optional[bool] = True,
    src_tag: Optional[bool] = True,
) -> Callable[
    [Callable[[T, TagContextManager], None | Tag | TagContextManager] | Callable[[T], None | Tag | TagContextManager]],
    TagDescriptor[T],
]: ...


# TODO: Change from type Any to TypedDict class
def comment(*args: Any, **kwargs: Any) -> Union[TagDescriptor[T], Callable[[Callable[[T], Any]], TagDescriptor[T]]]:  # type: ignore
    kwargs["comment"] = args[0]

    return tag(None, **kwargs)  # type: ignore


class ComponentProtocol(Protocol):
    def render(
        self,
    ) -> Union[BeautifulSoup, Coroutine[Any, Any, Union[None, TagContextManager, Tag, BeautifulSoup]]]: ...


class ComponentContext(TypedDictClass):
    pass


# HACK: We are using a metaclass to ensure __init__ only gets called once
class Meta(type):
    def __call__(cls: Type[Y], *args: Any, **kwargs: Any) -> Y:
        # sourcery skip: instance-method-first-arg-name
        return cls.__new__(cls, *args, **kwargs)  # type: ignore


_component_loaded_src: dict[str, str] = {}


class Component(TagMixins, metaclass=Meta):
    _render_coro: Union[
        None,
        Coroutine[Any, Any, BeautifulSoup],
    ]
    _content: TagContextManager
    _component_content: TagContextManager
    _content_to_append: Union[BeautifulSoup, TagContextManager, list[Tag], "Component"]
    _tag_methods: list[str] = []  # Declare the class attribute
    _tags: dict[str, TagContextManager] = {}
    _tags_called: set[str] = set()
    _context_stack: list[Tag]
    _context_token: Optional[contextvars.Token[Any]]
    _render_cache: Optional[TagContextManager]
    _is_component = True
    _last_component: Optional["Component"]
    _first_component: bool
    _before_render_called: bool
    _after_render_called: bool
    _called_with_context_manager: bool
    # TODO: Maybe change the name of this attribute
    _has_src_tag_or_comment_component: bool = False

    src: Optional[str] | BeautifulSoup | Tag
    src_cache_key: Optional[str] = ""
    src_select_one: Optional[str] = None
    src_select_comment: Optional[str] = None

    def __new__(cls, *args: Any, **kwargs: Any):
        instance = super().__new__(cls)

        skip_render = kwargs.pop("__skip_render__", False)

        instance.src_cache_key = cls.__name__
        instance._render_cache = None
        instance._context_stack = []
        instance._last_component = None
        instance._render_coro = None
        instance._first_component = False
        instance._after_render_called = False
        instance._before_render_called = False
        instance._called_with_context_manager = False
        instance._tags = {}
        instance._tags_called = set()

        # # Define a function to cache the result of the render method
        # def cache_render_result(func: Callable[..., Any]) -> Callable[..., Any]:
        #     def wrapper(*args: Any, **kwargs: Any) -> Any:
        #         if not instance._render_cache:
        #             instance._render_cache = func(*args, **kwargs)
        #
        #         return instance._render_cache
        #
        #     return wrapper

        # Wrap the render method with the caching function
        # instance.render = cache_render_result(instance.render)

        # Check if the html context is set, otherwise create a new one
        html_context = weba_html_context.get(None)

        if html_context is None:
            # Create a new HTML context for this component
            html_context = instance
            # Set the new HTML context in the context variable
            instance._context_token = weba_html_context.set(html_context)
            instance._first_component = True

        instance.html_context = html_context  # type: ignore
        instance._weba_html_context = html_context

        if skip_render:
            return instance

        instance.__init__(*args, **kwargs)

        cls_path = inspect.getfile(cls)
        cls_dir = os.path.dirname(cls_path)

        if env.is_prd:
            global _component_loaded_src

            loaded_src_key = f"{cls.__name__}_{cls_path}_{instance.src_cache_key}"

            content = _component_loaded_src.get(loaded_src_key)

            if not content:
                src = instance.src or (cls.src if hasattr(cls, "src") else "--html")

                if src:
                    content = _component_loaded_src[loaded_src_key] = str(src)
                else:
                    content = "--html"
        else:
            content = instance.src or (cls.src if hasattr(cls, "src") else "--html")

        instance._content = load_html_to_soup(content, base_dir=cls_dir)  # type: ignore (we need to access private property)

        selectors = [
            ("src_select_one", "select_one"),
            ("src_select_comment", "select_comment"),
            # Add more selectors here if needed
        ]

        for attr_name, method_name in selectors:
            if hasattr(instance._content, attr_name) and getattr(instance, attr_name):
                selector_value = getattr(instance, attr_name)
                select_method = getattr(instance, method_name)
                if not (selected_tag := select_method(str(selector_value))):
                    raise ValueError(f"Could not find tag with selector '{selector_value}' in component {cls.__name__}")

                instance.src = instance._content = selected_tag  # type: ignore
                break

        if (
            not asyncio.iscoroutinefunction(instance.render)
            and not asyncio.iscoroutinefunction(instance.before_render)
            and not asyncio.iscoroutinefunction(instance.after_render)
        ):
            instance._render_sync_component()

        return instance

    def _render_sync_component(self):
        self._before_render()
        self._render_tags()

        render_result = self.render()

        self._after_render()

        # If render_result is not None, use it as the content to append
        # Otherwise, use self._content if it's not None
        self._content = self._content_to_append = render_result if render_result is not None else self.content  # type: ignore

        self._append_contexts()

        # if not self._first_component and not asyncio.iscoroutine(self) and not self._after_render_called:
        if not self._first_component:
            self._weba_html_context._last_component = self  # type: ignore

    def __init__(self):
        pass

    def render(
        self,
    ) -> Union[
        BeautifulSoup,
        Coroutine[Any, Any, Union[None, TagContextManager, Tag, BeautifulSoup]],
        TagContextManager,
        Tag,
        None,
    ]:
        # This method should be overridden by subclasses to modify self._content
        # It can return a BeautifulSoup object, a coroutine, or None
        return self._render_cache or self._content

    def before_render(
        self,
    ) -> (
        Coroutine[Any, Any, Union[None, TagContextManager, Tag, BeautifulSoup]]
        | Union[BeautifulSoup, TagContextManager, Tag, None]
        | None
    ):
        pass

    def after_render(
        self,
    ) -> (
        Coroutine[Any, Any, Union[None, TagContextManager, Tag, BeautifulSoup]]
        | Union[BeautifulSoup, TagContextManager, Tag, None]
        | None
    ):
        pass

    def _append_contexts(self):
        if isinstance(self._content_to_append, Tag):
            self._append_to_context(self._content_to_append)  # type: ignore
        elif self._content_to_append is not None and isinstance(self._content_to_append, list):  # type: ignore
            [self._append_to_context(tag) for tag in self._content_to_append]  # type: ignore

    def _append_to_context(self, content: Optional[Union[BeautifulSoup, TagContextManager]] = None):
        if not content:
            return

        try:
            if self._weba_html_context._context_stack:  # type: ignore (we need to access private property)
                self._weba_html_context._context_stack[-1].append(content)  # type: ignore (we need to access private property)
        except ValueError as e:
            if str(e) != "Tag.index: element not in tag":
                raise

    def __await__(self):  # type: ignore
        yield from self._execute_render().__await__()

        return self  # type: ignore

    def _set_weba_context(self) -> None:
        if not weba_html_context.get(None):
            self._context_token = weba_html_context.set(self)

        # NOTE: this makes sure the content is available in the context manager
        if self._weba_html_context._context_stack:  # type: ignore (we need to access private property)
            if content := self._weba_html_context._context_stack.pop():
                self._content = self._content_to_append = content  # type: ignore (we need to access private property)

    def __enter__(self):
        self._set_weba_context()

        return self

    async def __aenter__(self):
        await self._execute_render()

        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self._reset_weba_context()

    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self._reset_weba_context()

    def _reset_weba_context(self) -> None:
        if hasattr(self, "_context_token") and self._context_token is not None:
            weba_html_context.reset(self._context_token)
            self._context_token = None

    def reset_context(self) -> None:
        self._reset_weba_context()

    def reset(self) -> None:
        self._reset_weba_context()

    def output_ready(self, _):
        return str(self.content)

    # @cached_property
    # def component(self):
    #     return self._content
    @property
    def attrs(self) -> dict[str, Any]:
        return self._content.attrs

    @attrs.setter
    def attrs(self, value: dict[str, Any]):  # type: ignore
        self._content.attrs = value

    # if a method doesn't exist try calling it on self._content
    def __getattr__(self, name: str):
        if name not in ["_content", "context"] and hasattr(self.content, name):
            response = getattr(self.content, name)

            if isinstance(response, Tag):
                return self._tag_context_manager(response)

            return response

        # raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _tag_context_manager(self, tag: Tag):
        if tag._is_component:
            return tag

        return TagContextManager(tag, self._weba_html_context)  # type: ignore

    def __str__(self):
        return clean_comments(str(self.content))

    async def _execute_render(self):
        await self._async_before_render()

        self._render_tags()

        if asyncio.iscoroutinefunction(self.render):
            content_to_append = await self.render()
        else:
            content_to_append = self.render()

        content_to_append = content_to_append or self.content

        if content_to_append:
            self._content = content_to_append  # type: ignore

        await self._async_after_render()  # type: ignore

        self._append_to_context(content_to_append)  # type: ignore

        if not self._first_component:
            self._weba_html_context._last_component = content_to_append  # type: ignore

    def _render_tags(self):
        # loop through the _tags that are set and just call them to make sure they get added to the content
        for tag_method in self.__class__._tag_methods:
            getattr(self, tag_method)

    def _generic_render_hook(
        self, hook_type: str, is_async: bool = False
    ) -> Union[Callable[[], Any], Callable[[], Coroutine[Any, Any, None]]]:
        attr_name: str = f"_{hook_type}_render_called"
        method_name: str = f"{hook_type}_render"

        def sync_wrapper() -> None:
            if getattr(self, attr_name, False):
                return

            method: Optional[Callable[[], Any]] = getattr(self, method_name, None)

            if method and not asyncio.iscoroutinefunction(method):
                setattr(self, attr_name, True)
                method()

        async def async_wrapper() -> None:
            if getattr(self, attr_name, False):
                return

            method: Optional[Union[Callable[[], None], Callable[[], Coroutine[Any, Any, None]]]] = getattr(
                self, method_name, None
            )

            if not method:
                return

            setattr(self, attr_name, True)

            if asyncio.iscoroutinefunction(method):
                await method()
            else:
                await asyncio.to_thread(method)

        return async_wrapper if is_async else sync_wrapper

    def __iter__(self):
        for child in iter(self.contents):  # type: ignore
            yield self._tag_context_manager(child)  # type: ignore

    async def _async_after_render(self) -> None:
        await self._generic_render_hook("after", is_async=True)()

    def _after_render(self) -> None:
        self._generic_render_hook("after", is_async=False)()

    async def _async_before_render(self) -> None:
        await self._generic_render_hook("before", is_async=True)()

    def _before_render(self) -> None:
        self._generic_render_hook("before", is_async=False)()

    @property
    def content(self) -> TagContextManager:
        return self._render_cache or self._content
