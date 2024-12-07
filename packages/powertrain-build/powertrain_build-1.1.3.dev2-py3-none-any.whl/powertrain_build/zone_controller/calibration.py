# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module for handling ZoneController calibration."""

from pathlib import Path
from powertrain_build.problem_logger import ProblemLogger


class ZoneControllerCalibration(ProblemLogger):
    """Class for handling ZoneController calibration."""

    calibration_function_step_template = '{swc_name}_ZcCalibrationStep'
    trigger_read_rte_cdata_signal = {
        'name_template': 'c{swc_name}_TriggerReadRteCData',
        'data_type': 'Float32'
    }

    def __init__(self, build_cfg, calib_data):
        """Init.

        Args:
            build_cfg (BuildProjConfig): Object with build configuration settings.
            calib_data (dict): Dictionary containing calibration data for a ZoneController project.
        """
        self.swc_name = build_cfg.get_composition_config("softwareComponentName")
        self.src_code_dst_dir = build_cfg.get_src_code_dst_dir()
        self.calibration_variables = calib_data['class_info']
        self.calibration_interface_header = 'calibration_interface.h'
        self.calibration_interface_source = 'calibration_interface.c'
        self.trigger_read_rte_cdata_signal_name = self.trigger_read_rte_cdata_signal['name_template'].format(
            swc_name=self.swc_name
        )
        if self.trigger_read_rte_cdata_signal_name in self.calibration_variables:
            self.critical(f'Signal {self.trigger_read_rte_cdata_signal_name} already defined in project.')
        self.calibration_variables.update({
            self.trigger_read_rte_cdata_signal_name: {
                "type": self.trigger_read_rte_cdata_signal['data_type'],
                "width": 1,
            }
        })

    def _get_header_guard(self):
        header_guard_tmp = Path(self.calibration_interface_header).stem
        return header_guard_tmp.upper() + '_H'

    def get_header_file_content(self):
        """Get content for the calibration header file.

        Returns:
            (list(str)): List of lines to write to calibration header file.
        """
        lines_to_write = []
        header = [
            f'#ifndef {self._get_header_guard()}\n',
            f'#define {self._get_header_guard()}\n',
            '#define CVC_CAL\n',
            '#include <string.h>\n',
            '#include "tl_basetypes.h"\n',
            f'#include "Rte_{self.swc_name}.h"\n',
            '\n'
        ]
        footer = [
            '\n',
            f'#endif /* {self._get_header_guard()} */\n'
        ]

        lines_to_write.extend([
            f'#define {self.swc_name}_START_SEC_VCC_CAL\n',
            f'#include "{self.swc_name}_MemMap.h"\n'
        ])
        for signal_name, signal_data in self.calibration_variables.items():
            if isinstance(signal_data["width"], list):
                rows, cols = signal_data["width"]
                if rows > 1:
                    declaration = f'extern CVC_CAL {signal_data["type"]} {signal_name}[{rows}][{cols}];\n'
                else:
                    declaration = f'extern CVC_CAL {signal_data["type"]} {signal_name}[{cols}];\n'
            else:
                declaration = f'extern CVC_CAL {signal_data["type"]} {signal_name};\n'
            lines_to_write.append(declaration)
        lines_to_write.extend([
            f'#define {self.swc_name}_STOP_SEC_VCC_CAL\n',
            f'#include "{self.swc_name}_MemMap.h"\n'
        ])

        lines_to_write.append('\n')
        for signal_name, signal_data in self.calibration_variables.items():
            if isinstance(signal_data["width"], list):
                # MAPs get typedef:ed to structs and need special data type mapping in calibration.py
                if signal_name.startswith("m") and signal_name[-2:] not in ["_r", "_c"]:
                    return_type = f'const {signal_data["autosar_type"]}*'
                else:
                    return_type = f'const {signal_data["type"]}*'
            else:
                return_type = f'{signal_data["type"]}'
            lines_to_write.append(f'extern {return_type} Rte_CData_{self.swc_name}_{signal_name}(void);\n')

        lines_to_write.extend([
            '\n',
            f'void {self.calibration_function_step_template.format(swc_name=self.swc_name)}(void);\n'
        ])

        return header + lines_to_write + footer

    def get_source_file_content(self):
        """Get content for the calibration source file.

        Returns:
            (list(str)): List of lines to write to calibration source file.
        """
        trigger_read_calibration_function = f'Rte_CData_{self.swc_name}_{self.trigger_read_rte_cdata_signal_name}()'

        header = [
            f'#include "{self.calibration_interface_header}"\n',
            '\n',
            f'#define {self.swc_name}_START_SEC_VCC_CAL\n',
            f'#include "{self.swc_name}_MemMap.h"\n',
            f'CVC_CAL {self.trigger_read_rte_cdata_signal["data_type"]} '
            f'{self.trigger_read_rte_cdata_signal_name} = 0;\n',
            f'#define {self.swc_name}_STOP_SEC_VCC_CAL\n',
            f'#include "{self.swc_name}_MemMap.h"\n',
            '\n',
            f'#define {self.swc_name}_START_SEC_CODE\n',
            f'#include "{self.swc_name}_MemMap.h"\n',
            f'void {self.calibration_function_step_template.format(swc_name=self.swc_name)}(void)\n{{\n'
        ]

        body = [f'    if ({self.trigger_read_rte_cdata_signal_name} != {trigger_read_calibration_function})\n']
        body.append('    {\n')
        for signal_name, signal_data in self.calibration_variables.items():
            if isinstance(signal_data["width"], list):
                rte_call = f'Rte_CData_{self.swc_name}_{signal_name}()'
                body.append(f'        memcpy({signal_name}, {rte_call}, sizeof({signal_name}));\n')
            else:
                body.append(f'        {signal_name} = Rte_CData_{self.swc_name}_{signal_name}();\n')
        body.append('    }\n')

        footer = [
            '}\n',
            f'#define {self.swc_name}_STOP_SEC_CODE\n',
            f'#include "{self.swc_name}_MemMap.h"\n'
        ]

        return header + body + footer

    def generate_calibration_interface_files(self):
        """Generate calibration interface files."""
        header_file_content = self.get_header_file_content()
        calibration_interface_header_path = Path(self.src_code_dst_dir, self.calibration_interface_header)
        with calibration_interface_header_path.open(mode='w', encoding='utf-8') as file_handler:
            file_handler.writelines(header_file_content)

        source_file_content = self.get_source_file_content()
        calibration_interface_source_path = Path(self.src_code_dst_dir, self.calibration_interface_source)
        with calibration_interface_source_path.open(mode='w', encoding='utf-8') as file_handler:
            file_handler.writelines(source_file_content)
