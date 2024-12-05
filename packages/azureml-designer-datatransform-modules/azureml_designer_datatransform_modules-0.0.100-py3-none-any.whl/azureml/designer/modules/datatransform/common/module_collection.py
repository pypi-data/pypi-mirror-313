from typing import List
import importlib
import re
from azureml.designer.modules.datatransform.common.module_base import ModuleBase


def get_all_modules() -> List[ModuleBase]:
    return [construct_module_by_name(module_name)
            for module_name in get_all_modules_name()]


def get_all_modules_name() -> List[str]:
    return [
        'ApplyMathModule',
        'ApplySqlTransModule',
        'ClipValuesModule',
        'SummarizeDataModule'
    ]


def construct_module_by_name(module_name: str) -> ModuleBase:
    split_class_name = re.findall('[A-Z][^A-Z]*', module_name)
    module_file_name = '_'.join(split_class_name).lower()
    module_namespace = 'azureml.designer.modules.datatransform.modules.' + module_file_name
    module = importlib.import_module(module_namespace, module_name)
    module_class = getattr(module, module_name)
    return module_class()
