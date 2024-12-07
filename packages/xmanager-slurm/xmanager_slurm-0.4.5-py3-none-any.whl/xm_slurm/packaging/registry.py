import dataclasses
from typing import Callable, Generic, ParamSpec, Sequence, Type, TypeVar

from xmanager import xm

T_co = TypeVar("T_co", covariant=True)
P = ParamSpec("P")
ExecutableSpecT = TypeVar("ExecutableSpecT", bound=xm.ExecutableSpec)


@dataclasses.dataclass(frozen=True)
class IndexedContainer(Generic[T_co]):
    index: int
    value: T_co


RegistrationCallable = Callable[
    [Sequence[IndexedContainer[xm.Packageable]]],
    Sequence[IndexedContainer[xm.Executable]],
]


_REGISTRY: dict[Type[xm.ExecutableSpec], RegistrationCallable] = {}


def register(
    *typs: Type[ExecutableSpecT],
) -> Callable[[RegistrationCallable], RegistrationCallable]:
    def decorator(
        registration_callable: RegistrationCallable,
    ) -> RegistrationCallable:
        global _REGISTRY
        for typ in typs:
            _REGISTRY[typ] = registration_callable
        return registration_callable

    return decorator


def route(
    typ: Type[ExecutableSpecT],
    packageables: Sequence[IndexedContainer[xm.Packageable]],
) -> Sequence[IndexedContainer[xm.Executable]]:
    global _REGISTRY
    return _REGISTRY[typ](packageables)
