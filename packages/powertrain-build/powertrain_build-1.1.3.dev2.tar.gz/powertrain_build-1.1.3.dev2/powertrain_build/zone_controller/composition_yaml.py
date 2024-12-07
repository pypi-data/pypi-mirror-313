# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module for handling ZoneController composition yaml generation."""

import re
from pathlib import Path
from ruamel.yaml import YAML

from powertrain_build.problem_logger import ProblemLogger
from powertrain_build.types import a2l_range
from powertrain_build.zone_controller.calibration import ZoneControllerCalibration as ZCC


class CompositionYaml(ProblemLogger):
    """Class for handling ZoneController composition yaml generation."""

    def __init__(self, build_cfg, composition_spec, unit_cfg, zc_core, zc_dids, zc_nvm, a2l_axis_data, enums):
        """Init.

        Args:
            build_cfg (BuildProjConfig): Object with build configuration settings.
            composition_spec (dict): Dict with port interface information.
            unit_cfg (UnitConfig): Object with unit configurations.
            zc_core (ZCCore): Object with zone controller diagnositic event information.
            zc_dids (ZCDIDs): Object with zone controller diagnostic DID information.
            zc_nvm (ZCNVMDef): Object with NVM definition information.
            a2l_axis_data (dict): Dict with characteristic axis data from A2L file.
        """
        self.tl_to_autosar_base_types = {
            "Bool": "boolean",
            "Float32": "float32",
            "Int16": "sint16",
            "Int32": "sint32",
            "Int8": "sint8",
            "UInt16": "uint16",
            "UInt32": "uint32",
            "UInt8": "uint8",
        }
        self.build_cfg = build_cfg
        self.unit_src_dirs = build_cfg.get_unit_src_dirs()
        self.composition_spec = composition_spec
        self.unit_cfg = unit_cfg
        self.zc_core = zc_core
        self.zc_dids = zc_dids
        self.zc_nvm = zc_nvm
        self.enums = enums
        self.a2l_axis_data = a2l_axis_data
        base_data_types = self.get_base_data_types()  # Might not be necessary in the long run
        self.data_types = {
            **base_data_types,
            **self.composition_spec.get("data_types", {}),
        }
        self.port_interfaces = self.composition_spec.get("port_interfaces", {})
        calibration_variables, measurable_variables = self._get_variables()
        self.calibration_init_values = self.get_init_values(calibration_variables)
        self.cal_class_info = self._get_class_info(calibration_variables)
        self.meas_class_info = self._get_class_info(measurable_variables)
        if self.build_cfg.get_code_generation_config(item="generateCalibrationInterfaceFiles"):
            trigger_read_rte_cdata_signal_name = self._get_calibration_trigger_signal_name(calibration_variables)
            self.cal_class_info["autosar"]["class_info"].update(
                {
                    trigger_read_rte_cdata_signal_name: {
                        "type": ZCC.trigger_read_rte_cdata_signal["data_type"],
                        "access": "READ-WRITE",
                        "init": 0,
                    }
                }
            )

    @staticmethod
    def _cast_init_value(value_str):
        """Cast initialization value to correct type.

        Args:
            value_str (str): String representation of the value.
        Returns:
            (int/float): Value casted to correct type.
        """
        if value_str.endswith("F"):
            return float(value_str[:-1])
        return int(value_str)

    def get_base_data_types(self):
        """Create base data types in expected Autosar/yaml2arxml format."""
        base_data_types = {
            "Bool": {"type": "ENUMERATION", "enums": {"False": 0, "True": 1}},
            "Float32": {
                "type": "FLOAT",
                "limits": {"lower": -3.4e38, "upper": 3.4e38},
            },
        }
        int_data_types = [data_type for data_type in self.tl_to_autosar_base_types if "Int" in data_type]
        for data_type in int_data_types:
            lower, upper = a2l_range(data_type)
            base_data_types[data_type] = {
                "type": "INTEGER",
                "limits": {"lower": lower, "upper": upper},
            }
        return base_data_types

    def check_unsupported_fields(self, signal_name, signal_data):
        """Warn about signal data containing unsupported field values.

        Unsupported fields will not be propagated to the ARXML.
        If any signal contains non-default data, PyBuild should fail.

        Args:
            signal_name (string): Name of signal to process.
            signal_data (dict): signal data.
        """
        unsupported_fields = {"lsb": 1, "offset": 0}
        for field, default_value in unsupported_fields.items():
            if signal_data[field] != "-" and signal_data[field] != default_value:
                self.warning(
                    "Unsupported configuration: %s -> %s, for signal %s.",
                    field,
                    signal_data[field],
                    signal_name,
                )

    def generate_yaml(self):
        """Generates a yaml from project/model information."""
        composition_name = self.build_cfg.get_composition_config("compositionName")
        composition_ending = self.build_cfg.get_composition_config("compositionEnding")
        all_info = self.gather_yaml_info()

        output_directory = self.build_cfg.get_src_code_dst_dir()
        self.info(
            "Writing Yaml into %s/%s.%s",
            output_directory,
            composition_name,
            composition_ending,
        )
        Path(output_directory).mkdir(parents=True, exist_ok=True)

        with open(
            f"{output_directory}/{composition_name}.{composition_ending}",
            "w",
            encoding="utf-8",
        ) as file:
            yaml = YAML()

            def modify_float_representation(s):
                return re.sub(r"(\s-?\d+)e(?=\+|-\d)", r"\1.e", s)

            yaml.dump(all_info, file, transform=modify_float_representation)

    def gather_yaml_info(self):
        """Creates dict with relevant project/model information.

        Returns:
            all_info (dict): Dict to be written to yaml.
        """
        software_components, pt_build_data_types = self._get_software_components()

        all_info = {
            "ExternalFiles": {
                "Composition": self.build_cfg.get_composition_config("compositionArxml"),
                "GenerateExternalImplementationTypes": self.build_cfg.get_composition_config(
                    "generateExternalImplementationType"
                ),
            },
            "SoftwareComponents": software_components,
            "DataTypes": {**self.data_types, **pt_build_data_types},
            "PortInterfaces": self.port_interfaces,
        }

        return all_info

    def get_init_values(self, calibration_variables):
        """Get initialization values for calibration variables.

        Args:
            calibration_variables (dict): Dict of existing calibration variables.
        Returns:
            init_values (dict): Dictionary with initialization values for calibration variables.
        """
        value_extraction_regexes = [
            (
                re.compile(r"^\s*CVC_CAL[A-Z_]*\s+\w+\s+(?P<name>\w+)\s*=\s*(?P<value>[-\d\.e]+F?)\s*;"),
                lambda regex_match, _: self._cast_init_value(regex_match.group("value")),
            ),
            (
                re.compile(r"^\s*CVC_CAL[A-Z_]*\s+\w+\s+(?P<name>\w+)\[(?P<size>[\d]+)\]\s*=\s*"),
                self._get_array_init_values,
            ),
            (
                re.compile(r"^\s*CVC_CAL[A-Z_]*\s+\w+\s+(?P<name>\w+)\[(?P<rows>[\d]+)\]\[(?P<cols>[\d]+)\]\s*=\s*"),
                self._get_matrix_init_values,
            ),
            (
                re.compile(r"^\s*CVC_CAL[A-Z_]*\s+\w+\s+(?P<name>\w+)\s*=\s*(?P<enum>[a-zA-Z_$][\w_]*?)*;"),
                lambda regex_match, _: regex_match.group("enum"),
            ),
        ]

        init_values = {}
        calibration_definitions = self._get_all_calibration_definitions()
        calibration_definitions.reverse()  # Reverse to pop from the end for performance
        while calibration_definitions:
            line = calibration_definitions.pop()
            for regex, extraction_function in value_extraction_regexes:
                regex_match = regex.match(line)
                if regex_match is not None and regex_match.group("name") in calibration_variables:
                    if regex_match.group("name") in init_values:
                        self.critical("Variable definition for %s already found.", regex_match.group("name"))
                    init_values[regex_match.group("name")] = extraction_function(regex_match, calibration_definitions)

        missing_init_values = set(calibration_variables) - set(init_values.keys())
        if missing_init_values:
            self.critical("Missing init values for calibration variables:\n%s", "\n".join(missing_init_values))

        return init_values

    def _get_all_calibration_definitions(self):
        """Get all calibration definitions from the source files.

        Returns:
            (iter): Iterator with calibration definitions.
        """
        calibration_definitions = []
        end_of_definitions_regex = re.compile(r"^void\s*RESTART_.*")
        c_files = [Path(src_dir, unit.split("__")[0] + ".c").resolve() for unit, src_dir in self.unit_src_dirs.items()]
        for c_file in c_files:
            read_lines = ""
            with c_file.open(mode="r", encoding="latin-1") as file_handle:
                for line in file_handle:
                    if end_of_definitions_regex.match(line):
                        break
                    read_lines += line
            calibration_definitions.extend(re.sub(r"/\*.*?\*/", "", read_lines, flags=re.S).splitlines())
        return calibration_definitions

    def _get_array_init_values(self, array_regex_match, definitions_list):
        """Get initialization values for an array.

        NOTES:
        Modifies the argument definitions_list by popping elements.
        Popping from the end since list is reversed.

        Args:
            array_regex_match (re.Match): Match object with array definition.
            definitions_list (list): List (reversed) with lines to parse.
        Returns:
            (list): List of initialization values for the array.
        """
        array_init_values_str = ""
        line = definitions_list.pop()  # Skip array definition line
        while "};" not in line:
            array_init_values_str += line.strip()
            line = definitions_list.pop()
        array_init_values_str += line.strip()
        array_init_values = re.findall(r"([-\d\.e]+F?),?", array_init_values_str)

        if int(array_regex_match.group("size")) != len(array_init_values):
            self.critical("Could not parse init values for array definition %s.", array_regex_match.group("name"))

        return [self._cast_init_value(value) for value in array_init_values]

    def _get_matrix_init_values(self, matrix_regex_match, definitions_list):
        """Get initialization values for a matrix.

        NOTES:
        Modifies the argument definitions_list by popping elements.
        Popping from the end since list is reversed.

        Args:
            matrix_regex_match (re.Match): Match object with matrix definition.
            definitions_list (list): List (reversed) with lines to parse.
        Returns:
            (list(list)): List of initialization values for the matrix.
        """
        matrix_init_values = []
        matrix_init_values_str = ""
        line = definitions_list.pop()  # Skip matrix definition line
        while "};" not in line:
            matrix_init_values_str += line.strip()
            if "}" in line:
                matrix_init_values.append(re.findall(r"([-\d\.e]+F?),?", matrix_init_values_str))
                matrix_init_values_str = ""
            line = definitions_list.pop()

        row_check = int(matrix_regex_match.group("rows")) != len(matrix_init_values)
        col_check = any(int(matrix_regex_match.group("cols")) != len(row) for row in matrix_init_values)
        if row_check or col_check:
            self.critical("Could not parse init values for matrix definition %s.", matrix_regex_match.group("name"))

        return [[self._cast_init_value(value) for value in row] for row in matrix_init_values]

    def _get_calibration_trigger_signal_name(self, calibration_variables):
        """Get the variable of the calibration trigger.

        Make sure it is not present already.

        Args:
            calibration_variables (dict): Dict of existing calibration variables.
        Returns:
            trigger_signal (str): Name of variable for triggering calibration.
        """
        software_component_name = self.build_cfg.get_composition_config("softwareComponentName")
        trigger_signal = ZCC.trigger_read_rte_cdata_signal["name_template"].format(swc_name=software_component_name)

        if trigger_signal in calibration_variables:
            self.critical("Signal %s already defined in project.", trigger_signal)

        return trigger_signal

    def _get_diagnostic_info(self):
        """Get diagnostic information from composition spec.

        NOTE: This function sets the valid_dids property of the ZCDIDs object.

        Returns:
            diag_dict (dict): Dict containing diagnostic information.
        """
        diag_dict = {}
        diagnostics = self.composition_spec.get("diagnostics", {})
        dids = diagnostics.get("dids", {})
        self.zc_dids.valid_dids = dids
        events = diagnostics.get("events", {})
        rids = diagnostics.get("rids", {})
        if dids:
            diag_dict["dids"] = self.zc_dids.valid_dids
        if events:
            diag_dict["events"] = self.zc_core.get_diagnostic_trouble_codes(events)
        if rids:
            diag_dict["rids"] = rids
            self.warning("Will not generate code for RIDs, add manually.")
        return diag_dict

    def _get_nvm_info(self):
        """Creates a dict with NVM information.

        NVM dicts also needs to be added to the "static" field in the generated yaml.

        NOTE: This function sets the valid_nvm_definitions property of the ZCNVMDef object.

        Returns:
            nvm_dict (dict): Dict containing NVM information.
            data_types (dict): Dict containing data types for NVM information.
            static_variables (dict): Dict containing "static" variables to add to the "static" field.
        """
        data_types = {}
        static_variables = {}
        yaml_nvm_definitions = self.composition_spec.get("nv-needs", {})
        self.zc_nvm.valid_nvm_definitions = yaml_nvm_definitions
        nvm_dict = self.zc_nvm.valid_nvm_definitions

        for nvm_name, nvm_data in nvm_dict.items():
            init = []
            nr_of_unused_signals = self.zc_nvm.project_nvm_definitions[nvm_name]["size"]
            data_type_name = f"dt_{nvm_name}"
            data_types[data_type_name] = {"type": "RECORD", "elements": {}}
            for signal in self.zc_nvm.project_nvm_definitions[nvm_name]["signals"]:
                nr_of_unused_signals -= signal["x_size"] * signal["y_size"]
                size = max(signal["x_size"], 1) * max(signal["y_size"], 1)
                if size > 1:
                    x_data_type_name = f"dt_{signal['name']}_x"
                    y_data_type_name = f"dt_{signal['name']}_y"
                    if signal["x_size"] > 1 and signal["y_size"] == 1:
                        init.append([0] * signal["x_size"])
                        data_types[data_type_name]["elements"][signal["name"]] = x_data_type_name
                        data_types[x_data_type_name] = {
                            "type": "ARRAY",
                            "size": signal["x_size"],
                            "element": signal["type"],
                        }
                    elif signal["x_size"] > 1 and signal["y_size"] > 1:
                        init.append([[0] * signal["y_size"]] * signal["x_size"])
                        data_types[data_type_name]["elements"][signal["name"]] = y_data_type_name
                        data_types[y_data_type_name] = {
                            "type": "ARRAY",
                            "size": signal["y_size"],
                            "element": x_data_type_name,
                        }
                        data_types[x_data_type_name] = {
                            "type": "ARRAY",
                            "size": signal["x_size"],
                            "element": signal["type"],
                        }
                    else:
                        self.critical("NVM signal size incorrect. x_size should not be 1 if y_size > 1.")
                else:
                    init.append(0)
                    data_types[data_type_name]["elements"][signal["name"]] = signal["type"]

            nvm_data.update({
                "datatype": data_type_name,
                "init": init
            })
            static_variables[nvm_name.lower()] = {
                "type": data_type_name,
                "access": "READ-ONLY",
                "init": init,
            }

            if nr_of_unused_signals > 0:
                nvm_data["init"].append([0] * nr_of_unused_signals)
                data_types[data_type_name]["elements"]["unused"] = f"{data_type_name}_Unused"
                data_types[f"{data_type_name}_Unused"] = {
                    "type": "ARRAY",
                    "size": nr_of_unused_signals,
                    "element": self.zc_nvm.project_nvm_definitions[nvm_name]["default_datatype"],
                }

        return nvm_dict, data_types, static_variables

    def _get_ports_info(self):
        """Creates a dict containing port information.

        Returns:
            ports (dict): Dict containing port information.
        """
        ports = self.composition_spec.get("ports", {})
        for call, call_data in self.composition_spec.get("calls", {}).items():
            if call in ports:
                continue
            ports[call] = {
                "interface": call_data.get("interface", call),
                "direction": call_data["direction"],
            }
        return ports

    def _get_runnable_calls_info(self):
        """Creates a dict containing desired calls for the SWC.

        Returns:
            call_dict(dict): Dict containing runnable calls information.
        """
        call_dict = {}
        for call, call_data in self.composition_spec.get("calls", {}).items():
            call_dict[call] = {"operation": call_data["operation"]}
            if "timeout" in call_data:
                call_dict[call]["timeout"] = call_data["timeout"]
        return call_dict

    def _get_runnable_info(self):
        """Creates a dict containing runnables information.

        Returns:
            dict: Dict containing runnables information.
        """
        swc_name = self.build_cfg.get_composition_config("softwareComponentName")
        autosar_prefix = "AR_"
        swc_prefix = self.build_cfg.get_scheduler_prefix()
        custom_step_function = self.build_cfg.get_composition_config("customYamlStepFunctionName")
        custom_init_function = self.build_cfg.get_composition_config("customYamlInitFunctionName")
        standard_init_function = autosar_prefix + swc_prefix + "VcExtINI"
        init_function = custom_init_function if custom_init_function is not None else standard_init_function
        call_dict = self._get_runnable_calls_info()
        runnables = self.build_cfg.get_units_raster_cfg()["SampleTimes"]
        calibration_variables = list(self.cal_class_info["autosar"]["class_info"].keys())
        swc_content = {init_function: {"type": "INIT", "accesses": calibration_variables}}

        if self.build_cfg.get_code_generation_config(item="generateCalibrationInterfaceFiles"):
            cal_step_function = autosar_prefix + ZCC.calibration_function_step_template.format(swc_name=swc_name)
            swc_content[cal_step_function] = {
                "type": "PERIODIC",
                "period": 0.1,
                "accesses": calibration_variables,
            }

        if len(runnables) == 1 and custom_step_function is not None:
            swc_content[custom_step_function] = {
                "type": "PERIODIC",
                "period": list(runnables.values())[0],
                "accesses": calibration_variables,
            }
            if call_dict:
                swc_content[custom_step_function]["calls"] = call_dict
            return swc_content

        if custom_step_function is not None:
            self.warning(
                "Custom step function specified, but multiple runnables defined. Ignoring custom step function."
            )

        for runnable, period in runnables.items():
            key = autosar_prefix + swc_prefix + runnable
            swc_content[key] = {
                "period": period,
                "type": "PERIODIC",
                "accesses": calibration_variables,
            }
            if call_dict:
                swc_content[key]["calls"] = call_dict

        return swc_content

    def _get_software_components(self):
        """Creates a dict with swc information and referred data types.

        Returns:
            swcs (dict): SWC information.
            data_types (dict): Data types information.
        """
        software_component_name = self.build_cfg.get_composition_config("softwareComponentName")
        software_component_template = self.build_cfg.get_composition_config("softwareComponentTemplate")
        software_component_base = self.build_cfg.get_composition_config("softwareComponentBase")

        swcs = {software_component_name: {}}
        swcs[software_component_name]["type"] = "SWC"  # Other types than swc??
        if software_component_template is not None:
            swcs[software_component_name]["template"] = software_component_template
        if software_component_base is not None:
            swcs[software_component_name]["swcbase"] = software_component_base
        swcs[software_component_name]["runnables"] = self._get_runnable_info()
        if self.build_cfg.get_composition_config("includeShared"):
            swcs[software_component_name]["shared"] = self.cal_class_info["autosar"]["class_info"]
        if self.build_cfg.get_composition_config("includeStatic"):
            swcs[software_component_name]["static"] = self.meas_class_info["autosar"]["class_info"]
        swcs[software_component_name]["ports"] = self._get_ports_info()
        diagnostic_info = self._get_diagnostic_info()
        if self.build_cfg.get_composition_config("includeDiagnostics"):
            swcs[software_component_name]["diagnostics"] = diagnostic_info
        nvm_info, nvm_data_types_tmp, static_variables = self._get_nvm_info()
        if self.build_cfg.get_composition_config("includeNvm"):
            swcs[software_component_name]["nv-needs"] = nvm_info
            nvm_data_types = nvm_data_types_tmp
            if self.build_cfg.get_composition_config("includeStatic"):
                swcs[software_component_name]["static"].update(static_variables)
        else:
            nvm_data_types = {}

        data_types = {
            **self.cal_class_info["autosar"]["data_types"],
            **self.meas_class_info["autosar"]["data_types"],
            **nvm_data_types,
        }

        return swcs, data_types

    def _get_variables(self):
        """Get calibration and measurable variables from the unit configuration.

        Returns:
            calibration_variables (dict): Dict with calibration variables.
            measurable_variables (dict): Dict with measurable variables.
        """
        calibration_variables = {}
        measurable_variables = {}
        config = self.unit_cfg.get_per_cfg_unit_cfg()
        valid_configs = ["outports", "local_vars", "calib_consts"]
        for valid_config in valid_configs:
            for signal_name, unit_info in config.get(valid_config, {}).items():
                if len(unit_info) > 1:
                    self.critical("Multiple definitions for %s in config json files.", signal_name)
                for info in unit_info.values():
                    if "CVC_CAL" in info["class"]:
                        calibration_variables[signal_name] = info
                    elif "CVC_DISP" in info["class"]:
                        measurable_variables[signal_name] = info
                    else:
                        self.critical("Signal %s has no class defined.", signal_name)
                        continue
                    self.check_unsupported_fields(signal_name, info)
        return calibration_variables, measurable_variables

    def _get_class_info(self, variable_dict):
        """Creates a dict with parameter information and referred data types.

        Args:
            variable_dict (dict): Dictionary with variables and data.
        Returns:
            (dict): Dictionary with variables and data types (Autosar and TL).
        """
        autosar_class_info = {}
        autosar_data_types = {}
        tl_class_info = {}
        for signal_name, info in variable_dict.items():
            (
                autosar_class_info,
                autosar_data_types,
            ) = self._add_autosar_data_types(autosar_class_info, autosar_data_types, signal_name, info)
            if signal_name in autosar_class_info:
                tl_class_info[signal_name] = {
                    "type": info["type"],
                    "autosar_type": autosar_class_info[signal_name]["type"].split("/")[-1],
                    "width": info["width"],
                }
        return {
            "autosar": {
                "class_info": autosar_class_info,
                "data_types": autosar_data_types,
            },
            "tl": {"class_info": tl_class_info, "data_types": {}},
        }

    def _add_autosar_data_types(self, class_info, data_types, signal_name, info):
        """Process a variable for inclusion in composition, adding it's data type to
        data_types and the variable to class_info.

        Args:
            class_info (dict): Dictionary with variables.
            data_types (dict): Dictionary with data types.
            signal_name (string): Name of signal to process.
            info (dict): signal data.
        Returns::wq

            class_info (dict): Updated dictionary with variables.
            data_types (dict): Updated dictionary with data types.
        """
        if info["type"] in self.enums:
            return class_info, data_types
        if "Bool" in info["type"]:
            upper = 1
            lower = 0
        else:
            base_type_lower = self.data_types[info["type"]]["limits"]["lower"]
            base_type_upper = self.data_types[info["type"]]["limits"]["upper"]
            lower = info["min"] if info["min"] != "-" else base_type_lower
            upper = info["max"] if info["max"] != "-" else base_type_upper
        if not isinstance(info["width"], list):
            class_info[signal_name] = {
                "type": info["type"],
                "access": "READ-ONLY" if "CVC_DISP" in info["class"] else "READ-WRITE",
                "init": self.calibration_init_values.get(signal_name, max(min(0, upper), lower)),
            }
            return class_info, data_types

        if isinstance(lower, list) or isinstance(upper, list):
            if info["width"][0] > 1:
                self.critical(
                    "%s is a multidimentional array of elements with different constraints, not supported.", signal_name
                )
            init = []
            for idx in range(info["width"][1]):
                lower_val = lower[idx] if isinstance(lower, list) else lower
                lower_val = lower_val if lower_val != "-" else base_type_lower
                upper_val = upper[idx] if isinstance(upper, list) else upper
                upper_val = upper_val if upper_val != "-" else base_type_upper
                init.append(max(min(0, upper_val), lower_val))
        else:
            init = max(min(0, upper), lower)
            if info["width"][0] > 1:
                init = [[init] * info["width"][1] for _ in range(info["width"][0])]
            else:
                init = [init] * info["width"][1]

        init = self.calibration_init_values.get(signal_name, init)

        new_data_type = {}
        new_data_type_name = f"dt_{signal_name}"
        if signal_name.startswith("t"):
            if signal_name.endswith("_x"):
                new_data_type_data = {
                    "type": "COM_AXIS",
                    "axis-index": 1,
                    "size": info["width"][1],
                    "limits": {"lower": lower, "upper": upper},
                    "swrecordlayout": {
                        "name": f"Distr_{signal_name}",
                        "type": "INDEX_INCR",
                        "basetype": self.tl_to_autosar_base_types[info["type"]],
                        "label": "X",
                    },
                }
            else:
                axis = self.a2l_axis_data.get(signal_name, {}).get("axes", [signal_name + "_x"])[0]
                new_data_type_data = {
                    "type": "CURVE",
                    "axis": f"dt_{axis}",
                    "limits": {"lower": lower, "upper": upper},
                    "swrecordlayout": {
                        "name": f"Curve_{signal_name}",
                        "type": "COLUMN_DIR",
                        "basetype": self.tl_to_autosar_base_types[info["type"]],
                        "label": "Val",
                    },
                }
        elif signal_name.startswith("m"):
            new_data_type_data = {
                "type": "COM_AXIS",
                "size": info["width"][1],
                "limits": {"lower": lower, "upper": upper},
                "swrecordlayout": {
                    "name": f"Distr_{signal_name}",
                    "type": "INDEX_INCR",
                    "basetype": self.tl_to_autosar_base_types[info["type"]],
                },
            }
            if signal_name.endswith("_r"):
                new_data_type_data["axis-index"] = 1
                new_data_type_data["swrecordlayout"]["label"] = "X"
            elif signal_name.endswith("_c"):
                new_data_type_data["axis-index"] = 2
                new_data_type_data["swrecordlayout"]["label"] = "Y"
            else:
                default_names = [signal_name + "_r", signal_name + "_c"]
                axis_r, axis_c = self.a2l_axis_data.get(signal_name, {}).get("axes", default_names)
                new_data_type_data = {
                    "type": "MAP",
                    "x-axis": f"dt_{axis_r}",
                    "y-axis": f"dt_{axis_c}",
                    "limits": {"lower": lower, "upper": upper},
                    "swrecordlayout": {
                        "name": f"Map_{signal_name}",
                        "type": "COLUMN_DIR",
                        "basetype": self.tl_to_autosar_base_types[info["type"]],
                        "label": "Val",
                    },
                }
        elif info["width"][0] == 1:
            new_data_type_name = f"dt_{signal_name}_{info['width'][1]}"
            new_data_type_data = {
                "type": "ARRAY",
                "size": info["width"][1],
                "element": info["type"],
            }
        else:
            self.critical("Signal config error for %s.", signal_name)
            return class_info, data_types

        new_data_type[new_data_type_name] = new_data_type_data
        class_info[signal_name] = {
            "type": new_data_type_name,
            "access": "READ-ONLY" if "CVC_DISP" in info["class"] else "READ-WRITE",
            "init": init,
        }
        data_types = {**data_types, **new_data_type}
        return class_info, data_types
