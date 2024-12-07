import typing as tp

InstanceT_contra = tp.TypeVar("InstanceT_contra", contravariant=True)
GetterT_co = tp.TypeVar("GetterT_co", covariant=True)
SetterT_co = tp.TypeVar("SetterT_co", contravariant=True)


class Descriptor(tp.Protocol[GetterT_co, SetterT_co]):
    def __set_name__(self, owner: tp.Type[tp.Any], name: str) -> None: ...

    @tp.overload
    def __get__(
        self, instance: InstanceT_contra, owner: tp.Type[InstanceT_contra] | None = None
    ) -> GetterT_co: ...

    @tp.overload
    def __get__(self, instance: None, owner: tp.Type[InstanceT_contra]) -> GetterT_co: ...

    def __get__(
        self, instance: InstanceT_contra | None, owner: tp.Type[InstanceT_contra] | None = None
    ) -> GetterT_co: ...

    def __set__(self, instance: tp.Any, value: SetterT_co) -> None: ...
