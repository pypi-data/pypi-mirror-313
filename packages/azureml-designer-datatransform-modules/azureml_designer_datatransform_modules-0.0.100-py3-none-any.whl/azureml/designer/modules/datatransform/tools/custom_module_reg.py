# import os
# import sys
# import tempfile
# import uuid
# import json
# import argparse
# import re

# from git.repo import Repo

# from azureml.studio.common.utils.fileutil import ensure_folder, delete_folder from
# azureml.studio.common.utils.dictutils import get_value_by_key_path from azureml.studio.common.utils.yamlutils
# import load_yaml_file from azureml.studio.common.utils.dependencies import Dependencies from
# azureml.studio.common.attributes import BooleanParameter, IntParameter, FloatParameter, StringParameter,
# \ InputPort, DataTableInputPort, OutputPort, DataTableOutputPort, ILearnerOutputPort, ILearnerInputPort,
# ZipInputPort from azureml.studio.common.datatypes import DataTypes from azureml.core.conda_dependencies import
# CondaDependencies from azureml.studio.tool.module_registry import ServerConf, ModuleRegistry, WorkspaceRegistry


# EXIT_CODE_ERROR = 2


# def _load_yaml_module_spec(file_name, base_dir=None):
#     yaml_file_obj = load_yaml_file(file_name)  # type: dict

#     if type(yaml_file_obj) != dict:
#         raise Exception("Could not load yaml file as dict.")

#     def get_from_yaml(path):
#         return get_value_by_key_path(yaml_file_obj, path)

#     def convert_input_port(yaml_input_port):
#         name = yaml_input_port.get("name", None)
#         port_type = yaml_input_port.get("type", None)
#         desc = yaml_input_port.get("desc", None)
#         is_opt = yaml_input_port.get("optional", False)

# if not port_type: module_input_port = InputPort(data_type=any, allowed_data_types=[DataTypes.ANY], name=name,
# friendly_name=name, is_optional=is_opt, description=desc) elif port_type == "TabularDataFolder": module_input_port
# = DataTableInputPort(name=name, friendly_name=name, is_optional=is_opt, description=desc) elif port_type ==
# "GenericFolder": module_input_port = InputPort(data_type=any, allowed_data_types=[DataTypes.GENERIC_FOLDER],
# name=name, friendly_name=name, is_optional=is_opt, description=desc) elif port_type == "ModelFolder":
# module_input_port = ILearnerInputPort(name=name, friendly_name=name, is_optional=is_opt, description=desc) elif
# port_type == "GenericFile": raise ValueError(f"'GenericFile' is not supported yet.") elif port_type == "Zip":
# module_input_port = ZipInputPort(name=name, friendly_name=name, is_optional=is_opt, description=desc) else: raise
# ValueError(f"'{port_type}' is not a valid input port type.")

#         return module_input_port.to_dict()

#     def convert_output_port(yaml_output_port):
#         name = yaml_output_port.get("name", None)
#         port_type = yaml_output_port.get("type", None)
#         desc = yaml_output_port.get("desc", None)

#         if not port_type:
#             module_output_port = OutputPort(DataTypes.ANY, name=name, friendly_name=name, description=desc)
#         elif port_type == "TabularDataFolder":
#             module_output_port = DataTableOutputPort(name=name, friendly_name=name, description=desc)
#         elif port_type == "GenericFolder":
#             module_output_port = OutputPort(DataTypes.GENERIC_FOLDER, name=name, friendly_name=name, description=desc)
#         elif port_type == "ModelFolder":
#             module_output_port = ILearnerOutputPort(name=name, friendly_name=name, description=desc)
#         elif port_type == "GenericFile":
#             raise ValueError(f"'GenericFile' is not supported yet.")
#         else:
#             raise ValueError(f"'{port_type}' is not a valid output port type.")

#         return module_output_port.to_dict()

#     def convert_parameter(yaml_parameter):
#         name = yaml_parameter.get("name", None)
#         param_type = str.lower(yaml_parameter.get("type", None) or "")
#         desc = yaml_parameter.get("desc", None)
#         def_val = yaml_parameter.get("default", None)
#         is_opt = yaml_parameter.get("optional", False)

