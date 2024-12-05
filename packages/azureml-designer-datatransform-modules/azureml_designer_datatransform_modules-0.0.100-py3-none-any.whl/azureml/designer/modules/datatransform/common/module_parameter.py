from typing import Type, List
from enum import Enum
from abc import ABC, abstractmethod

from azureml.studio.core.utils.strutils import decode_script_string
from azureml.studio.internal.error import ErrorMapping, NotInRangeValueError, ParameterParsingError, NullOrEmptyError, \
    ColumnNotFoundError
from azureml.studio.core.io.data_frame_directory import load_data_frame_from_directory, DataFrameDirectory
from azureml.studio.core.data_frame_schema import DataFrameSchema
from azureml.designer.modules.datatransform.common.logger import custom_module_logger as logger, format_obj
from azureml.studio.core.utils.column_selection import ColumnSelection, ColumnSelectionColumnNotFoundError
import pandas as pd
from urllib.parse import unquote


class ModuleParameterBase(ABC):
    def __init__(
            self,
            name: str = None,
            friendly_name: str = None,
            description: str = None,
            data_type: type = None,
            is_optional: bool = True,
            default_value=None
    ):
        self._name = name
        self._friendly_name = name if friendly_name is None else friendly_name
        self._description = name if description is None else description
        self._data_type = data_type
        self._is_optional = is_optional
        self._default_value = default_value
        self._value = None

    @property
    def name(self):
        return self._name

    @property
    def friendly_name(self):
        return self._friendly_name

    @property
    def description(self):
        return self._description

    @property
    def data_type(self):
        return self._data_type

    @property
    def default_value(self):
        return self._default_value

    @property
    def value(self):
        return self._value

    @property
    def is_optional(self):
        return self._is_optional

    @property
    @abstractmethod
    def parameter_type(self):
        pass

    def validate(self):
        if not self.is_optional and self.value is None:
            raise ErrorMapping.throw(NullOrEmptyError(self._friendly_name))
        return True

    def insert_argument(self, value):
        if value is not None and not isinstance(value, self.data_type):
            ErrorMapping.throw(ParameterParsingError(self.friendly_name))
        self._value = value


class ModuleParameterTypes(Enum):
    InputPort = "inputPath"
    OutputPort = "outputPath"
    Other = "inputValue"


class IOPortModuleParameter(ModuleParameterBase):
    def __init__(self, name=None, friendly_name=None, description=None, is_optional=False
                 ):
        super().__init__(name=name, friendly_name=friendly_name, description=description,
                         data_type=str, is_optional=is_optional,
                         )

    def validate(self):
        super().validate()
        if self.value is None:
            return
        if not isinstance(self.value, self.data_type):
            raise TypeError(
                f"Unexpected data type for input port '{self.name}'."
                f" Expected {self.data_type} but got {type(self.value)}.")


class InputPortModuleParameter(IOPortModuleParameter):
    def __init__(self, name=None, friendly_name=None, description=None, is_optional=False,
                 ):
        self._data = None
        super().__init__(name=name, friendly_name=friendly_name, description=description,
                         is_optional=is_optional,
                         )

    @property
    def parameter_type(self):
        return ModuleParameterTypes.InputPort

    def insert_argument(self, value):
        if value is not None:
            if isinstance(value, str):
                self._value = value
            elif isinstance(value, DataFrameDirectory):
                self._data = value
            elif isinstance(value, pd.DataFrame):
                self._data = DataFrameDirectory.create(
                    data=value,
                    schema=DataFrameSchema.data_frame_to_dict(value),
                    compute_visualization=False
                )
            else:
                ErrorMapping.throw(ParameterParsingError(self.friendly_name))
        self._value = value

    @property
    def data(self):
        if self._data is not None:
            return self._data
        if self._value:
            logger.info(f"Read data from {self._value}")
            self._data = load_data_frame_from_directory(self._value)
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def validate(self):
        if not self.is_optional and self.value is None and self._data is None:
            raise ErrorMapping.throw(NullOrEmptyError(self._friendly_name))
        return True


class OutputPortModuleParameter(IOPortModuleParameter):
    def __init__(self, name=None, friendly_name=None, description=None, is_optional=False
                 ):
        self._data = None
        super().__init__(name=name, friendly_name=friendly_name, description=description,
                         is_optional=is_optional,
                         )

    @property
    def parameter_type(self):
        return ModuleParameterTypes.OutputPort

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def save(self, compute_visualization=True):
        logger.info(format_obj(self._friendly_name, self._data))
        if not self._value:
            raise ValueError('Path is None for save of {self._friendly_name}')
        if not isinstance(self.data, DataFrameDirectory):
            raise ValueError(
                'data of output should be type DataFrameDirectory')
        if compute_visualization:
            self.data = DataFrameDirectory.create(
                data=self.data.data, schema=self.data.schema_data,
                compute_visualization=True, compute_stats_in_visualization=True
            )
        self.data.dump(self._value)
        logger.info("Write output to (\"%s\") %s", self.name, self.value)

    def validate(self):
        if self.value is not None and not isinstance(self.value, str):
            raise ErrorMapping.throw(
                ParameterParsingError(
                    self._friendly_name))


