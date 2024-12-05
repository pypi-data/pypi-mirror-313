from azureml.designer.modules.datatransform.common.module_base import ModuleBase
from typing import List
from azureml.designer.modules.datatransform import __version__, __yamlversion__, __packagename__


class YamlSpec:
    def __init__(self, module: ModuleBase):
        self._module = module
        self._inputs = module.inputs
        self._outputs = module.outputs
        self._implementation = Implementation(module)

    @property
    def name(self):
        return self._module.meta_data.name

    @property
    def id(self):
        return self._module.meta_data.id

    @property
    def version(self):
        return __yamlversion__

    @property
    def category(self):
        return self._module.meta_data.category

    @property
    def description(self):
        return self._module.meta_data.description

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @property
    def implementation(self):
        return self._implementation


class Implementation():
    _REQUIRED_MODULES = [
        f'{__packagename__}=={__version__}',
    ]

    def __init__(self, module: ModuleBase):
        self._conda = self._get_conda(module.conda_config_file)
        self._runconfig = RunConfig(module)
        args = [item for key, value in module.get_args().items()
                for item in [key, value]]
        self._args = args
        self._module = module

    @property
    def container(self):
        result = {
            "conda": self._conda,
            "command": [
                "python",
                "-m",
                "azureml.designer.modules.datatransform.invoker",
                self._module.__class__.__name__],
            "args": self._args,
            "runConfig": self._runconfig}
        return result

    @property
    def invoking(self):
        return {
            "module": "azureml.designer.modules.datatransform.inference_entry",
            "class": "InferenceEntry",
            "func": type(self._module).__name__
        }

    def _get_conda(self, path: str):
        from ruamel.yaml import ruamel
        with open(path, 'r') as stream:
            obj = ruamel.yaml.safe_load(stream)
            obj = self._insert_pip_packages(
                obj, Implementation._REQUIRED_MODULES)
        return obj

    def _insert_pip_packages(self, conda_obj, pips: List[str]):
        pip = [item for item in conda_obj["dependencies"]
               if isinstance(item, dict) and "pip" in item]
        if not pip:
            pip_item = {'pip': []}
            conda_obj["dependencies"].append(pip_item)
            pip = [pip_item]
        pip[0]['pip'].extend(pips)
        return conda_obj


class RunConfig():
    def __init__(self, module: ModuleBase):
        pass

    @property
    def baseDockerImage(self):
        return "mcr.microsoft.com/azureml/base:intelmpi2018.3-ubuntu16.04"

    @property
    def gpuSupport(self):
        return False
