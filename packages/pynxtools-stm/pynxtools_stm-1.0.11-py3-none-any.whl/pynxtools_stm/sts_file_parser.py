#!/usr/bin/env python3
"""
To collect data from Bias Spectroscopy output file that is mainly a
file with dat extension.
"""
# -*- coding: utf-8 -*-
#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
import os
from typing import Dict, Optional, Tuple, Union

import numpy as np

from pynxtools_stm.helper import (
    UNIT_TO_SKIP,
    fill_template_from_eln_data,
    link_seperation_from_hard_code,
    nested_path_to_slash_separated_path,
    to_intended_t,
    work_out_overwriteable_field,
    convert_data_dict_path_to_hdf5_path,
)
from pynxtools_stm.analyticalplot import dY_by_dX as dI_by_dV

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


# Type aliases
NestedDict = Dict[str, Union[int, str, float, "NestedDict"]]


# pylint: disable=invalid-name
class BiasSpecData_Nanonis:
    """This class collect and store data fo Bias spectroscopy of SPM experiment.

    The class splits the data and store in into nested python dictionary as follows.
       E.g.
        bais_data = {data_field_name:{value: value_for_data_field_of_any_data_typeS,
                                      unit: unit name,
                                      date: ---,
                                      time: ---}
                    }
    """

    def __init__(self, file_name: str) -> None:
        """Innitialize object level variables."""
        # Note: If get some information about machines or vendors which makes
        # the data file distinguished collecte them.
        self.bias_spect_dict: NestedDict = {}
        self.raw_file: str = file_name
        self.nanonis_version = ""
        self.choose_correct_function_to_extract_data()

    def get_data_nested_dict(self) -> NestedDict:
        """Retrun nested dict as bellow

        bais_data = {data_field_name:{value: value_for_data_field_of_any_data_typeS,
                                      unit: unit name,
                                      date: ---,
                                      time: ---}
                    }
        """
        return self.bias_spect_dict

    # pylint: disable=too-many-arguments
    def check_and_write_unit(
        self, dct, key_or_line, unit_separators, end_of_seperators, value=None
    ):
        """Check and write unit.

        Parameters
        ----------
        dct : dict

        key_or_line : _type_
            The dict that tracks full nested paths and unit at deepest nest.
        unit_separators : list
            List of separator chars
        end_of_seperators : list
            List of end separator chars
        value : dict, optional
            dict to store dict
        """
        for sep_unit, end_sep in zip(unit_separators, end_of_seperators):
            if sep_unit in key_or_line:
                key, unit = key_or_line.split(sep_unit, 1)
                unit = unit.split(end_sep)[0]
                if key_or_line in dct:
                    del dct[key_or_line]
                # skiping some unit that are not part of standard e.g. on/off
                if unit in UNIT_TO_SKIP:
                    unit = ""
                if isinstance(value, dict):
                    value["unit"] = unit
                else:
                    value: NestedDict = {}
                    value["unit"] = unit
                dct[key] = value
                break

    def retrive_key_recursively(
        self, line_to_analyse: str, dict_to_store: NestedDict, key_seperators: list
    ) -> None:
        """Store metadata path in recursive manner because the path is separated by chars.

        Parameters
        ----------
        line_to_analyse : str
            Line with metadata path where each part of path is separated by chars from
            key_separated chars.
        dict_to_store : NestedDict
            Dict to store metadata path part in nested form
        key_separators : list
            List of chars separating metadata path.
        """
        unit_separators = [" ("]
        end_of_seperators = [")"]

        line_to_analyse = line_to_analyse.strip()
        for k_sep in key_seperators:
            new_dict: NestedDict = {}
            if k_sep in line_to_analyse:
                key, rest = line_to_analyse.split(k_sep, 1)
                key = key.strip()
                if key in dict_to_store:
                    new_dict = dict_to_store[key]  # type: ignore
                else:
                    new_dict = {}
                dict_to_store[key] = new_dict
                # check if key contains any unit inside bracket '()'
                self.check_and_write_unit(
                    dict_to_store, key, unit_separators, end_of_seperators, new_dict
                )
                self.retrive_key_recursively(rest, new_dict, key_seperators)
                return

        for sep_unit in unit_separators:
            if sep_unit in line_to_analyse:
                self.check_and_write_unit(
                    dict_to_store, line_to_analyse, unit_separators, end_of_seperators
                )
                return

        dict_to_store["value"] = line_to_analyse.strip()
        return

    def check_matrix_data_block_has_started(
        self, line_to_analyse: str
    ) -> Tuple[bool, list]:
        """_summary_

        Parameters
        ----------
        line_to_analyse : str
            Line to check whether matrix data has started.

        Returns
        -------
            Bool flag: Flag for matarix data found
            value list: List of row values if the matrix has found.
        """
        wd_list = line_to_analyse.split()
        int_list = []
        if not wd_list:
            return False, []
        for word in wd_list:
            try:
                float_n = float(word)
                int_list.append(float_n)
            except ValueError:
                return False, []
        return True, int_list

    def check_metadata_and_unit(self, key_and_unit: str):
        """Check for metadata and unit.

        Parameters
        ----------
        key_and_unit : str
            String to check key, metadata and unit
        """
        metadata = ""
        key, unit = key_and_unit.split("(")
        unit, rest = unit.split(")", 1)
        # Some units have extra info e.g. Current (A) [filt]
        if "[" in rest:
            metadata = rest.split("[")[-1].split("]")[0]
        if unit in UNIT_TO_SKIP:
            unit = ""
        return key, unit, metadata

    def extract_and_store_from_dat_file(self) -> None:
        """Extract data from data file and store them into object level nested dictionary."""

        key_seperators = [">", "\t"]
        is_matrix_data_found = False
        one_d_numpy_array = np.empty(0)

        def dismentle_matrix_into_dict_key_value_list(
            column_string, one_d_np_array, dict_to_store
        ):
            column_keys = column_string.split("\t")
            np_2d_array = one_d_np_array.reshape(-1, len(column_keys))
            dat_mat_comp = "dat_mat_components"
            dict_to_store[dat_mat_comp] = {}
            for ind, key_and_unit in enumerate(column_keys):
                if "(" in key_and_unit:
                    key, unit, data_stage = self.check_metadata_and_unit(key_and_unit)
                    # data_stage could be 'filt' or something like this
                    if data_stage:
                        dict_to_store[dat_mat_comp][f"{key.strip()} [{data_stage}]"] = {
                            "unit": unit,
                            "value": np_2d_array[:, ind],
                            "metadata": data_stage,
                        }
                    else:
                        dict_to_store[dat_mat_comp][key.strip()] = {
                            "unit": unit,
                            "value": np_2d_array[:, ind],
                        }
                else:
                    dict_to_store[dat_mat_comp][key.strip()] = {
                        "value": list(np_2d_array[:, ind])
                    }

        with open(self.raw_file, mode="r", encoding="utf-8") as file_obj:
            lines = file_obj.readlines()
            # last two lines for getting matrix data block that comes at the end of the file
            last_line: str
            for ind, line in enumerate(lines):
                if ind == 0:
                    last_line = line
                    continue
                is_mat_data, data_list = self.check_matrix_data_block_has_started(line)
                if is_mat_data:
                    is_matrix_data_found = True
                    one_d_numpy_array = np.append(one_d_numpy_array, data_list)
                    is_mat_data = False
                # Map matrix data if file has at least two empty lines or starts
                # other data or metadata except matrix data
                elif (not is_mat_data) and is_matrix_data_found:
                    is_matrix_data_found = False
                    dismentle_matrix_into_dict_key_value_list(
                        last_line, one_d_numpy_array, self.bias_spect_dict
                    )
                    last_line = line
                else:
                    self.retrive_key_recursively(
                        last_line, self.bias_spect_dict, key_seperators
                    )
                    last_line = line

            if (not is_mat_data) and is_matrix_data_found:
                is_matrix_data_found = False
                dismentle_matrix_into_dict_key_value_list(
                    last_line, one_d_numpy_array, self.bias_spect_dict
                )

    def choose_correct_function_to_extract_data(self) -> None:
        """Choose correct function to extract data that data in organised format."""
        if not os.path.isfile(self.raw_file):
            raise ValueError("Provide correct file.")

        ext = self.raw_file.rsplit(".", 1)[-1]
        if ext == "dat":
            self.extract_and_store_from_dat_file()

    def get_flip_number(self, eln_dict):
        """Get the number to flip the data plot from user defined eln."""
        seach_key = (
            "/ENTRY[entry]/INSTRUMENT[instrument]/lock_in/lock_in_data_flip_number"
        )
        flip_num = eln_dict.get(seach_key, None)
        if flip_num is not None:
            return flip_num
        raise ValueError(
            f"To determine the plot fliping {seach_key} must be provided by eln."
        )


