import logging
import os

import win32com.client

_logger = logging.getLogger(__name__)

UNKNOWN_TYPE = "Unknown"
TYPE_NAME_MAP = {
    1: "Modules",
    2: "Class Modules",
    3: "Forms",
    11: "ActiveX Designer",
    100: "Microsoft Excel Objects",
}


def export_vba_from_excel_app(output_path: str) -> None:

    excel = win32com.client.Dispatch("Excel.Application")

    for vb_project in excel.VBE.VBProjects:

        vb_project_name = vb_project.name

        vb_project_dir = os.path.join(output_path, vb_project_name)

        _logger.info(
            'processing VB Project "%s" in "%s"',
            vb_project_name,
            vb_project_dir,
        )

        for vb_comp in vb_project.VBComponents:

            vb_comp_type = TYPE_NAME_MAP.get(vb_comp.Type, UNKNOWN_TYPE)
            vb_comp_name = vb_comp.name

            vb_comp_count = vb_comp.CodeModule.CountOfLines

            if vb_comp_count == 0:

                continue

            vb_comp_dir = os.path.join(
                vb_project_dir,
                vb_comp_type,
            )

            os.makedirs(vb_comp_dir, exist_ok=True)

            vb_comp_file_path = os.path.join(
                vb_comp_dir,
                vb_comp_name + ".bas",
            )

            _logger.info(
                '  writing "%s"',
                vb_comp_file_path,
            )

            with open(
                vb_comp_file_path,
                "w",
                encoding="utf-8",
            ) as f:

                f.write(vb_comp.CodeModule.Lines(1, vb_comp_count))
