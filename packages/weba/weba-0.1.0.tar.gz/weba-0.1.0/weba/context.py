import contextvars
from functools import cached_property
from typing import Any, ClassVar, TypeVar

T = TypeVar("T")


class Context:
    weba_context: ClassVar[contextvars.ContextVar[Any]] = contextvars.ContextVar("current_weba_context")

    @cached_property
    def context(self):
        context = self.weba_context.get(None)

        if not context:
            self._weba_context_token = self.weba_context.set(self)
            context = self

        return context

    async def __aenter__(self):
        return self.context

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        if hasattr(self, "_weba_context_token"):
            self.weba_context.reset(self._weba_context_token)