def construct_nxdata_for_dIbydV(axis_and_field_data, template, flip_num, acc=4):
    """Construct NXdata for dI/dV.
    axis_and_field_data : dict
        Dictionary that contains axes info (name, data, unit), fields (name, data, unit),
        and extra annotation e.g. filt, filt2.

    Field is a current and axis is a voltage data.
    """

    axis_info = axis_and_field_data["axes"]
    fields_info = axis_and_field_data["fields"]
    extra_annot = axis_and_field_data["extra_annot"]
    a_data = axis_info["data"]
    a_name = axis_info["name"]
    a_unit = axis_info["unit"]
    a_nx_path = axis_info["nx_path"]
    a_metadata = axis_info["metadata"]
    f_data = fields_info["data"]
    f_name = fields_info["name"]
    f_unit = fields_info["unit"]

    if len(a_data) != 1 or len(a_name) != 1 or len(a_unit) != 1:
        raise ValueError("There must be only one Bias axis.")
    if extra_annot:
        extra_annot = f"_{extra_annot}"

    for f_dat, f_mn, f_unt in zip(f_data, f_name, f_unit):
        f_mn = "grad_" + "_".join(f_mn.lower().split(" "))
        grp = f"/ENTRY[entry]/DATA[{f_mn}{extra_annot}]"
        di_by_dv_nm = "di_by_dv"
        f_dat = f_dat * flip_num
        template[grp + "/" + di_by_dv_nm] = dI_by_dV(f_dat, a_data[0], acc=acc)
        dI_by_dV_u = f"{f_unt}/{a_unit[0]}"
        template[grp + "/" + di_by_dv_nm + "/@units"] = dI_by_dV_u
        template[grp + "/@signal"] = di_by_dv_nm
        template[grp + "/" + di_by_dv_nm + "/@long_name"] = (
            f"{di_by_dv_nm}({dI_by_dV_u})"
        )
        template[grp + "/@axes"] = a_name[0]
        template[grp + "/" + a_name[0]] = {"link": a_nx_path[0]}
        template[grp + "/" + a_name[0] + "/@units"] = a_unit[0]
        template[grp + "/" + a_name[0] + "/@long_name"] = f"{a_name[0]}({a_unit[0]})"


