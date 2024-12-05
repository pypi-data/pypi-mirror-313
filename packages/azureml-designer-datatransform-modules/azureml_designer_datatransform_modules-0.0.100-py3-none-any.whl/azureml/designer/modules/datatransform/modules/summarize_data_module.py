import pandas as pd
import numpy as np
import sys
from azureml.designer.modules.datatransform.common.module_base import ModuleBase
from azureml.designer.modules.datatransform.common.module_parameter import ModuleParameters, InputPortModuleParameter, \
    OutputPortModuleParameter
from azureml.designer.modules.datatransform.common.logger import custom_module_logger as logger
from azureml.designer.modules.datatransform.common.module_meta_data import ModuleMetaData
from azureml.designer.modules.datatransform.common.module_spec_node import ModuleSpecNode
from azureml.studio.core.utils.missing_value_utils import has_na


class SummarizeDataModule(ModuleBase):
    def __init__(self):
        meta_data = ModuleMetaData(
            id="2c57074f-674f-45de-ad85-d84e4726f04e",
            name="Summarize Data",
            category="Statistical Functions",
            description="Generates a basic descriptive statistics report for the columns in a dataset.")
        parameters = ModuleParameters([
            InputPortModuleParameter(
                name="input", friendly_name="Input", is_optional=False),
            OutputPortModuleParameter(
                name="dataset", friendly_name="Result_dataset", is_optional=False)
        ])
        module_nodes = [
            ModuleSpecNode.from_module_parameter(parameters["input"]),
            ModuleSpecNode.from_module_parameter(parameters["dataset"]),
        ]
        conda_config_file = './azureml/designer/modules/datatransform/modules/conda_config/summarize_data_module.yml'
        super().__init__(
            meta_data=meta_data,
            parameters=parameters,
            module_nodes=module_nodes,
            conda_config_file=conda_config_file)

    def run(self):
        logger.info("Read input data")
        input_data = self._get_input("input")
        output = pd.DataFrame()
        logger.info('Summarize input data')
        for column in input_data.columns:
            output = pd.concat([output, Series_Summarize(
                input_data[column]).get_summarize()])
        logger.info("Normalize output columns to corresponding data types")
        output = SummarizeDataModule._normalize_column(input_data, output)
        self._handle_output("dataset", output)

    @staticmethod
    def _include_mix_datetime(data: pd.DataFrame):
        include_datetime = [
            Series_Summarize._is_datetime(
                data[column]) for column in data]
        return any(include_datetime) and not all(include_datetime)

    @staticmethod
    def _normalize_column(data: pd.DataFrame, output: pd.DataFrame):
        if SummarizeDataModule._include_mix_datetime(data):
            convert_columns = [
                "Mode",
                "Min",
                "Max",
                "Mean",
                "1st quantile",
                "Median",
                "3rd quantile",
                "P0.5",
                "P1",
                "P5",
                "P95",
                "P99",
                "P99.5"]
            for column in convert_columns:
                output[column] = output[column].apply(str)
        for column in output.columns:
            column_type = pd.api.types.infer_dtype(output[column])
            if column_type == "integer":
                # Do not use astype("Int64") here because this type is not supported by some Numpy functions.
                if has_na(output[column], include_inf=True):
                    output[column] = output[column].astype('float')
                else:
                    output[column] = output[column].astype('int64')
            if column_type == "floating":
                output[column] = output[column].astype('float')
            if column_type == "boolean":
                output[column] = output[column].astype('bool')
        return output


