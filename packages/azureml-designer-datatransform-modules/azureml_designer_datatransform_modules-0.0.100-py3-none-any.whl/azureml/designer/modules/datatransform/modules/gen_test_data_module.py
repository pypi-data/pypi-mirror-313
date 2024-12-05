# import pandas as pd
# from azureml.designer.modules.datatransform.common.module_base import ModuleBase
# from azureml.designer.modules.datatransform.common.module_meta_data import ModuleMetaData
# from azureml.designer.modules.datatransform.common.module_parameter import InputPortModuleParameter, \
#     OutputPortModuleParameter, ScriptModuleParameter, ModuleParameters
# from azureml.designer.modules.datatransform.common.module_spec_node import ModuleSpecNode
# from io import StringIO
# from azureml.designer.modules.datatransform.common.logger import custom_module_logger as logger
# from azureml.designer.modules.datatransform.common.logger import format_obj

# class GenTestDataModule(ModuleBase):
#     def __init__(self):
#         meta_data = ModuleMetaData(
#             id="5ee98d28-16f4-47c8-a3de-15cc12f7242f",
#             name="Generate Test Data",
#             category="Data Input and Output",
#             description="")
#         parameters = ModuleParameters([
#             OutputPortModuleParameter(name="dataset", friendly_name="Result_dataset", is_optional=False),
#             ScriptModuleParameter(name="csv", friendly_name="Input CSV", is_optional=False)
#         ])
#         module_nodes= [
#             ModuleSpecNode.from_module_parameter(parameters["dataset"]),
#             ModuleSpecNode.from_module_parameter(parameters["csv"]),
#         ]
#         conda_config_file = './azureml/designer/modules/datatransform/modules/conda_config/gen_test_data_module.yml'
#         super().__init__(meta_data=meta_data, parameters=parameters, module_nodes=module_nodes,
#                          conda_config_file=conda_config_file)

#     def run(self):
#         csv = self.parameters["csv"].value
#         data = pd.read_csv(StringIO(csv))
#         self._handle_output("dataset",data)