class ScriptModuleParameter(ModuleParameterBase):
    def __init__(
            self,
            name=None,
            friendly_name=None,
            default_value=None,
            description=None,
            is_optional=False,
            language=None):
        self._language = language
        super().__init__(
            name=name,
            friendly_name=friendly_name,
            default_value=default_value,
            description=description,
            data_type=str,
            is_optional=is_optional,
        )

    @property
    def parameter_type(self):
        return ModuleParameterTypes.Other

    @property
    def language(self):
        return self._language

    def insert_argument(self, value):
        if value is not None and not isinstance(value, self.data_type):
            ErrorMapping.throw(ParameterParsingError(self.friendly_name))
        self._value = decode_script_string(value)


class ValueModuleParameter(ModuleParameterBase):
    def __init__(
        self,
        name=None,
        friendly_name=None,
        default_value=None,
        description=None,
        data_type=None,
        is_optional=True,
    ):
        super().__init__(name=name, friendly_name=friendly_name, default_value=default_value, description=description,
                         data_type=data_type, is_optional=is_optional,
                         )

    @property
    def parameter_type(self):
        return ModuleParameterTypes.Other


class PercentileValueModuleParameter(ValueModuleParameter):
    def __init__(self, name=None, friendly_name=None, default_value=None, description=None, is_optional=True,
                 ):
        super().__init__(name=name, friendly_name=friendly_name, default_value=default_value, description=description,
                         data_type=float, is_optional=is_optional,
                         )

    def validate(self):
        super().validate()
        if self.value is not None and (self.value < 0 or self.value > 100):
            ErrorMapping.throw(
                NotInRangeValueError(
                    self._friendly_name, 0, 100))


class ColumnSelectorModuleParameter(ModuleParameterBase):
    def __init__(
        self,
        name=None,
        friendly_name=None,
        description=None,
        input_port: InputPortModuleParameter = None,
        is_optional=True,
        default_value=None,
    ):
        self._input_port = input_port
        super().__init__(
            name=name,
            friendly_name=friendly_name,
            description=description,
            data_type=str,
            is_optional=is_optional,
            default_value=default_value,
        )

    def bind_input(self, input_port: InputPortModuleParameter):
        self._input_port = input_port

    @property
    def input_port(self):
        return self._input_port

    @property
    def parameter_type(self):
        return ModuleParameterTypes.Other

    def validate(self):
        super().validate()
        if self.value is not None:
            json_string = unquote(self.value)
            ColumnSelection(json_string)

    @property
    def data(self):
        if self.value:
            json_string = unquote(self.value)
            try:
                column_selector = ColumnSelection(json_string)
                return column_selector.select_dataframe_directory(
                    self.input_port.data)
            except ColumnSelectionColumnNotFoundError as colNotFoundErr:
                ErrorMapping.rethrow(colNotFoundErr, ColumnNotFoundError)
        else:
            return self.input_port.data


class ModuleParameters():
    def __init__(self, parameters: List[Type[ModuleParameterBase]]):
        self._parameters = parameters
        self._parameters_dict = {para.name: para for para in parameters}

    def __getitem__(self, item) -> ModuleParameterBase:
        return self._parameters_dict[item]

    def __setitem__(self, key, item):
        self._parameters_dict[key] = item

    def __iter__(self):
        for item in self._parameters:
            yield (item.name, item)

    @property
    def parameters(self):
        return self._parameters

    @property
    def inputs(self) -> List[InputPortModuleParameter]:
        return [
            parameter for parameter in self._parameters if isinstance(
                parameter,
                InputPortModuleParameter)]

    @property
    def outputs(self) -> List[OutputPortModuleParameter]:
        return [
            parameter for parameter in self._parameters if isinstance(
                parameter,
                OutputPortModuleParameter)]

    def insert_arguments(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self._parameters_dict:
                # should not happen for studio
                raise ValueError(f"Unexpected parameter '{key}'.")
            param = self._parameters_dict[key]
            param.insert_argument(value)

    def validate_arguments(self):
        para: ModuleParameterBase
        for para in self._parameters:
            para.validate()

    def get_args(self):
        return {f"--{param.name}": {param.parameter_type: param.description}
                for param in self._parameters}
