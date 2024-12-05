from abc import ABC, abstractmethod
import argparse
from enum import Enum
from typing import List
import pandas as pd
from azureml.designer.modules.datatransform.common.module_parameter import ModuleParameters, ModuleParameterBase, \
    OutputPortModuleParameter, InputPortModuleParameter, ColumnSelectorModuleParameter
from azureml.designer.modules.datatransform.common.logger import custom_module_logger as logger
from azureml.designer.modules.datatransform.common.logger import format_obj
from azureml.designer.modules.datatransform.common.module_meta_data import ModuleMetaData
from azureml.designer.modules.datatransform.common.module_spec_node import ModuleSpecNode
from azureml.studio.core.io.data_frame_directory import DataFrameDirectory
from azureml.studio.core.data_frame_schema import DataFrameSchema
from azureml.studio.internal.error import ErrorMapping, ParameterParsingError
from azureml.designer.modules.datatransform.tools.dataframe_utils import normalize_dataframe_for_output


class ModuleBase(ABC):

    MODULECLASSNAME = 'module_classname'
    DATAFILENAME = 'data.parquet'

    def __init__(
            self,
            meta_data: ModuleMetaData,
            parameters: ModuleParameters = None,
            module_nodes: List[ModuleSpecNode] = None,
            conda_config_file: str = None):
        self._meta_data = meta_data
        # TODO: enable construct parameters from module nodes.
        self._parameters = parameters
        self._module_nodes = module_nodes if module_nodes else []
        # top level parameters should not be optional
        for node in self._module_nodes:
            if not isinstance(
                    node._module_parameter,
                    InputPortModuleParameter):
                node._is_optional = False
        self._conda_config_file = conda_config_file

    @property
    def parameters(self) -> ModuleParameters:
        return self._parameters

    @property
    def module_nodes(self) -> List[ModuleSpecNode]:
        return self._module_nodes

    @property
    def inputs(self) -> List[ModuleSpecNode]:
        return [node for node in self._module_nodes if not isinstance(
            node._module_parameter, OutputPortModuleParameter)]

    @property
    def outputs(self) -> List[ModuleSpecNode]:
        return [node for node in self._module_nodes if isinstance(
            node._module_parameter, OutputPortModuleParameter)]

    @property
    def meta_data(self) -> ModuleMetaData:
        return self._meta_data

    @property
    def conda_config_file(self) -> str:
        return self._conda_config_file

    def _get_input(self, name: str) -> pd.DataFrame:
        # TODO: add parameter validation
        param = self.parameters[name]
        if isinstance(param, InputPortModuleParameter):
            if param.data is not None:
                return param.data.data.reset_index(drop=True)
        if isinstance(param, ColumnSelectorModuleParameter):
            dfd = param.data
            if dfd is not None:
                return param.data.data.reset_index(drop=True)
        return None

    def _handle_output(self, name: str, data: pd.DataFrame, schema=None):
        # TODO: add parameter validation
        data = normalize_dataframe_for_output(data)
        # logger.info(format_obj(name, data))
        param = self.parameters[name]
        if schema is None:
            schema = DataFrameSchema.data_frame_to_dict(data)
        dfd = DataFrameDirectory.create(
            data=data, schema=schema, compute_visualization=True, compute_stats_in_visualization=True)
        param.data = dfd

    def validate_spec_tree(self, **kwargs):
        # TODO: add validate for parameter tree within invoker.
        pass

    def train(self):
        self.run()
        output_ports = self.parameters.outputs
        for index in range(len(output_ports)):
            output_ports[index].save()

    def run_with_inference_params(
            self,
            ports: list,
            params: dict = None,
            global_params: dict = None):
        logger.info(format_obj("raw params", params))
        logger.info(format_obj("raw global params", global_params))
        inputs = self.parameters.inputs
        for port_index in range(min(len(inputs), len(ports))):
            inputs[port_index].insert_argument(ports[port_index])
        for key, value in global_params.items():
            params[key] = value
        self.parse_and_insert_inference_params(params, True)
        self.run()
        # TODO: use DFD after ds ready
        return [output.data for output in self.parameters.outputs]

    @abstractmethod
    def run(self):
        pass

    def parse_and_insert_inference_params(self, params: dict, validate=False):
        rawargs = []
        if params:
            for parent_node in self._module_nodes:
                for node in parent_node.get_all_nodes():
                    if node._name in params:
                        # arg name convertion align with module spec
                        rawargs.extend(
                            [f'--{node._module_parameter.name}', params[node.name]])
                        del params[node._name]
        self.parse_and_insert_args(rawargs, validate)

    def parse_and_insert_args(self, rawargs, validate=False):
        parser = self.get_arg_parser()
        args = parser.parse_args(rawargs)
        logger.info(format_obj("invoker args", vars(args)))
        self.insert_arguments(**vars(args))
        if validate:
            self.validate_arguments()

    def get_arg_parser(self) -> argparse.ArgumentParser:
        logger.info("Construct arg parser")
        parser = argparse.ArgumentParser()
        parser.add_argument(
            self.MODULECLASSNAME,
            help="current module class name for constructor",
            nargs='?')
        param: ModuleParameterBase
        for key, param in self.parameters:
            logger.info("arg: %s", key)
            # TODO: need to switch to SpecModuleNode.name after yaml support
            # name & display_name
            extra_keys = set([item._name for sublist in [node.get_nodes(
                param) for node in self._module_nodes] for item in sublist])
            extra_keys.discard(key)
            keys = ["--" + key]
            keys.extend(["--" + item for item in extra_keys])
            for key in keys:
                if '_' in key:
                    new_key = key.replace('_', '-')
                    if new_key not in keys:
                        keys.append(new_key)
            if issubclass(param.data_type, Enum):
                parser.add_argument(
                    *keys,
                    help=param.description,
                    type=EnumArgType(
                        param.data_type,
                        param.friendly_name),
                    required=False,
                    choices=list(
                        param.data_type))
            else:
                parser_type = BooleanArgType(
                    param.friendly_name) if param.data_type is bool else param.data_type
                parser.add_argument(*keys, help=param.description,
                                    type=parser_type, required=False)
        return parser

    def insert_arguments(self, **kwargs):
        if self.MODULECLASSNAME in kwargs:
            kwargs.pop(self.MODULECLASSNAME)
        self.parameters.insert_arguments(**kwargs)

    def validate_arguments(self):
        self.parameters.validate_arguments()

    def get_args(self):
        args = {}
        for node in self._module_nodes:
            args.update(node.get_args())
        return args


class BooleanArgType(object):
    def __init__(self, display_name: str):
        self._display_name = display_name

    def __call__(self, value: str):
        if value is False or value is True:
            return value
        value = value.strip()
        if not value:
            ErrorMapping.throw(
                ParameterParsingError(
                    self._display_name,
                    to_type="boolean",
                    from_type="string",
                    arg_value=value))
        if value.lower() in ["t", "y", "1", "true"]:
            return True
        if value.lower() in ["f", "n", "0", "false"]:
            return False
        ErrorMapping.throw(
            ParameterParsingError(
                self._display_name,
                to_type="boolean",
                from_type="string",
                arg_value=value))


class EnumArgType(object):
    def __init__(self, enum: Enum, display_name: str):
        self._enum = enum
        self._display_name = display_name

    def __call__(self, value):
        if isinstance(value, self._enum):
            return value
        try:
            return self._enum[value]
        except KeyError:
            ErrorMapping.throw(
                ParameterParsingError(
                    self._display_name,
                    to_type=self._enum,
                    from_type="string",
                    arg_value=value))
