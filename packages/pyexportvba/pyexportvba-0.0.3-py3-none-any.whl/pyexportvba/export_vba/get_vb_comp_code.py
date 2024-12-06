from typing import Any, Optional


def get_vb_comp_code(vb_comp: Any) -> Optional[str]:
    n_lines = vb_comp.CodeModule.CountOfLines

    if n_lines == 0:
        return None

    code_str = str(
        vb_comp.CodeModule.Lines(
            1,
            n_lines,
        )
    )

    code_str = code_str.replace("\r\n", "\n")

    return code_str
