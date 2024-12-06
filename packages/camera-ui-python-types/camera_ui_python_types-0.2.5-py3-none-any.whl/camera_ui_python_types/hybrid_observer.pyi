import asyncio
from collections.abc import AsyncIterator, Awaitable
from reactivex import Observable, abc as abc
from reactivex.disposable import Disposable as RxDisposable
from typing import Any, Callable, Generic, Protocol, TypeVar

T = TypeVar('T')
TSource = TypeVar('TSource')
TResult = TypeVar('TResult')

class DisposableProtocol(Protocol):
    def dispose(self) -> None: ...

class HybridObservable(Observable[T], Generic[T]):
    """
    A hybrid observable that supports both synchronous and asynchronous operations.
    Provides compatibility between ReactiveX and asyncio.
    """
    _observable: Observable[T]
    def __init__(self, observable: Observable[T]) -> None:
        """
        Initialize the hybrid observable with a regular observable.

        Args:
            observable: The underlying ReactiveX observable
        """
    def run(self) -> T:
        """
        Run the observable synchronously and return the last value.

        Returns:
            The last value emitted by the observable
        """
    def pipe(self, *operators: Callable[[Any], Any]) -> Any:
        """
        Apply a series of operators to the observable.

        Args:
            *operators: The operators to apply

        Returns:
            A new HybridObservable with the operators applied
        """
    def subscribe(self, on_next: Callable[[T], None] | abc.ObserverBase[T] | None = None, on_error: Callable[[Exception], None] | None = None, on_completed: Callable[[], None] | None = None, *, scheduler: abc.SchedulerBase | None = None) -> abc.DisposableBase:
        """
        Subscribe to the observable with synchronous callbacks.
        """
    async def arun(self) -> T:
        """
        Run the observable asynchronously and return the last value.

        Returns:
            The last value emitted by the observable

        Raises:
            asyncio.InvalidStateError: If the observable completes without emitting a value
            Exception: Any error that occurred during observation
        """
    async def arun_with_timeout(self, timeout: float) -> T:
        """
        Run the observable asynchronously with a timeout.

        Args:
            timeout: Maximum time to wait in seconds

        Returns:
            The last value emitted by the observable

        Raises:
            TimeoutError: If the operation times out
        """
    async def apipe(self, *operators: Callable[[Observable[Any]], Observable[Any]]) -> HybridObservable[Any]:
        """
        Asynchronous version of pipe.

        Args:
            *operators: The operators to apply

        Returns:
            A new HybridObservable with the operators applied
        """
    async def asubscribe(self, on_next: Callable[[T], Awaitable[Any]] | None = None, on_error: Callable[[Exception], Awaitable[Any]] | None = None, on_completed: Callable[[], Awaitable[Any]] | None = None) -> RxDisposable:
        """
        Subscribe asynchronously to the observable sequence.
        """
    async def asubscribe_with_backpressure(self, on_next: Callable[[T], Awaitable[Any]] | None = None, max_queue_size: int = 100) -> RxDisposable:
        """
        Subscribe asynchronously with backpressure control.

        Args:
            on_next: Async callback for next value
            max_queue_size: Maximum size of the internal queue

        Returns:
            A disposable object to cancel the subscription
        """
    async def __aiter__(self) -> AsyncIterator[T]:
        """
        Async iterator implementation.
        """
    def dispose(self) -> None:
        """
        Synchronous cleanup of resources.
        """
    async def dispose_async(self) -> None:
        """
        Asynchronous cleanup of resources.
        Handles both synchronous and asynchronous disposal.
        """
    @classmethod
    def from_iterable(cls, iterable: list[TSource] | tuple[TSource, ...] | set[TSource]) -> HybridObservable[TSource]:
        """
        Create a HybridObservable from an iterable.
        """
    @classmethod
    async def from_async_iterable(cls, async_iterable: AsyncIterator[TSource]) -> HybridObservable[TSource]:
        """
        Create a HybridObservable from an async iterable.
        """
    @classmethod
    def from_future(cls, future: asyncio.Future[TSource]) -> HybridObservable[TSource]:
        """
        Create a HybridObservable from a future.
        """
