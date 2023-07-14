from contextlib import AbstractAsyncContextManager
from typing import Any


class _AClosing(AbstractAsyncContextManager):
    """Async Closing Context Manager"""

    def __init__(self, obj: Any) -> None:
        self.obj = obj

    async def __aenter__(self) -> Any:
        return self.obj

    async def __aexit__(self, *exc_info) -> None:
        await self.obj.close()


aclosing = _AClosing
