from azureml.studio.core.utils.column_selection import ColumnSelection
import json


def convert_column_selection_to_json(column_selection: ColumnSelection):
    return json.dumps(column_selection._obj)