#         if not param_type:
#             print("Warning: Parameter type not provided, default as 'string'")
#             param_type = "string"

#         if param_type in ("int", "integer"):
#             param = IntParameter(name, name, is_optional=is_opt, description=desc, default_value=def_val)
#         elif param_type in ("str", "text", "string", ""):
#             param = StringParameter(name, name, is_optional=is_opt, description=desc, default_value=def_val)
#         elif param_type in ("float", "double"):
#             param = FloatParameter(name, name, is_optional=is_opt, description=desc, default_value=def_val)
#         elif param_type in ("bool", "boolean"):
#             param = BooleanParameter(name, name, is_optional=is_opt, description=desc, default_value=def_val)
#         elif param_type in ("mode", "enum"):
#             opts = yaml_parameter.get("options", None)
#             if not opts or type(opts) is not list:
#                 # raise ValueError(f"Mode parameter {name} has not any options.")
#                 if not def_val:
#                     def_val = "Default"

#                 mode_values_info = [
#                     (def_val, {
#                         "DisplayValue": def_val,
#                         "Parameters": []
#                     })
#                 ]
#             else:
#                 mode_values_info = []
#                 for yaml_opt in opts:
#                     if type(yaml_opt) == dict and len(yaml_opt) == 1:
#                         for k, v in yaml_opt.items():
#                             mode_values_info.append((k, {
#                                 "DisplayValue": k,
#                                 "Parameters": [convert_parameter(child) for child in v]
#                             }))
#                     elif type(yaml_opt) == str:
#                         mode_values_info.append((yaml_opt, {
#                             "DisplayValue": yaml_opt,
#                             "Parameters": []
#                         }))

#             mode_param = {
#                 "Name": name,
#                 "FriendlyName": name,
#                 "IsOptional": is_opt,
#                 "Description": desc,
#                 "DefaultValue": def_val,
#                 "ParameterType": "Mode",
#                 "HasDefaultValue": def_val is not None,
#                 "MarkupType": "Parameter",
#                 "ModeValuesInfo": dict(mode_values_info)
#             }
#             return mode_param

#         else:
#             raise ValueError(f"'{param_type}' is not a valid parameter type.")

#         return param.to_dict()

#     def convert_conda_dependency(yaml_conda):
#         if not yaml_conda:
#             return {}

#         if isinstance(yaml_conda, str):  # load as external file
#             yaml_base_dir = os.path.dirname(file_name)
#             if yaml_conda[0] == '/':
#                 yaml_base_dir = base_dir
#                 yaml_conda = yaml_conda[1:]

#             conda_decl_file = os.path.join(yaml_base_dir, yaml_conda) if yaml_base_dir else yaml_conda
#             conda_decl_file = os.path.abspath(conda_decl_file)
#             if base_dir and not conda_decl_file.startswith(base_dir):
#                 raise PermissionError(f"Conda reference file '{conda_decl_file}' is not under base directory.")

#             if not os.path.isfile(conda_decl_file):
#                 raise IOError(f"Conda reference file '{conda_decl_file}' not exists.")

#             yaml_conda = load_yaml_file(conda_decl_file)

#         aml_conda_dep = CondaDependencies(_underlying_structure=yaml_conda)
#         dep = Dependencies(aml_conda_dep)
#         return dep.to_dict()

#     def convert_meta_parameters(yaml_meta):
#         if not yaml_meta:
#             return {}

#         return {
#             "BaseDockerImage": yaml_meta.get("baseDockerImage", None),
#             "GpuSupport": yaml_meta.get("gpuSupport", None)
#         }

#     def convert_module_entry(yaml_invoking):
#         if not yaml_invoking:
#             return {}

#         return {
#             "ModuleName": yaml_invoking.get("module", None),
#             "ClassName": yaml_invoking.get("class", None),
#             "MethodName": yaml_invoking.get("func", None),
#         }

#     def convert_commandline_entry(yaml_command, yaml_args):
#         command = yaml_command if isinstance(yaml_command, list) else []
#         option_names = {}