# pylint: disable=too-many-locals too-many-statements
def construct_nxdata_for_dat(
    template,
    data_dict,
    sub_config_dict,
    data_group_concept,
    flip_number,
    acc=4,
):
    """
    Construct NXdata that includes counts all the NXdata groups (Bais and current) and
    the analytical NXdata group (dI/dV) vs Bias.

    This function palces all the functions that required to filtter the data field and axes
    to construct NXdata group from raw file.

    Parameters:
    -----------
    template : dict[str, Any]
        Capturing data elements. One to one dictionary for capturing data array, data axes
        and so on from data_dict to be ploted.
    data_dict : dict[str, Union[array, str]]
        Data stored from dat file. Path (str) to data elements which mainly come from
        dat file. Data from this dict will go to template
    sub_config_dict : dict[str, list]
        This dictionary is numerically data order to list (list of path to data elements in
        input file). Each order indicates a group of data set.
    data_group_concept : NeXus path for NXdata
        This is the concept as /ENTRY[entry]/DATA[data]
    flip_number : int
        The number to multiply with current or field data
    acc:
        The accuracy of the derivative calculation.
    Return:
    -------
    None

    Raise:
    ------
    None
    """

    # pylint: disable=too-many-branches
    def get_axes_and_fields_data(dt_val, data_dict, axes):
        """Fill up template's indivisual data field and the descendant attribute.
        e.g. /Entry[ENTRY]/data/DATA,
          /Entry[ENTRY]/data/DATA/@axes and so on
        """
        dt_grps = []
        axes_name = []
        axes_unit = []
        axes_metadata = []
        axes_data = []

        # Possible axes
        # The axes and data list will be field globaly and used inside other local functions
        data_field_nm = []
        data_field_dt = []
        data_field_unit = []
        # Collects axes, and data field info.
        # list of paths e.g. "/dat_mat_components/Bias/value" comes as
        # dict value of /ENTRY[entry]/DATA[data] in config file.
        for path in dt_val:
            path_data = data_dict.get(path, "")
            if isinstance(path_data, str) and path_data == "":
                continue
            # E.g. extra_annot:'filt', data_grp: LI Demod 1 X [filt]
            # trimed_path: /dat_mat_components/Bias [filt]/
            dt_grp, extra_annot, trimed_path = find_extra_annot(path)
            dt_grps.append(dt_grp)
            is_axis_path = False
            for axis in axes:
                if axis + "value" in trimed_path:
                    # removing forward slash
                    axes_name.append(axis[0:-1].lower())
                    axes_data.append(path_data)
                    axis_unit = path.replace("/value", "/unit")
                    axes_unit.append(
                        data_dict[axis_unit] if axis_unit in data_dict else ""
                    )
                    axis_mtdt = path.replace("/value", "/metadata")
                    axes_metadata.append(
                        data_dict[axis_mtdt] if axis_mtdt in data_dict else ""
                    )
                    is_axis_path = True

            # To collect data field name for each dt_grp
            # All the data field has the same axes
            if not is_axis_path and path[-6:] == "/value":
                if extra_annot in dt_grp and "[" in dt_grp:
                    field = dt_grp[0 : dt_grp.index("[")].strip()
                else:
                    field = dt_grp
                data_field_dt.append(data_dict[path])
                data_field_nm.append(field.lower())
                unit_path = path.replace("/value", "/unit")
                data_field_unit.append(data_dict.get(unit_path, ""))
        # If axes data is not found than assumes all the generated fields usages single
        # common axes data
        if not axes_name and not axes_data:
            axes_data = axs_dt
            axes_name = [ax.lower() for ax in axs_nm]
            axes_metadata = axs_mtdt
            axes_unit = axs_unit
        # No field data is found
        if not data_field_dt or not data_field_nm:
            return {}
        return {
            "axes": {
                "name": axes_name,
                "data": axes_data,
                "unit": axes_unit,
                "metadata": axes_metadata,
            },
            "fields": {
                "name": data_field_nm,
                "data": data_field_dt,
                "unit": data_field_unit,
            },
            "extra_annot": extra_annot,
        }

    def construct_data_group_for_each_field(axis_and_field_data):
        """Construct data group for each field which is  current."""

        axes = axis_and_field_data["axes"]
        fields = axis_and_field_data["fields"]
        extra_annot = axis_and_field_data["extra_annot"]

        # Axes
        axes_data = axes["data"]
        axes_name = axes["name"]
        axes_metadata = axes["metadata"]
        axes_unit = axes["unit"]
        # Fields
        data_field_nm = fields["name"]
        data_field_dt = fields["data"]
        data_field_unit = fields["unit"]

        for dt_fd, dat_, unit in zip(data_field_nm, data_field_dt, data_field_unit):
            dt_fd = "_".join(dt_fd.lower().split(" "))
            if extra_annot:
                temp_data_grp = data_group_concept.replace(
                    "DATA[data", f"DATA[{dt_fd}" f"_{extra_annot}"
                )
            else:
                temp_data_grp = data_group_concept.replace("DATA[data", f"DATA[{dt_fd}")
            template[temp_data_grp + "/@signal"] = dt_fd
            template[temp_data_grp + "/@axes"] = axes_name

            data_field = temp_data_grp + "/" + dt_fd

            # To flip the data plot of Lock-in demodulated signal
            if "li_demod" in dt_fd:
                dat_ = dat_ * flip_number
                template[data_field] = dat_
            else:
                template[data_field] = dat_
            for axis, a_data, a_unit, _ in zip(
                axes_name, axes_data, axes_unit, axes_metadata
            ):
                axis_fd = temp_data_grp + "/" + axis
                if axis_and_field_data["axes"].get("nx_path", None) is not None:
                    axis_and_field_data["axes"]["nx_path"].append(
                        convert_data_dict_path_to_hdf5_path(axis_fd)
                    )
                else:
                    axis_and_field_data["axes"]["nx_path"] = [
                        convert_data_dict_path_to_hdf5_path(axis_fd)
                    ]
                template[temp_data_grp + "/" + axis] = a_data
                template[f"{temp_data_grp}/{axis}/@long_name"] = f"{axis}({a_unit})"
                template[f"{temp_data_grp}/@{axis}_indices"] = 0
                template[f"{temp_data_grp}/{axis}/@units"] = a_unit
            if unit:
                template[data_field + "/@units"] = unit
                template[data_field + "/@long_name"] = f"{dt_fd} ({unit})"
            else:
                template[data_field + "/@long_name"] = dt_fd

    def find_extra_annot(key):
        """Find out extra annotation that comes with data e.g. filt in
        /dat_mat_components/Current [filt]/value, which refers scan in filter mode.
        """
        data_grp = key.split("/")[-2]
        extra_annot = data_grp.split("[")[-1] if "[" in data_grp else ""
        extra_annot = extra_annot.split("]")[0].strip() if extra_annot else ""
        tmp_grp_nm = (
            data_grp[0 : data_grp.index("[")].strip() if "[" in data_grp else data_grp
        )

        return data_grp, extra_annot, key.replace(data_grp, tmp_grp_nm)

    def top_level_Bias_axis(top_ax_list, data_dict, axes):
        """Sometimes Bias axis comes one with: /dat_mat_components/Bias calc/value.
        Later on this bias will be used as a Bias axis for afterward measurements.
        """
        axs_nm = []
        axs_dt = []
        axs_unit = []
        axs_mtdt = []
        for path in top_ax_list:
            for ax in axes:
                if ax not in path:
                    continue
            if "/value" == path[-6:] and path in data_dict:
                axs_dt.append(data_dict[path])
                axs_nm.append("Bias")
                unit_path = path.replace("/value", "/unit")
                axs_unit.append(data_dict[unit_path] if unit_path in data_dict else "")
                metadata_path = path.replace("/value", "/metadata")
                axs_mtdt.append(
                    data_dict[metadata_path] if metadata_path in data_dict else ""
                )
        return axs_nm, axs_dt, axs_unit, axs_mtdt

    # Thses are top level axes, somtimes other measurement occurs with the same Bias axis
    axs_nm: Optional[list[str]] = []
    axs_unit: Optional[list[str]] = []
    axs_mtdt: Optional[list[str]] = []
    axs_dt: Optional[list[str]] = []
    axes = ["Bias/", "Bias calc/"]

    axis_and_field_data: Optional[dict] = None
    # From config file
    #
    # "/ENTRY[entry]/DATA[data]" : {"0": ["/dat_mat_components/Bias calc/value", ...],
    #                               "1": ["/dat_mat_components/Current [filt]/value", ...]}
    for dt_key, dt_val in sub_config_dict.items():
        # There are several scan data gourp in the given file.
        if dt_key == "0":
            # This is top level Bias axis which is the same for all the Lock-in signals
            axs_nm, axs_dt, axs_unit, axs_mtdt = top_level_Bias_axis(
                dt_val, data_dict, axes
            )
        else:
            axis_and_field_data = get_axes_and_fields_data(dt_val, data_dict, axes)
            # No field data is found
            if not axis_and_field_data:
                continue
            construct_data_group_for_each_field(axis_and_field_data)
            construct_nxdata_for_dIbydV(
                axis_and_field_data, template, flip_number, acc=acc
            )


