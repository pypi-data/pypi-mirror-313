from azureml.designer.modules.datatransform.common.module_base import ModuleBase
from azureml.designer.modules.datatransform.common.module_meta_data import ModuleMetaData
from azureml.designer.modules.datatransform.common.module_parameter import InputPortModuleParameter, \
    ValueModuleParameter, ModuleParameters
from azureml.designer.modules.datatransform.common.module_spec_node import ModuleSpecNode
import time


class WaitingModule(ModuleBase):
    def __init__(self):
        meta_data = ModuleMetaData(
            id="dad8d93e-86d6-4172-a660-f202dcd414bb",
            name="Waiting",
            category="Internal",
            description="Waiting")
        parameters = ModuleParameters(
            [
                InputPortModuleParameter(
                    name="input",
                    friendly_name="Input",
                    is_optional=False),
                ValueModuleParameter(
                    name="waiting_time",
                    friendly_name="Waiting time in second",
                    data_type=int),
            ])
        module_nodes = [
            ModuleSpecNode.from_module_parameter(parameters["input"]),
            ModuleSpecNode.from_module_parameter(parameters["waiting_time"]),
        ]
        conda_config_file = './azureml/designer/modules/datatransform/modules/conda_config/gen_test_data_module.yml'
        super().__init__(
            meta_data=meta_data,
            parameters=parameters,
            module_nodes=module_nodes,
            conda_config_file=conda_config_file)

    def run(self):
        time.sleep(self.parameters['waiting_time'].value)

    def train(self):
        self.run()
