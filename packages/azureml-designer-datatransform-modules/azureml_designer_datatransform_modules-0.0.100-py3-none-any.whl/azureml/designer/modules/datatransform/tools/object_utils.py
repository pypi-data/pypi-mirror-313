from enum import Enum


def convert_to_native_object(obj):
    if isinstance(obj, list):
        return [convert_to_native_object(item) for item in obj]
    if isinstance(obj, Enum):
        return obj.value
    if type(obj) in [str, float, int, bool]:
        return obj
    if isinstance(obj, tuple):
        return tuple(convert_to_native_object(item) for item in obj)
    if isinstance(obj, dict):
        return {convert_to_native_object(key): convert_to_native_object(
            value) for key, value in obj.items()}
    result = {}
    for name, value in vars(type(obj)).items():
        if isinstance(value, property):
            value = value.fget(obj)
            if value is None:
                continue
            result[name] = convert_to_native_object(value)
    return result
