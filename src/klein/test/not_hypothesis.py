from functools import wraps
from itertools import product
from typing import Callable, Iterable, Tuple, TypeVar


T = TypeVar("T")
S = TypeVar("S")


def given(
    *args: Callable[[], Iterable[T]],
    **kwargs: Callable[[], Iterable[T]],
) -> Callable[[Callable[..., None]], Callable[..., None]]:
    def decorator(testMethod: Callable[..., None]) -> Callable[..., None]:
        @wraps(testMethod)
        def realTestMethod(self: S) -> None:
            everyPossibleArgs = product(
                *[eachFactory() for eachFactory in args]
            )
            everyPossibleKwargs = product(
                *[
                    [(name, eachValue) for eachValue in eachFactory()]
                    for (name, eachFactory) in kwargs.items()
                ]
            )
            everyPossibleSignature = product(
                everyPossibleArgs, everyPossibleKwargs
            )
            # not quite the _full_ cartesian product but the whole point is
            # that we're making a feeble attempt at this rather than bringing
            # in hypothesis.
            for (computedArgs, computedPairs) in everyPossibleSignature:
                computedKwargs = dict(computedPairs)
                testMethod(self, *computedArgs, **computedKwargs)

        return realTestMethod

    return decorator


def binary() -> Callable[[], Iterable[bytes]]:
    """
    Generate some binary data.
    """

    def params() -> Iterable[bytes]:
        return [b"data", b"data data data", b"\x00" * 50]

    return params


def ascii_text(min_size: int = 0) -> Callable[[], Iterable[str]]:
    """
    Generate some ASCII strs.
    """

    def params() -> Iterable[str]:
        yield from [
            "latin1-text",
            "some more latin1 text",
            "hére is latin1 text",
        ]
        if not min_size:
            yield ""

    return params


def latin1_text(min_size: int = 0) -> Callable[[], Iterable[str]]:
    """
    Generate some strings encodable as latin1
    """

    def params() -> Iterable[str]:
        yield from [
            "latin1-text",
            "some more latin1 text",
            "hére is latin1 text",
        ]
        if not min_size:
            yield ""

    return params


def text(
    min_size: int = 0, alphabet: str = "ignored"
) -> Callable[[], Iterable[str]]:
    """
    Generate some text.
    """

    def params() -> Iterable[str]:
        yield from latin1_text(min_size)()
        yield "\N{SNOWMAN}"

    return params


def textHeaderPairs() -> Callable[[], Iterable[Iterable[Tuple[str, str]]]]:
    """ """


def bytesHeaderPairs() -> Callable[[], Iterable[Iterable[Tuple[str, bytes]]]]:
    """ """


def booleans() -> Callable[[], Iterable[bool]]:
    def parameters() -> Iterable[bool]:
        yield True
        yield False

    return parameters


def jsonObjects() -> Callable[[], Iterable[object]]:
    def parameters() -> Iterable[object]:
        yield {}
        yield {"hello": "world"}
        yield {"here is": {"some": "nesting"}}
        yield {
            "and": "multiple",
            "keys": {
                "with": "nesting",
                "and": 1234,
                "numbers": ["with", "lists", "too"],
            },
        }
    return parameters
