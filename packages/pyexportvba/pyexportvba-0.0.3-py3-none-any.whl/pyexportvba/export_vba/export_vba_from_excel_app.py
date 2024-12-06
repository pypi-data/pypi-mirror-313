import logging
import os

import win32com.client

from .get_vb_comp_code import get_vb_comp_code
from .get_vb_comp_paths import get_vb_comp_paths

_logger = logging.getLogger(__name__)


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

            (
                vb_comp_dir,
                vb_comp_file_path,
            ) = get_vb_comp_paths(
                vb_project_dir,
                vb_comp,
            )

            code_str = get_vb_comp_code(vb_comp)

            if code_str is None:
                _logger.warning(
                    '  ignoring empty "%s"',
                    vb_comp_file_path,
                )

                continue

            _logger.info(
                '  exporting "%s"',
                vb_comp_file_path,
            )

            os.makedirs(vb_comp_dir, exist_ok=True)

            with open(
                vb_comp_file_path,
                "w",
                encoding="utf-8",
            ) as f:
                f.write(code_str)
