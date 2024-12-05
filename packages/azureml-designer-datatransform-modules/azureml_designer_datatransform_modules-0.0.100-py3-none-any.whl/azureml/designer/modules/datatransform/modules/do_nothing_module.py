from azureml.designer.modules.datatransform.common.module_base import ModuleBase
from azureml.designer.modules.datatransform.common.module_meta_data import ModuleMetaData
from azureml.designer.modules.datatransform.common.module_parameter import InputPortModuleParameter, \
    OutputPortModuleParameter, ValueModuleParameter, ModuleParameters
from azureml.designer.modules.datatransform.common.module_spec_node import ModuleSpecNode
from azureml.designer.modules.datatransform.common.logger import custom_module_logger as logger
import shutil
import errno


class DoNothingModule(ModuleBase):
    def __init__(self):
        meta_data = ModuleMetaData(
            id="f6de26a9-cc74-4df9-8cd5-e9902fc91164",
            name="Do Nothing",
            category="Internal",
            description="Save DFD Genererate By Dprep")
        parameters = ModuleParameters(
            [
                InputPortModuleParameter(
                    name="input",
                    friendly_name="Input",
                    is_optional=False),
                OutputPortModuleParameter(
                    name="output",
                    friendly_name="Result_dataset",
                    is_optional=False),
                ValueModuleParameter(
                    name="datastore_name",
                    friendly_name="Data Store Name",
                    data_type=str),
                ValueModuleParameter(
                    name="upload_path",
                    friendly_name="Upload Path",
                    data_type=str),
            ])
        module_nodes = [
            ModuleSpecNode.from_module_parameter(parameters["input"]),
            ModuleSpecNode.from_module_parameter(parameters["datastore_name"]),
            ModuleSpecNode.from_module_parameter(parameters["upload_path"]),
            ModuleSpecNode.from_module_parameter(parameters["output"]),
        ]
        conda_config_file = './azureml/designer/modules/datatransform/modules/conda_config/gen_test_data_module.yml'
        super().__init__(
            meta_data=meta_data,
            parameters=parameters,
            module_nodes=module_nodes,
            conda_config_file=conda_config_file)

    def run(self):
        input_path = self.parameters["input"]._value
        output_path = self.parameters["output"]._value
        datastore_name = self.parameters["datastore_name"].value
        upload_path = self.parameters["upload_path"].value
        logger.info(
            f"Copy from {input_path} to datastore: {datastore_name} on path {upload_path}")
        try:
            DoNothingModule.copy_anything(input_path, output_path)
        except Exception as ex:
            logger.info(f'{ex}')
            DoNothingModule.copy_anything(input_path, output_path)
        logger.info(f"Done Copy")
        from psutil import virtual_memory
        mem = virtual_memory()
        logger.info(f"total memory {mem.total/1024/1024.0/1024}G")

    @staticmethod
    def copy_anything(src, dst):
        try:
            shutil.copytree(src, dst)
        except OSError as exc:  # python >2.5
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
            else:
                raise

    def train(self):
        self.run()
