import os
from typing import Any, Tuple

UNKNOWN_TYPE = "Unknown"
TYPE_NAME_MAP = {
    1: "Modules",
    2: "Class Modules",
    3: "Forms",
    11: "ActiveX Designer",
    100: "Microsoft Excel Objects",
}
FILE_EXT = "bas"


def get_vb_comp_paths(
    vb_project_dir: str,
    vb_comp: Any,
) -> Tuple[str, str]:

    vb_comp_file_name = ".".join(
        (
            vb_comp.name,
            FILE_EXT,
        )
    )

    vb_comp_dir = os.path.join(
        vb_project_dir,
        TYPE_NAME_MAP.get(vb_comp.Type, UNKNOWN_TYPE),
    )

    vb_comp_file_path = os.path.join(
        vb_comp_dir,
        vb_comp_file_name,
    )

    return (
        vb_comp_dir,
        vb_comp_file_path,
    )