#         if isinstance(yaml_args, list):
#             args_obj = []
#             arg_name = None
#             for i, v in enumerate(yaml_args):
#                 if isinstance(v, str):
#                     if arg_name:
#                         print(f"Warning: parsed '{arg_name}' as fixed command argument.")
#                         command.append(arg_name)  # fixed argument
#                     arg_name = v
#                 elif isinstance(v, dict) and v:
#                     port_name = list(v.values())[0]
#                     if not arg_name:
#                         raise ValueError(f"Error: no argname for command line argument '{port_name}'.")
#                     args_obj.append((port_name, arg_name))
#                     arg_name = None
#             if arg_name:
#                 print(f"Warning: parsed '{arg_name}' as fixed command argument.")
#                 command.append(arg_name)  # the last fixed argument
#             option_names = dict(args_obj)

#         return {
#             "Command": command,
#             "OptionNames": option_names
#         }

#     module_name = get_from_yaml("name")
#     family_id = get_from_yaml("id")
#     inputs = get_from_yaml("inputs") or []
#     outputs = get_from_yaml("outputs") or []

#     # build module spec
#     module_spec = {
#         "Name": module_name,
#         "FriendlyName": module_name,
#         "FamilyId": family_id,
#         "Category": get_from_yaml("category"),
#         "Description": get_from_yaml("description"),
#         "Version": "1",
#         "Owner": get_from_yaml("owner") or "Custom Module Registry",
#         "ReleaseState": "Release",
#         "IsDeterministic": True,
#         "CondaDependencies": convert_conda_dependency(get_from_yaml("implementation/container/conda")),
#         "ModuleMetaParameters": convert_meta_parameters(get_from_yaml("implementation/container/runConfig")),
#         "ModuleEntry": convert_module_entry(get_from_yaml("implementation/invoking")),
#         "CommandLineEntry": convert_commandline_entry(
#             yaml_command=get_from_yaml("implementation/container/command"),
#             yaml_args=get_from_yaml("implementation/container/args")
#         ),
#         "ModuleInterface": {
#             "InputPorts": [convert_input_port(o) for o in inputs if o.get("port", False)],
#             "OutputPorts": [convert_output_port(o) for o in outputs],
#             "Parameters": [convert_parameter(o) for o in inputs if not o.get("port", False)],
#         }
#     }

#     if get_from_yaml("isDeprecated") is True:
#         print(f"Warning: Will delete module '{module_name}'({family_id}).")
#         module_spec["IsDeprecated"] = True

#     return module_spec


# def _validate_module_spec(module_spec):
#     # TODO: we need json schema or manually check all necessary fields.
#     return True


# def _lock_pip_package_commit_version(module_spec, repo_store=None):
#     pip_packages = get_value_by_key_path(module_spec, "CondaDependencies/PipPackages")
#     re_pip_vcs = re.compile(r'^git\+(?P<url>[^@#]+?)(@(?P<branch>.+?))?(?P<args>#(.+?=[^&]+)(&(.+?=[^&]+))*)?$')
#     repo_store = repo_store or _GitRepositories()

#     if not pip_packages or type(pip_packages) != list:
#         return

#     for i, v in enumerate(pip_packages):
#         match = re_pip_vcs.match(v)
#         if match:  # pip package from vcs
#             git_url = match.group('url')
#             branch_or_tag = match.group('branch') or 'master'
#             commit_hash = repo_store.get_remote_commit_hash(git_url, branch_or_tag)
#             if commit_hash:
#                 pip_pkg_ver_locked = str.join('', [
#                     'git+',
#                     git_url,
#                     '@',
#                     commit_hash,
#                     match.group('args') or ''
#                 ])
#                 print(f"Replace pip package '{v}' to '{pip_pkg_ver_locked}'")
#                 pip_packages[i] = pip_pkg_ver_locked


# def _register_modules(modules, conf_name, workspace_id, cert_file):
#     if uuid.UUID(ServerConf.GLOBAL_WORKSPACE_ID) == uuid.UUID(workspace_id):
#         raise Exception("Attempting to register custom module to global workspace.")

