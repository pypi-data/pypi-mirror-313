from azureml.designer.modules.datatransform.common.module_parameter import ModuleParameterBase, IOPortModuleParameter, \
    ScriptModuleParameter, ColumnSelectorModuleParameter
from enum import Enum
from azureml.studio.core.utils.column_selection import ColumnSelectionBuilder, ColumnType
from azureml.designer.modules.datatransform.tools.column_selection_utils import convert_column_selection_to_json


class ModuleSpecNode:
    Mode = "Mode"
    Script = "Script"
    ColumnPicker = "ColumnPicker"
    DataFrameDirectory = "DataFrameDirectory"

    def __init__(
            self,
            name,
            friendly_name=None,
            description=None,
            module_parameter: ModuleParameterBase = None,
            is_optional=False,
            parent_node: 'ModuleSpecNode' = None,
            options: list = None):
        if module_parameter is None:
            raise ValueError("module_parameter should not be None")
        self._name = name
        self._friendly_name = friendly_name if friendly_name else module_parameter.friendly_name
        self._description = description if description else name
        self._module_parameter = module_parameter
        self._dependencies = None
        self._children = []
        self.add_parent(parent_node, options)
        self._is_optional = is_optional

    @staticmethod
    def from_module_parameter(
            module_parameter: ModuleParameterBase,
            is_optional=False,
            parent_node: 'ModuleSpecNode' = None,
            options: list = None) -> 'ModuleSpecNode':
        return ModuleSpecNode(
            name=module_parameter.name,
            friendly_name=module_parameter.friendly_name,
            description=module_parameter.description,
            module_parameter=module_parameter,
            is_optional=is_optional,
            parent_node=parent_node,
            options=options)

    @property
    def name(self):
        return self._name if not isinstance(
            self._module_parameter,
            IOPortModuleParameter) else self._friendly_name

    @property
    def label(self):
        return self._friendly_name if self._friendly_name != self._name and not isinstance(
            self._module_parameter, IOPortModuleParameter) else None

    @property
    def optional(self):
        return True if self._is_optional else None

    @property
    def type(self):
        para_data_type = self._module_parameter.data_type
        if issubclass(para_data_type, Enum):
            return ModuleSpecNode.Mode
        if isinstance(self._module_parameter, ScriptModuleParameter):
            return ModuleSpecNode.Script
        if isinstance(self._module_parameter, ColumnSelectorModuleParameter):
            return ModuleSpecNode.ColumnPicker
        if isinstance(self._module_parameter, IOPortModuleParameter):
            return ModuleSpecNode.DataFrameDirectory
        if self._module_parameter.data_type is bool:
            return "Boolean"
        if self._module_parameter.data_type is str:
            return "String"
        return para_data_type.__name__.capitalize()

    @property
    def port(self):
        return True if isinstance(
            self._module_parameter,
            IOPortModuleParameter) else False

    @property
    def columnPickerFor(self):
        if isinstance(self._module_parameter, ColumnSelectorModuleParameter):
            port_parameter = self._module_parameter.input_port
            # port parameter & port node must be 1:1 mapping & should share the same name & description
            # TODO: add validation.
            # TODO: might need to change to description. Need to confirm with
            # studio team
            return port_parameter._friendly_name
        return None

    @property
    def language(self):
        if isinstance(self._module_parameter, ScriptModuleParameter):
            return self._module_parameter.language
        return None

    @property
    def singleColumnSelection(self):
        # if isinstance(self._module_parameter, ColumnSelectorModuleParameter):
        #     # TODO: need to add single_column_selection in column picker parameter
        #     return True
        # return None
        return None

    @property
    def default(self):
        if isinstance(self._module_parameter, ColumnSelectorModuleParameter):
            if self._module_parameter.default_value == convert_column_selection_to_json(
                    ColumnSelectionBuilder().include_col_types(ColumnType.NUMERIC)):
                return "NumericAll"
            if self._module_parameter.default_value == convert_column_selection_to_json(
                    ColumnSelectionBuilder().include_all()):
                return "All"
        return self._module_parameter.default_value

    @property
    def options(self):
        options_key = []
        options_dict = {}
        if issubclass(self._module_parameter.data_type, Enum):
            options_key = list(self._module_parameter.data_type)
            if self._children:
                for child in self._children:
                    if child._parent_options:
                        for option in child._parent_options:
                            if option in options_dict:
                                options_dict[option].append(child)
                            else:
                                options_dict[option] = [child]
        return None if not options_key else [{option_key: options_dict[option_key]}
                                             if option_key in options_dict else option_key for option_key in
                                             options_key]

    def get_nodes(self, module_parameter: ModuleParameterBase):
        nodes = []
        if self._module_parameter == module_parameter:
            nodes.append(self)
        for child in self._children:
            nodes.extend(child.get_nodes(module_parameter))
        return nodes

    def add_parent(self, parent_node: 'ModuleSpecNode', options: list):
        if parent_node is not None:
            if options:
                for option in options:
                    if not isinstance(option,
                                      parent_node._module_parameter.data_type):
                        raise Exception(
                            f"Not valid dependency. '{option}' not in type '{parent_node._module_parameter.data_type}'")
            if self not in parent_node._children:
                parent_node._children.append(self)
        self._parent_node = parent_node
        self._parent_options = options

    def get_args(self):
        # due to io port can not support label and IO port is unique. argname
        # come from parameter name, arg value from friendly name
        arg_key = self._name.replace("_", "-")  # for module code use
        arg_value = self.name  # for spec parameter use
        args = {
            "--" +
            arg_key: {
                self._module_parameter.parameter_type: arg_value}}
        for child in self._children:
            args.update(child.get_args())
        return args

    def get_all_nodes(self):
        nodes = [self]
        for child in self._children:
            nodes.extend(child.get_all_nodes())
        return nodes
