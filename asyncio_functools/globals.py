from typing import AsyncGenerator, AsyncIterable, Callable, TypeVar

T = TypeVar('T')


async def aenumerate(values: AsyncIterable[T]) -> AsyncIterable[tuple[int, T]]:
    """As enumerate, but for AsyncIterable

    Example:
        async def async_generator() -> AsyncGenerator[int, None]:
            for i in range(10):
                yield i

        # is not working:
        for i, item in enumerate(async_generator()):
            print(i, item)
        >> TypeError: 'async_generator' object is not iterable

        # is working
        async for i, item in aenumerate(async_generator()):
            print(i, item)
        >> 0 0, 1 1, 2 2, 3 3, 4 4, 5 5, 6 6, 7 7, 8 8, 9 9,
    """
    idx = 0
    async for value in values:
        yield idx, value
        idx += 1


async def alist(values: AsyncIterable[T]) -> list[T]:
    """As list, but for AsyncIterable

    Example:
        async def async_generator() -> AsyncGenerator[int, None]:
            for i in range(10):
                yield i

        results = await alist(async_generator())
        results == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    return [item async for item in values]


async def amap(func: Callable, values: AsyncIterable[T]) -> AsyncIterable[T]:
    """As map, but for AsyncIterable

    Example:
        async def async_generator() -> AsyncGenerator[int, None]:
            for i in range(10):
                yield i

        # is not working:
        results = [item for item in map(str, async_generator())]
        >> TypeError: 'async_generator' object is not iterable

        # is working
        results = [item async for item in amap(str, async_generator())]
        results == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    """
    async for value in values:
        yield func(value)


async def azip(*args: AsyncIterable[T]) -> AsyncIterable[tuple[T, ...]]:
    """As zip, but for AsyncIterable

    Example:
        async def async_generator1() -> AsyncGenerator[int, None]:
            for i in range(10):
                yield i

        async def async_generator2() -> AsyncGenerator[int, None]:
            for i in range(5, 10):
                yield i

        # is not working:
        for i, j in zip(async_generator1(), async_generator2()):
            print(i, j)
        >> TypeError: 'async_generator' object is not iterable

        # is working:
        async for i, j in azip(async_generator1(), async_generator2()):
            print(i, j, end=', ')
        >> 5 0, 6 1, 7 2, 8 3, 9 4,
    """

    async def generator(_iterable: AsyncIterable[T]) -> AsyncGenerator[T, None]:
        async for _item in _iterable:
            yield _item

    stack = [generator(iterable) for iterable in args]
    first_gen = stack[0]
    bunch = ()
    while stack:
        gen = stack.pop(0)
        if gen == first_gen and len(bunch) != 0:
            yield bunch
            bunch = ()
        try:
            value = await gen.asend(None)
            bunch += (value,)
        except (StopIteration, StopAsyncIteration):
            break
        stack.append(gen)