#     conf = ServerConf(
#         name=conf_name,
#         workspace_id=workspace_id
#     )
#     module_reg = ModuleRegistry(conf.url, workspace_id=workspace_id, cert_file=cert_file)
#     module_spec_compat = [ModuleSpecCompat(m) for m in modules]
#     print("Get latest BatchID...")
#     latest_batch_id = module_reg.get_latest_batch_id()
#     print(f"Latest BatchID is {latest_batch_id}")
#     reg_batch_id = latest_batch_id + 1
#     print(f"Registering {len(modules)} modules to Batch {reg_batch_id}")
#     module_reg.add_batch(reg_batch_id, module_spec_compat)
#     print(f"Active Batch {reg_batch_id}")
#     module_reg.activate_batch(reg_batch_id)
#     print(f"Register complete.")


# class ModuleSpecCompat:
#     def __init__(self, module_spec_obj):
#         self._ux_contract_dict = module_spec_obj

#     @property
#     def ux_contract_dict(self):
#         return self._ux_contract_dict


# class _GitRepoReferences:
#     def __init__(self):
#         self.heads = {}
#         self.tags = {}

#     def get_hash(self, branch_or_tag):
# return self.heads.get(branch_or_tag, None) or
# self.heads.get(branch_or_tag, None)


# class _GitRepositories:
#     re_git_ref = re.compile(r'^([0-9A-Fa-f]{40})\s+refs/(heads|tags)/(.+)$')

#     def __init__(self):
#         self._repos = {}

#     def get_remote_commit_hash(self, git_url, branch_or_tag, reload=False):
#         repo_refs = self._get_repo_refs(git_url, reload=reload)
#         return repo_refs.get_hash(branch_or_tag)

#     def git_has_branch(self, git_url, branch, reload=False):
#         repo_refs = self._get_repo_refs(git_url, reload=reload)
#         return branch in repo_refs.heads

#     def _get_repo_refs(self, git_url, reload=False):
#         repo_refs = None

#         if not reload:
#             repo_refs = self._repos.get(git_url, None)

#         if not repo_refs:
#             repo_refs = self._git_ls_remote(git_url)
#             self._repos[git_url] = repo_refs

#         return repo_refs

#     @classmethod
#     def _git_ls_remote(cls, git_url):
#         temp_dir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
#         repo_refs = _GitRepoReferences()

#         try:
#             temp_repo = Repo.init(path=temp_dir, mkdir=True)
#             temp_repo.create_remote('origin', git_url)
#             ls_remote_result = temp_repo.git.ls_remote('--heads', '--tags')
#             for row in ls_remote_result.split('\n'):
#                 match = cls.re_git_ref.match(row)
#                 if match:
#                     commit_hash, ref_type, branch_or_tag = match.groups()
#                     getattr(repo_refs, ref_type)[branch_or_tag] = commit_hash

#         finally:
#             delete_folder(temp_dir, force=True)

#         return repo_refs

#     @classmethod
# def git_clone(cls, git_url, clone_dir, branch_or_tag=None,
# commit_hash=None):

#         ensure_folder(clone_dir)

#         def print_progress(op_code, cur_count, max_count=None, message=''):
#             print(f"git({op_code}): {cur_count}/{max_count}, {message}")

#         if commit_hash:
#             if branch_or_tag:
#                 clone_repo = Repo.clone_from(git_url, clone_dir, progress=print_progress, branch=branch_or_tag)
#             else:
#                 clone_repo = Repo.clone_from(git_url, clone_dir, progress=print_progress)
#             clone_repo.head.reset(commit=commit_hash, index=True)
#         elif branch_or_tag:
#             clone_repo = Repo.clone_from(git_url, clone_dir, progress=print_progress, branch=branch_or_tag, depth=1)
#         else:
#             clone_repo = Repo.clone_from(git_url, clone_dir, progress=print_progress, depth=1)

#         return clone_repo