def from_dat_file_into_template(template, dat_file, config_dict, eln_data_dict):
    """Pass metadata, current and voltage into template from eln and dat file."""
    # To collect the concept if any nxdl concept is overwritten
    dict_orig_key_to_mod_key: Dict[str, list] = {}
    b_s_d = BiasSpecData_Nanonis(dat_file)
    flattened_dict = {}
    # BiasSpecData_Nanonis to give slash separated path
    nested_path_to_slash_separated_path(
        b_s_d.get_data_nested_dict(), flattened_dict=flattened_dict
    )

    fill_template_from_eln_data(eln_data_dict, template)
    data_group_concept = "/ENTRY[entry]/DATA[data]"
    for c_key, c_val in config_dict.items():
        if "@eln" in c_val:
            continue
        if c_val in ["", None, "None", "none"]:
            continue
        if isinstance(c_val, str) and flattened_dict.get(c_val, ""):
            template[c_key] = to_intended_t(flattened_dict[c_val])
        if isinstance(c_val, dict) and c_val:
            if data_group_concept == c_key:
                # pass exp. data section to NXdata group
                flip_num = b_s_d.get_flip_number(eln_data_dict)
                construct_nxdata_for_dat(
                    template,
                    flattened_dict,
                    c_val,
                    data_group_concept,
                    flip_num,
                )
            else:
                # pass other physical quantity that has muliple dimensions or type for
                # same physical quantity e.g. in drift_N N will be replaced X, Y and Z
                work_out_overwriteable_field(
                    template, flattened_dict, c_val, c_key, dict_orig_key_to_mod_key
                )
    # The following function can be used if links in application come true
    # link_seperation(template, dict_orig_key_to_mod_key)
    link_seperation_from_hard_code(template, dict_orig_key_to_mod_key)


def get_sts_raw_file_info(raw_file):
    """Parse the raw_file into a plain (keys are organised) dictionary. It helps users as well
    as developers to understand how the reader works and modify the config file.
    """

    base_file = os.path.basename(raw_file)
    raw_name = base_file.split(".")[0]
    temp_file = f"{raw_name}.txt"
    b_s_d = BiasSpecData_Nanonis(raw_file)
    flattened_dict = {}
    nested_path_to_slash_separated_path(
        b_s_d.get_data_nested_dict(), flattened_dict=flattened_dict
    )
    with open(temp_file, mode="w", encoding="utf-8") as txt_f:
        for key, val in flattened_dict.items():
            txt_f.write(f"{key} : {val}\n")

    logging.info(" %s has been created to investigate raw data structure.", temp_file)
