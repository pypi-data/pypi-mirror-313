import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress

import psutil
from litestar import Litestar

from ..env import env


# https://docs.litestar.dev/2/usage/applications.html
@asynccontextmanager
async def node_dev_lifespan_handler(_app: Litestar) -> AsyncGenerator[None, None]:
    if env.is_prd:
        yield
        return

    node = await asyncio.create_subprocess_exec(*env.node_dev_cmd)

    try:
        yield
    finally:
        with suppress(psutil.NoSuchProcess):
            if parent := psutil.Process(node.pid):
                for child in parent.children(recursive=True):
                    child.terminate()
