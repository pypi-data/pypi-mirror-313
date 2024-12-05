
from azureml.designer.modules.datatransform.common.module_collection import get_all_modules_name, \
    construct_module_by_name
from azureml.studio.core.io.data_frame_directory import DataFrameDirectory
from azureml.studio.internal.error_handler import error_handler
import pandas as pd


class InferenceEntry():
    def __init__(self, params: dict):
        # dynamically construct module function
        for module_name in get_all_modules_name():
            module = ModuleWrapper(module_name, params)
            setattr(self, module_name, module.run)


class ModuleWrapper():
    def __init__(self, module_name: str, params: dict = None):
        self._module_name = module_name
        self._params = params

    @error_handler
    def run(self, *args):
        ports = []
        params = {}

        for arg in args:
            if isinstance(
                    arg, DataFrameDirectory) or isinstance(
                    arg, pd.DataFrame) or arg is None:
                ports.append(arg)
            else:
                params = arg
                break
        transform_module = construct_module_by_name(self._module_name)
        return transform_module.run_with_inference_params(
            ports, self._params, params)
