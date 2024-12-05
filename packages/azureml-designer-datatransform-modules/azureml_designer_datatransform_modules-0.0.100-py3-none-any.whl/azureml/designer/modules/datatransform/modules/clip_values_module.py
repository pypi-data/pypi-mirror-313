from enum import Enum

import numpy as np
import pandas as pd
from azureml.studio.core.error import UserError

from azureml.designer.modules.datatransform.common.logger import custom_module_logger as logger
from azureml.designer.modules.datatransform.common.logger import format_obj
from azureml.designer.modules.datatransform.common.module_base import ModuleBase
from azureml.designer.modules.datatransform.common.module_meta_data import ModuleMetaData
from azureml.designer.modules.datatransform.common.module_parameter import InputPortModuleParameter, \
    OutputPortModuleParameter, ValueModuleParameter, PercentileValueModuleParameter, ColumnSelectorModuleParameter, \
    ModuleParameters
from azureml.designer.modules.datatransform.common.module_spec_node import ModuleSpecNode
from azureml.designer.modules.datatransform.tools.column_selection_utils import convert_column_selection_to_json
from azureml.studio.core.utils.column_selection import ColumnSelectionBuilder, ColumnType
from azureml.studio.core.utils.missing_value_utils import is_na
from azureml.studio.internal.error import ErrorMapping


class ClipMode(Enum):
    ClipPeaks = 'ClipPeaks'
    ClipSubPeaks = 'ClipSubPeaks'
    ClipPeaksAndSubpeaks = 'ClipPeaksAndSubpeaks'


class Threshold(Enum):
    Constant = 'Constant'
    Percentile = 'Percentile'


class ReplaceMode(Enum):
    Threshold = 'Threshold'
    Mean = 'Mean'
    Median = 'Median'
    Missing = 'Missing'