# def _register_custom_module(git_url=None, branch_or_tag=None, commit_hash=None, spec_file_name=None, pip_lock=False,
#                             workspace_id=None, resource_id=None, cert_file=None, conf=None, clean=True):
#     temp_dir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
#     repo_store = _GitRepositories()

#     if git_url and not branch_or_tag and not commit_hash and not spec_file_name:
#         print(f"Detecting yaml file path")
#         re_github_tree_url = re.compile(r'^(https://github.com/[\w\-.]+/[\w\-.]+)/tree/([\w\-.]+)(/(.*))?$')
#         match = re_github_tree_url.match(git_url)
#         if match:
#             git_url, branch_or_tag, spec_file_name = match.group(1) + ".git", match.group(2), match.group(4)
#             if spec_file_name:
#                 spec_file_name += "/*.yaml"
#             else:
#                 spec_file_name = "*.yaml"
#         else:
#             re_github_file_url = re.compile(r'^(https://github.com/[\w\-.]+/[\w\-.]+)/blob/([\w\-.]+)/(.*\.yaml)$')
#             match = re_github_file_url.match(git_url)
#             if match:
#                 git_url, branch_or_tag, spec_file_name = match.group(1) + ".git", match.group(2), match.group(3)

#         if branch_or_tag and spec_file_name:
#             if not repo_store.git_has_branch(git_url, branch=branch_or_tag):
#                 # split branch name if branch name contains '/'
#                 real_branch = branch_or_tag
#                 real_spec_file_name = spec_file_name
#                 while '/' in real_spec_file_name:
#                     index = real_spec_file_name.find('/')
#                     real_branch += '/' + real_spec_file_name[:index]
#                     real_spec_file_name = real_spec_file_name[index + 1:]

#                     if repo_store.git_has_branch(git_url, branch=real_branch):
#                         branch_or_tag = real_branch
#                         spec_file_name = real_spec_file_name
#                         break

#             if Repo.re_hexsha_only.match(branch_or_tag):
#                 commit_hash = branch_or_tag
#                 branch_or_tag = None

#             print(f'  git-url: {git_url}')
#             print(f'  branch: {branch_or_tag}')
#             print(f'  commit_hash: {commit_hash}')
#             print(f'  spec_file_name: {spec_file_name}')

#     try:
#         print(f"Clone to local directory: {temp_dir}")
#         repo_store.git_clone(git_url, temp_dir, branch_or_tag=branch_or_tag, commit_hash=commit_hash)
#         has_failed = False
#         all_loaded_modules = []

#         def load_module_spec(file_path):
#             nonlocal has_failed
#             try:
#                 module_spec = _load_yaml_module_spec(file_path, base_dir=temp_dir)
#                 if pip_lock:
#                     print("  lock pip package version...")
#                     _lock_pip_package_commit_version(module_spec, repo_store)
#                 print(json.dumps(module_spec))
#                 all_loaded_modules.append(module_spec)
#                 has_failed |= not _validate_module_spec(module_spec)
#             except Exception as ex:
#                 has_failed = True
#                 print(f"Load spec error: {ex}")

#         if spec_file_name and '*' not in spec_file_name:
#             print(f"Load spec file: {spec_file_name}")
#             load_module_spec(os.path.join(temp_dir, spec_file_name))

#         else:
#             search_pattern = spec_file_name or '*.yaml'
#             print(f"Search spec file '{search_pattern}'...")
#             import pathlib
#             for spec_file_path in pathlib.Path(temp_dir).rglob(search_pattern):
#                 print(f"Load spec file: {spec_file_path.relative_to(temp_dir)}")
#                 load_module_spec(str(spec_file_path))

#         if has_failed:
#             print(f"Not all yaml files load successfully, please check error logs.")
#             exit(EXIT_CODE_ERROR)

#         # convert Azure resource id to workspace id.
#         if not workspace_id and resource_id:
#             pat = r'/subscriptions/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})' \
#                   r'/resourceGroups/([^/]+)/providers/Microsoft\.MachineLearningServices/workspaces/([^/]+)'

#             match = re.search(pat, resource_id)
#             if not match:
#                 print(f"Invalid workspace resource id format.")
#                 exit(EXIT_CODE_ERROR)

