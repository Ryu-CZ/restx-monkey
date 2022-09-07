import itertools
import os
import pathlib
import typing

__all__ = (
    "is_writable",
    "replace_static_swagger_files",
)


def is_writable(p: typing.Union[pathlib.Path, str]) -> bool:
    """
    Is path writable/readable file?

    :param p: path to check
    :return: Is path writable/readable file?
    """
    p = pathlib.Path(p)
    if p.exists() and p.is_file():
        return os.access(p, os.W_OK | os.R_OK)
    return p.parent.exists() and os.access(p.parent, os.W_OK | os.R_OK)


def replace_static_swagger_files(target_folder: typing.Union[pathlib.Path, str, None] = None) -> None:
    """
    Use restx_monkey `static` assets to replace flask_restx `static` assets. Only if target files permissions allows it.

    :param target_folder: folder to replace swagger ui in, if not given flask_restx static is used
    """
    import flask_restx
    my_static = pathlib.Path(__file__).parent / "static"
    lib_static = pathlib.Path(target_folder) if target_folder else pathlib.Path(flask_restx.__file__).parent / "static"

    has_permissions = all(
        map(
            is_writable,
            itertools.chain(
                (lib_static,),
                lib_static.iterdir(),
            )
        )
    )
    if not has_permissions:
        # this is not must have feature, skip
        return

    # replace old files in static
    for src_path in my_static.iterdir():
        if src_path.is_file():
            (lib_static / src_path.name).write_bytes(src_path.read_bytes())