class ClipValuesModule(ModuleBase):
    _CLIPMODE = "clipmode"
    _THRESHOLD = "threshold"
    _UP_PERCENTILE_THRESHOLD = "up_percentile_threshold"
    _BOTTOM_PERCENTILE_THRESHOLD = "bottom_percentile_threshold"
    _UP_CONSTANT_THRESHOLD = "up_constant_threshold"
    _BOTTOM_CONSTANT_THRESHOLD = "bottom_constant_threshold"
    _UP_REPLACE_MODE = "up_replace_mode"
    _BOTTOM_REPLACE_MODE = "bottom_replace_mode"
    _INPLACE_FLAG = "inplace_flag"
    _INDICATOR_FLAG = "indicator_flag"
    _COLUMN_SELECTOR = "column_selector"
    _INPUT = "input"
    _DATASET = "dataset"

    def __init__(self):
        meta_data = ModuleMetaData(
            id="cdc62e1d-b64f-424c-ac09-bb050918a668",
            name="Clip Values",
            category="Data Transformation",
            description="Detects outliers and clips or replaces their values.")
        parameters = ModuleParameters([
            ValueModuleParameter(
                name=ClipValuesModule._CLIPMODE,
                friendly_name="Set of thresholds",
                data_type=ClipMode,
                default_value=ClipMode.ClipPeaks),
            ValueModuleParameter(
                name=ClipValuesModule._THRESHOLD,
                friendly_name="Threshold",
                data_type=Threshold,
                default_value=Threshold.Constant),
            PercentileValueModuleParameter(
                name=ClipValuesModule._UP_PERCENTILE_THRESHOLD,
                friendly_name="Percentile value for upper threshold",
                default_value=99,
            ),
            PercentileValueModuleParameter(
                name=ClipValuesModule._BOTTOM_PERCENTILE_THRESHOLD,
                friendly_name="Percentile value for lower threshold",
                default_value=1,
            ),
            ValueModuleParameter(
                name=ClipValuesModule._UP_CONSTANT_THRESHOLD,
                friendly_name="Constant value for upper threshold",
                data_type=float,
                default_value=99,
            ),
            ValueModuleParameter(
                name=ClipValuesModule._BOTTOM_CONSTANT_THRESHOLD,
                friendly_name="Constant value for lower threshold",
                data_type=float,
                default_value=1,
            ),
            ValueModuleParameter(
                name=ClipValuesModule._UP_REPLACE_MODE,
                friendly_name="Substitute value for peaks",
                data_type=ReplaceMode,
                default_value=ReplaceMode.Threshold,
            ),
            ValueModuleParameter(
                name=ClipValuesModule._BOTTOM_REPLACE_MODE,
                friendly_name="Substitute value for subpeaks",
                data_type=ReplaceMode,
                default_value=ReplaceMode.Threshold,
            ),
            ValueModuleParameter(
                name=ClipValuesModule._INPLACE_FLAG,
                friendly_name="Overwrite flag",
                data_type=bool,
                default_value=True),
            ValueModuleParameter(
                name=ClipValuesModule._INDICATOR_FLAG,
                friendly_name="Add indicator columns",
                data_type=bool,
                default_value=False),
            ColumnSelectorModuleParameter(
                name=ClipValuesModule._COLUMN_SELECTOR,
                friendly_name="List of columns",
                default_value=convert_column_selection_to_json(
                    ColumnSelectionBuilder().include_col_types(ColumnType.NUMERIC))),
            InputPortModuleParameter(
                name=ClipValuesModule._INPUT, friendly_name="Input", is_optional=False),
            OutputPortModuleParameter(
                name=ClipValuesModule._DATASET, friendly_name="Result_dataset", is_optional=False)
        ])
        parameters[ClipValuesModule._COLUMN_SELECTOR].bind_input(
            parameters[ClipValuesModule._INPUT])
        # root
        module_node_clip_mode = ModuleSpecNode.from_module_parameter(
            parameters[ClipValuesModule._CLIPMODE])
        # child 1
        module_node_threshold_type = ModuleSpecNode(name="upperThreshold",
                                                    friendly_name="Upper threshold",
                                                    module_parameter=parameters[ClipValuesModule._THRESHOLD],
                                                    parent_node=module_node_clip_mode,
                                                    options=[ClipMode.ClipPeaks])
        ModuleSpecNode(name="constantUpperThreshold",
                       module_parameter=parameters[ClipValuesModule._UP_CONSTANT_THRESHOLD],
                       parent_node=module_node_threshold_type,
                       options=[Threshold.Constant])
        ModuleSpecNode(name="percentileUpperThreshold",
                       module_parameter=parameters[ClipValuesModule._UP_PERCENTILE_THRESHOLD],
                       parent_node=module_node_threshold_type,
                       options=[Threshold.Percentile])
        ModuleSpecNode(name="modeUpperSubstitute",
                       module_parameter=parameters[ClipValuesModule._UP_REPLACE_MODE],
                       parent_node=module_node_clip_mode,
                       options=[ClipMode.ClipPeaks])
        # child 2
        module_node_threshold_type = ModuleSpecNode(name="lowerThreshold",
                                                    friendly_name="Lower threshold",
                                                    module_parameter=parameters[ClipValuesModule._THRESHOLD],
                                                    parent_node=module_node_clip_mode,
                                                    options=[ClipMode.ClipSubPeaks])
        ModuleSpecNode(name="constantLowerThreshold",
                       module_parameter=parameters[ClipValuesModule._BOTTOM_CONSTANT_THRESHOLD],
                       parent_node=module_node_threshold_type,
                       options=[Threshold.Constant])
        ModuleSpecNode(name="percentileLowerThreshold",
                       module_parameter=parameters[ClipValuesModule._BOTTOM_PERCENTILE_THRESHOLD],
                       parent_node=module_node_threshold_type,
                       options=[Threshold.Percentile])
        ModuleSpecNode(name="modeowerSubstitute",
                       module_parameter=parameters[ClipValuesModule._BOTTOM_REPLACE_MODE],
                       parent_node=module_node_clip_mode,
                       options=[ClipMode.ClipSubPeaks])
        # child 3
        module_node_threshold_type = ModuleSpecNode(name="lowerUpperThreshold",
                                                    module_parameter=parameters[ClipValuesModule._THRESHOLD],
                                                    parent_node=module_node_clip_mode,
                                                    options=[ClipMode.ClipPeaksAndSubpeaks])
        ModuleSpecNode(name="constantUThreshold",
                       module_parameter=parameters[ClipValuesModule._UP_CONSTANT_THRESHOLD],
                       parent_node=module_node_threshold_type,
                       options=[Threshold.Constant])
        ModuleSpecNode(name="percentileUThreshold",
                       module_parameter=parameters[ClipValuesModule._UP_PERCENTILE_THRESHOLD],
                       parent_node=module_node_threshold_type,
                       options=[Threshold.Percentile])
        ModuleSpecNode(name="constantLThreshold",
                       module_parameter=parameters[ClipValuesModule._BOTTOM_CONSTANT_THRESHOLD],
                       parent_node=module_node_threshold_type,
                       options=[Threshold.Constant])
        ModuleSpecNode(name="percentileLThreshold",
                       module_parameter=parameters[ClipValuesModule._BOTTOM_PERCENTILE_THRESHOLD],
                       parent_node=module_node_threshold_type,
                       options=[Threshold.Percentile])
        ModuleSpecNode(name="modeUSubstitute",
                       module_parameter=parameters[ClipValuesModule._UP_REPLACE_MODE],
                       parent_node=module_node_clip_mode,
                       options=[ClipMode.ClipPeaksAndSubpeaks])
        ModuleSpecNode(name="modeLSubstitute",
                       module_parameter=parameters[ClipValuesModule._BOTTOM_REPLACE_MODE],
                       parent_node=module_node_clip_mode,
                       options=[ClipMode.ClipPeaksAndSubpeaks])
        module_nodes = [
            module_node_clip_mode,
            ModuleSpecNode.from_module_parameter(parameters[ClipValuesModule._COLUMN_SELECTOR]),
            ModuleSpecNode.from_module_parameter(parameters[ClipValuesModule._INPLACE_FLAG]),
            ModuleSpecNode.from_module_parameter(parameters[ClipValuesModule._INDICATOR_FLAG]),
            ModuleSpecNode.from_module_parameter(parameters[ClipValuesModule._INPUT]),
            ModuleSpecNode.from_module_parameter(parameters[ClipValuesModule._DATASET])
        ]
        conda_config_file = './azureml/designer/modules/datatransform/modules/conda_config/clip_values_module.yml'
        super().__init__(
            meta_data=meta_data,
            parameters=parameters,
            module_nodes=module_nodes,
            conda_config_file=conda_config_file)

    def run(self):
        inputdata = self._get_input("input")
        selected_data = self._get_input("column_selector")
        clipmode = self.parameters["clipmode"].value

        for selected_column_name in selected_data:
            selected_column: pd.Series
            selected_column = selected_data[selected_column_name]

            if not selected_column.dropna().count() == 0 and \
                    not pd.api.types.is_numeric_dtype(selected_column):
                error_message = f"Specified column \"{selected_column.name}\" dtype is " \
                                f"{selected_column.dtype} which is non-numeric. " \
                                f"This type is not supported by the module."
                ErrorMapping.throw(UserError(error_message))

            up_threshold = None
            up_replace_value = None
            if clipmode in [ClipMode.ClipPeaks, ClipMode.ClipPeaksAndSubpeaks]:
                up_threshold = \
                    self.parameters["up_constant_threshold"].value \
                    if self.parameters["threshold"].value == Threshold.Constant \
                    else selected_column.quantile(self.parameters["up_percentile_threshold"].value / 100.0)
                up_replace_mode = self.parameters["up_replace_mode"].value
                up_replace_value = \
                    up_threshold \
                    if up_replace_mode == ReplaceMode.Threshold \
                    else selected_column.median() \
                    if up_replace_mode == ReplaceMode.Median \
                    else selected_column.mean() \
                    if up_replace_mode == ReplaceMode.Mean \
                    else None
            logger.info(format_obj("up_threshold", up_threshold))
            logger.info(format_obj("up_replace_value", up_replace_value))
            bottom_threshold = None
            bottom_replace_value = None
            if clipmode in [
                    ClipMode.ClipSubPeaks,
                    ClipMode.ClipPeaksAndSubpeaks]:
                bottom_threshold = \
                    self.parameters["bottom_constant_threshold"].value \
                    if self.parameters["threshold"].value == Threshold.Constant \
                    else selected_column.quantile(self.parameters["bottom_percentile_threshold"].value / 100.0)
                bottom_replace_mode = self.parameters["bottom_replace_mode"].value
                bottom_replace_value = \
                    up_threshold \
                    if bottom_replace_mode == ReplaceMode.Threshold \
                    else selected_column.median() \
                    if bottom_replace_mode == ReplaceMode.Median \
                    else selected_column.mean() \
                    if bottom_replace_mode == ReplaceMode.Mean \
                    else None
            logger.info(format_obj("bottom_threshold", bottom_threshold))
            logger.info(format_obj(
                "bottom_replace_value", bottom_replace_value))
            logger.info('Applying clip value functions on selected input dataset')
            clip_result = self.clip_function(
                selected_column,
                up_threshold,
                up_replace_value,
                bottom_threshold,
                bottom_replace_value)
            clip_result = clip_result.astype(float)
            if self.parameters["inplace_flag"].value is True:
                inputdata[selected_column_name] = clip_result
            else:
                column_index = inputdata.columns.get_loc(
                    selected_column_name) + 1
                inputdata.insert(column_index, selected_column_name +
                                 '_clipped_value', clip_result)
            if self.parameters["indicator_flag"].value is True:
                logger.info('Add indicator columns to output')
                indicator_result = self.clip_function(
                    selected_column,
                    up_threshold,
                    up_replace_value,
                    bottom_threshold,
                    bottom_replace_value,
                    True)
                column_index = inputdata.columns.get_loc(
                    selected_column_name if self.parameters["inplace_flag"].value is True
                    else selected_column_name + '_clipped_value') + 1
                inputdata.insert(
                    column_index,
                    selected_column_name +
                    '_clipped',
                    indicator_result)

        self._handle_output("dataset", inputdata)

    def clip_function_with_indicator(self, x, up_threshold, bottom_threshold):
        if is_na(x):
            return False
        if (up_threshold is not None and x > up_threshold) or (bottom_threshold is not None and x < bottom_threshold):
            return True
        else:
            return False

    def clip_function_no_indicator(self, x, up_threshold, up_replace_value,
                                   bottom_threshold, bottom_replace_value):
        if is_na(x):
            return np.NaN
        if up_threshold is not None and x > up_threshold:
            return up_replace_value
        else:
            if bottom_threshold is not None and x < bottom_threshold:
                return bottom_replace_value
            else:
                return x

    def clip_function(
            self,
            column,
            up_threshold,
            up_replace_value,
            bottom_threshold,
            bottom_replace_value,
            indicator: bool = False):
        if indicator is True:
            return column.apply(lambda x: self.clip_function_with_indicator(x, up_threshold, bottom_threshold))
        else:
            return column.apply(lambda x: self.clip_function_no_indicator(x, up_threshold, up_replace_value,
                                                                          bottom_threshold, bottom_replace_value))
