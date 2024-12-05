from azureml.designer.modules.datatransform.common.yaml_spec import YamlSpec
from azureml.designer.modules.datatransform.common.module_collection import get_all_modules
from azureml.designer.modules.datatransform.tools.object_utils import convert_to_native_object
from ruamel.yaml import ruamel
import os
import inspect


def main():
    modules = get_all_modules()
    for module in modules:
        print(f"generate yaml for {module.__class__}")
        yaml_data = YamlSpec(module)
        yaml_plain = convert_to_native_object(yaml_data)
        spec_path = os.path.join(os.path.dirname(__file__), "../yaml_spec/")
        module_file_name = inspect.getfile(module.__class__)
        with open(os.path.join(spec_path, f'{os.path.basename(module_file_name).split(".")[0]}.yaml'), 'w') as outfile:
            ruamel.yaml.round_trip_dump(yaml_plain, outfile)


if __name__ == "__main__":
    main()
