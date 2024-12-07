from typing import Mapping, TypedDict

from xmanager import xm


class JobArgs(TypedDict, total=False):
    args: xm.UserArgs
    env_vars: Mapping[str, str]


def get_args_for_python_entrypoint(
    entrypoint: xm.ModuleName | xm.CommandList,
) -> xm.SequentialArgs:
    match entrypoint:
        case xm.ModuleName():
            entrypoint_args = ["-m", entrypoint.module_name]
        case xm.CommandList():
            entrypoint_args = entrypoint.commands
        case _:
            raise TypeError(f"Invalid entrypoint type: {type(entrypoint)}")
    return xm.SequentialArgs.from_collection(entrypoint_args)
