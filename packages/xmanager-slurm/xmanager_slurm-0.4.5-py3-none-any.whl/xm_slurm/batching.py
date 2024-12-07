import asyncio
import collections
import dataclasses
import inspect
import time
import types
from typing import Any, Callable, Coroutine, Generic, ParamSpec, Sequence, TypeVar

T = TypeVar("T", contravariant=True)
R = TypeVar("R", covariant=True)
P = ParamSpec("P")


@dataclasses.dataclass(frozen=True, kw_only=True)
class Request:
    args: inspect.BoundArguments
    future: asyncio.Future


def stack_bound_arguments(
    signature: inspect.Signature, bound_arguments: Sequence[inspect.BoundArguments]
) -> inspect.BoundArguments:
    """Stacks bound arguments into a single bound arguments object."""
    stacked_args = collections.OrderedDict[str, Any]()
    for bound_args in bound_arguments:
        for name, value in bound_args.arguments.items():
            stacked_args.setdefault(name, [])
            stacked_args[name].append(value)
    return inspect.BoundArguments(signature, stacked_args)


class batch(Generic[R]):
    __slots__ = (
        "fn",
        "signature",
        "max_batch_size",
        "batch_timeout",
        "loop",
        "process_batch_task",
        "queue",
    )
    __name__: str = "batch"
    __qualname__: str = "batch"

    def __init__(
        self,
        fn: Callable[..., Coroutine[None, None, Sequence[R]]],
        /,
        *,
        max_batch_size: int,
        batch_timeout: float,
    ) -> None:
        self.fn = fn
        self.signature = inspect.signature(fn)

        self.max_batch_size = max_batch_size
        self.batch_timeout = batch_timeout

        self.loop: asyncio.AbstractEventLoop | None = None
        self.process_batch_task: asyncio.Task | None = None

        self.queue = asyncio.Queue[Request]()

    async def _process_batch(self):
        assert self.loop is not None
        while not self.loop.is_closed():
            batch = await self._wait_for_batch()
            assert len(batch) > 0

            bound_args = stack_bound_arguments(self.signature, [request.args for request in batch])
            futures = [request.future for request in batch]

            results_future = self.fn(*bound_args.args, *bound_args.kwargs)

            try:
                results = await results_future

                for result, future in zip(results, futures):
                    future.set_result(result)
            except Exception as e:
                for future in futures:
                    future.set_exception(e)

    async def _wait_for_batch(self) -> list[Request]:
        batch = [await self.queue.get()]

        batch_start_time = time.time()
        while True:
            remaining_batch_time_s = max(self.batch_timeout - (time.time() - batch_start_time), 0)

            try:
                request = await asyncio.wait_for(self.queue.get(), timeout=remaining_batch_time_s)
                batch.append(request)
            except asyncio.TimeoutError:
                break

            if (
                time.time() - batch_start_time >= self.batch_timeout
                or len(batch) >= self.max_batch_size
            ):
                break

        return batch

    def __get__(self, obj: Any, objtype: type) -> Any:
        del objtype
        if isinstance(self.fn, staticmethod):
            return self.__call__
        else:
            return types.MethodType(self, obj)

    @property
    def __func__(self) -> Callable[..., Coroutine[None, None, Sequence[R]]]:
        return self.fn

    @property
    def __wrapped__(self) -> Callable[..., Coroutine[None, None, Sequence[R]]]:
        return self.fn

    @property
    def __isabstractmethod__(self) -> bool:
        """Return whether the wrapped function is abstract."""
        return getattr(self.fn, "__isabstractmethod__", False)

    @property
    def _is_coroutine(self) -> bool:
        # TODO(jfarebro): py312 adds inspect.markcoroutinefunction
        # until then this is just a hack
        return asyncio.coroutines._is_coroutine  # type: ignore

    async def __call__(self, *args, **kwargs) -> R:
        if self.loop is None and self.process_batch_task is None:
            self.loop = asyncio.get_event_loop()
            self.process_batch_task = self.loop.create_task(self._process_batch())

        future = asyncio.Future[R]()
        bound_args = self.signature.bind(*args, **kwargs)
        self.queue.put_nowait(Request(args=bound_args, future=future))
        return await future