#             subscription_id, resource_group, workspace_name = match.group(1), match.group(2), match.group(3),

# print(f"Get workspaceID of workspace {workspace_name}") server_conf = ServerConf(conf) ws_reg = WorkspaceRegistry(
# server_conf.url, subscription_id=subscription_id, resource_group=resource_group, workspace_name=workspace_name,
# cert_file=cert_file) workspace_id = ws_reg.get_workspace_id()

#             if not workspace_id:
#                 print(f"Get workspaceID failed.")
#                 exit(EXIT_CODE_ERROR)

#         if workspace_id:
#             print(f"Registering modules to workspace {workspace_id}")
#             _register_modules(all_loaded_modules, conf, workspace_id, cert_file)

#     except Exception as err:
#         print(f"Unexpected error: {err}")
#         raise

#     finally:
#         if clean:
#             delete_folder(temp_dir, force=True)


# # this function is mucked as a entry point from a pip package,
# # which requires to contain no arguments
# # https://stackoverflow.com/a/2853939
# def main():
#     parser = argparse.ArgumentParser(
#         prog="python custom_module_reg.py",
#         formatter_class=argparse.RawDescriptionHelpFormatter,
#         description="""A CLI tool to register custom modules.

# eg:
# dry-run:
#   custom_module_reg https://github.com/USER/REPO.git --branch BRANCH --spec-file "PATH/TO/SPEC.yaml"
#   custom_module_reg https://github.com/USER/REPO.git --branch BRANCH --spec-file "PATH/DIR/*.yaml"
#   custom_module_reg https://github.com/USER/REPO/blob/BRANCH/PATH/TO/SPEC.yaml
#   custom_module_reg https://github.com/USER/REPO/tree/BRANCH/PATH/DIR

# register to workspace:
#   custom_module_reg SPEC_FILE_ARGS --workspace-id "WORKSPACE_ID" --conf int --cert "CERT_FILE"
# """,
#     )

#     parser.add_argument(
#         'git-url', type=str,
#         help="A public accessible git url. Also support github blob and tree url."
#     )
#     parser.add_argument(
#         '--branch', type=str,
#         help="Clone from specific branch name or tag name."
#     )
#     parser.add_argument(
#         '--commit', type=str,
#         help="Clone from specific commit hash."
#     )
#     parser.add_argument(
#         '--spec-file', type=str,
#         help="Path of the spec yaml file relative to the git repository root,"
#              "support wildcard char(eg: path/to/spec/*.yaml). "
#              "If not provided, it will recursively search for all .yaml extension files."
#     )
#     parser.add_argument(
#         '--pip-lock', action="store_true",
#         help="If set, all pip dependencies from git will force set version to current latest commit."
#     )
#     parser.add_argument(
#         '--workspace-id', type=str,
#         help="If provided, the custom modules will register to the workspace."
#     )
#     parser.add_argument(
#         '--workspace-resource-id', type=str,
#         help="Azure resource identifier url, format is "
#              "'/subscriptions/<subscriptionId>/resourceGroups/<resourceGroupName>"
#              "/providers/Microsoft.MachineLearningServices/workspaces/<workspaceName>'."
#     )
#     parser.add_argument(
#         '--conf', type=str, default="int",
#         help="Server config name. default is 'int'."
#     )
#     parser.add_argument(
#         '--cert', type=str,
#         help="Client credential cert file for SMT Admin api."
#     )
#     parser.add_argument(
#         '--clean', action="store_true",
#         help="Clean up all downloaded files after execution."
#     )

#     args, _ = parser.parse_known_args(sys.argv[1:])

#     _register_custom_module(
#         git_url=getattr(args, 'git-url'),
#         branch_or_tag=args.branch,
#         commit_hash=args.commit,
#         spec_file_name=args.spec_file,
#         pip_lock=args.pip_lock,
#         workspace_id=args.workspace_id,
#         resource_id=args.workspace_resource_id,
#         conf=args.conf,
#         cert_file=args.cert,
#         clean=args.clean
#     )


# if __name__ == '__main__':
#     main()
