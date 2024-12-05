import asyncio
import logging
from collections.abc import AsyncIterator, Awaitable, Sequence
from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    Protocol,
    TypeVar,
    Union,
    cast,
    runtime_checkable,
)

from reactivex import Observable, abc, from_iterable
from reactivex import from_future as rx_from_future
from reactivex.disposable import Disposable as RxDisposable

# Type definitions
T = TypeVar("T")
TSource = TypeVar("TSource")
TResult = TypeVar("TResult")


@runtime_checkable
class DisposableProtocol(Protocol):
    def dispose(self) -> None: ...


class HybridObservable(Observable[T], Generic[T]):
    """
    A hybrid observable that supports both synchronous and asynchronous operations.
    Provides compatibility between ReactiveX and asyncio.
    """

    _observable: Observable[T]

    def __init__(self, observable: Observable[T]):
        """
        Initialize the hybrid observable with a regular observable.

        Args:
            observable: The underlying ReactiveX observable
        """
        super().__init__(observable._subscribe)
        self._observable = observable

    def run(self) -> T:
        """
        Run the observable synchronously and return the last value.

        Returns:
            The last value emitted by the observable
        """
        return cast(T, self._observable.run())

    def pipe(self, *operators: Callable[[Any], Any]) -> Any:
        """
        Apply a series of operators to the observable.

        Args:
            *operators: The operators to apply

        Returns:
            A new HybridObservable with the operators applied
        """
        return HybridObservable(self._observable.pipe(*operators))

    def subscribe(
        self,
        on_next: Union[Callable[[T], None], abc.ObserverBase[T], None] = None,
        on_error: Union[Callable[[Exception], None], None] = None,
        on_completed: Union[Callable[[], None], None] = None,
        *,
        scheduler: Optional[abc.SchedulerBase] = None,
    ) -> abc.DisposableBase:
        """
        Subscribe to the observable with synchronous callbacks.
        """
        return self._observable.subscribe(on_next, on_error, on_completed, scheduler=scheduler)

    async def arun(self) -> T:
        """
        Run the observable asynchronously and return the last value.

        Returns:
            The last value emitted by the observable

        Raises:
            asyncio.InvalidStateError: If the observable completes without emitting a value
            Exception: Any error that occurred during observation
        """
        future: asyncio.Future[T] = asyncio.Future()
        last_value: Optional[T] = None
        error_occurred = False

        def on_next(value: T) -> None:
            nonlocal last_value
            last_value = value

        def on_error(error: Exception) -> None:
            nonlocal error_occurred
            error_occurred = True
            if not future.done():
                logging.error(f"Error in observable: {error}")
                future.set_exception(error)

        def on_completed() -> None:
            if not future.done():
                if error_occurred:
                    return
                if last_value is not None:
                    future.set_result(last_value)
                else:
                    future.set_exception(
                        asyncio.InvalidStateError("Observable completed without emitting a value")
                    )

        disposable = self.subscribe(on_next, on_error, on_completed)

        try:
            return await future
        finally:
            disposable.dispose()

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
        try:
            return await asyncio.wait_for(self.arun(), timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(f"Observable operation timed out after {timeout} seconds") from None

    async def apipe(
        self, *operators: Callable[[Observable[Any]], Observable[Any]]
    ) -> "HybridObservable[Any]":
        """
        Asynchronous version of pipe.

        Args:
            *operators: The operators to apply

        Returns:
            A new HybridObservable with the operators applied
        """
        return HybridObservable(self._observable.pipe(*operators))

    async def asubscribe(
        self,
        on_next: Union[Callable[[T], Awaitable[Any]], None] = None,
        on_error: Union[Callable[[Exception], Awaitable[Any]], None] = None,
        on_completed: Union[Callable[[], Awaitable[Any]], None] = None,
    ) -> RxDisposable:
        """
        Subscribe asynchronously to the observable sequence.
        """
        future: asyncio.Future[None] = asyncio.Future()

        async def async_on_next(value: T) -> None:
            if on_next:
                await on_next(value)

        async def async_on_error(error: Exception) -> None:
            if on_error:
                await on_error(error)
            if not future.done():
                future.set_exception(error)

        async def async_on_completed() -> None:
            if on_completed:
                await on_completed()
            if not future.done():
                future.set_result(None)

        def next_fn(x: T) -> None:
            asyncio.create_task(async_on_next(x))

        def error_fn(e: Exception) -> None:
            asyncio.create_task(async_on_error(e))

        def completed_fn() -> None:
            asyncio.create_task(async_on_completed())

        disposable = self.subscribe(next_fn, error_fn, completed_fn)

        def cancel_subscription() -> None:
            disposable.dispose()
            if not future.done():
                future.cancel()

        return RxDisposable(cancel_subscription)

    async def asubscribe_with_backpressure(
        self, on_next: Optional[Callable[[T], Awaitable[Any]]] = None, max_queue_size: int = 100
    ) -> RxDisposable:
        """
        Subscribe asynchronously with backpressure control.

        Args:
            on_next: Async callback for next value
            max_queue_size: Maximum size of the internal queue

        Returns:
            A disposable object to cancel the subscription
        """
        queue: asyncio.Queue[T] = asyncio.Queue(maxsize=max_queue_size)

        async def process_queue() -> None:
            while True:
                try:
                    value = await queue.get()
                    if on_next:
                        await on_next(value)
                    queue.task_done()
                except asyncio.CancelledError:
                    break

        process_task = asyncio.create_task(process_queue())

        def on_next_with_backpressure(value: T) -> None:
            if not process_task.done():
                queue.put_nowait(value)

        disposable = self.subscribe(on_next_with_backpressure)

        def cleanup() -> None:
            process_task.cancel()
            disposable.dispose()

        return RxDisposable(cleanup)

    async def __aiter__(self) -> "AsyncIterator[T]":
        """
        Async iterator implementation.
        """
        queue: asyncio.Queue[Union[T, Exception]] = asyncio.Queue(maxsize=100)
        done = asyncio.Event()
        subscription: Optional[abc.DisposableBase] = None

        def on_next(value: T) -> None:
            if not queue.full():
                queue.put_nowait(value)

        def on_completed() -> None:
            done.set()

        def on_error(error: Exception) -> None:
            if not done.is_set():
                queue.put_nowait(error)
                done.set()

        subscription = self.subscribe(on_next, on_error, on_completed)

        try:
            while not done.is_set() or not queue.empty():
                try:
                    item = await queue.get()
                    if isinstance(item, Exception):
                        raise item
                    yield item
                except asyncio.CancelledError:
                    break
        finally:
            if subscription:
                subscription.dispose()

    def dispose(self) -> None:
        """
        Synchronous cleanup of resources.
        """
        if isinstance(self._observable, DisposableProtocol):
            self._observable.dispose()

    async def dispose_async(self) -> None:
        """
        Asynchronous cleanup of resources.
        Handles both synchronous and asynchronous disposal.
        """
        # Führe synchrone dispose aus
        self.dispose()

        # Warte auf ausstehende Tasks oder Futures
        pending_tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
        if pending_tasks:
            await asyncio.gather(*pending_tasks, return_exceptions=True)

    @classmethod
    def from_iterable(
        cls: type["HybridObservable[TSource]"],
        iterable: Union[list[TSource], tuple[TSource, ...], set[TSource]],
    ) -> "HybridObservable[TSource]":
        """
        Create a HybridObservable from an iterable.
        """
        return cls(from_iterable(iterable))

    @classmethod
    async def from_async_iterable(
        cls: type["HybridObservable[TSource]"], async_iterable: AsyncIterator[TSource]
    ) -> "HybridObservable[TSource]":
        """
        Create a HybridObservable from an async iterable.
        """

        async def to_list(ait: AsyncIterator[TSource]) -> Sequence[TSource]:
            return [item async for item in ait]

        items = await to_list(async_iterable)
        return cls(from_iterable(items))

    @classmethod
    def from_future(
        cls: type["HybridObservable[TSource]"], future: asyncio.Future[TSource]
    ) -> "HybridObservable[TSource]":
        """
        Create a HybridObservable from a future.
        """
        return cls(rx_from_future(future))