class Series_Summarize():
    def __init__(self, ds: pd.Series):
        self._data = ds
        self._is_timedelta = Series_Summarize._is_timedelta(ds)
        self._is_datetime = Series_Summarize._is_datetime(ds)
        self._is_boolean = Series_Summarize._is_boolean(ds)
        self._preprocess_data = Series_Summarize._preprocess_data(ds)

    INT_MAX = sys.maxsize
    INT_MIN = -sys.maxsize - 1

    @staticmethod
    def _is_datetime(ds: pd.Series) -> bool:
        return not Series_Summarize._is_timedelta(
            ds) and pd.api.types.is_datetime64_any_dtype(ds)

    @staticmethod
    def _is_timedelta(ds: pd.Series) -> bool:
        return pd.core.dtypes.common.is_timedelta64_dtype(ds)

    @staticmethod
    def _is_boolean(ds: pd.Series) -> bool:
        return ds.dtype.name == "bool"

    @staticmethod
    def _preprocess_data(ds: pd.Series) -> pd.Series:
        if Series_Summarize._is_timedelta(ds):
            return ds.apply(lambda dt: pd.to_timedelta(dt).value).apply(
                lambda td: td if td != Series_Summarize.INT_MIN else None)
        if Series_Summarize._is_datetime(ds):
            return ds.apply(lambda dt: pd.to_datetime(dt).value).apply(
                lambda dt: dt if dt != Series_Summarize.INT_MIN else None)
        if Series_Summarize._is_boolean(ds):
            return ds.apply(lambda dt: 1.0 if dt else 0.0)
        return ds

    def _special_handle(self, fn, return_time_span=False):
        if self._is_boolean:
            return fn(self._preprocess_data)
        if not self._is_datetime and not self._is_timedelta:
            return fn(self._data)
        if self._is_timedelta:
            return None
        if return_time_span:
            return None
        # for datetime type
        _preprocess_data_numeric_format = pd.to_numeric(self._preprocess_data)
        return pd.to_datetime(fn(_preprocess_data_numeric_format))

    def _special_handle_skew_kurt(self, fn):
        # Fix bug 850740: when empty dataframe column with 'datetime64' type is processed,
        # it fails to convert to numeric in self._preprocess_data() function.
        # Change the data type to numeric before doing skew or kurt here if necessary.
        _preprocess_data_numeric_format = pd.to_numeric(self._preprocess_data)
        return fn(_preprocess_data_numeric_format)

    @staticmethod
    def _get_mode_str(ds: pd.Series):
        if ds.size > 1:
            return '{' + ', '.join([str(m) for m in ds]) + '}'
        elif ds.size == 1:
            return str(ds[0])
        return None

    def _is_numeric(self) -> bool:
        # np.issubdtype works for numpy's dtypes but fails for pandas specific types like pd.Categorical
        # pd.Categorical not numeric types
        if self._is_timedelta or self._is_datetime or pd.api.types.is_numeric_dtype(self._data):
            return True
        return False

    def _is_full_process(self) -> bool:
        return self._is_numeric() or self._is_boolean

    def _percentile(self, p):
        if self._is_full_process():
            return self._special_handle(lambda x: x.quantile(p / 100.0))
        return None

    def _range(self):
        if not self._is_full_process():
            return None
        if self._is_numeric() and not self._is_datetime and not self._is_timedelta and not self._is_boolean:
            return self._data.max() - self._data.min()
        if self._data.max() == self._data.min():
            return 0
        if self._is_boolean:
            return 1
        return None

    def _unique_value_count(self):
        if len(self._data.index) == 0:
            return None

        # Cannot directly use nunique for pandas series with dictionary value,
        # because dictionary is unhashable.
        if any(isinstance(self._data.iloc[i], dict) for i in range(len(self._data))):
            return pd.Series(self._data.tolist()).apply(
                lambda x: tuple(sorted(x.items())) if isinstance(x, dict) else x).nunique()

        if not isinstance(self._data.iloc[0], np.ndarray):
            return self._data.nunique()
        else:
            return pd.Series(self._data.tolist()).apply(lambda x: tuple(sorted(x))).nunique()

    def _mode(self):
        # Fix bug 901960: it fails to visualize summarize data output when column "mode" produces long strings.
        # In addition to be consistent with V1, only apply mode function on columns with numeric or boolean types.
        if not self._is_full_process():
            return None
        if len(self._data.index) == 0:
            return None
        if type(self._data.iloc[0]) != np.ndarray:
            return Series_Summarize._get_mode_str(self._data.mode())
        else:
            None

    def get_summarize(self) -> pd.DataFrame:
        functions = {
            "Feature": self._data.name,
            "Count": self._data.count(),
            "Unique Value Count": self._unique_value_count(),
            "Missing Value Count": (self._data.isnull()).sum(),
            "Min": self._data.min() if self._is_full_process() else None,
            "Max": self._data.max() if self._is_full_process() else None,
            "Mean": self._special_handle(lambda x: x.mean()) if self._is_full_process() else None,
            "Mean Deviation": self._special_handle(
                lambda x: x.mad()) if self._is_full_process() and not self._is_datetime and
            not self._is_timedelta else None,
            # can not output time delta
            "1st quantile": self._percentile(25),
            "Median": self._special_handle(lambda x: x.median()) if self._is_full_process() else None,
            "3rd quantile": self._percentile(75),
            "Mode": self._mode(),
            "Range": self._range(),
            "Sample Variance": self._data.var() if self._is_boolean or (
                not self._is_timedelta and not self._is_datetime and self._is_numeric()) else None,
            # can not output time delta
            "Sample Standard Deviation": self._special_handle(
                lambda x: x.std()) if self._is_full_process() and
            not self._is_datetime and not self._is_timedelta
            else None,
            "Sample Skewness": self._special_handle_skew_kurt(lambda x: x.skew()) if self._is_full_process() else None,
            "Sample Kurtosis": self._special_handle_skew_kurt(lambda x: x.kurt()) if self._is_full_process() else None,
            "P0.5": self._percentile(0.5),
            "P1": self._percentile(1),
            "P5": self._percentile(5),
            "P95": self._percentile(95),
            "P99": self._percentile(99),
            "P99.5": self._percentile(99.5),
        }
        data = pd.Series(functions, name=self._data.name).to_frame().T
        return data
