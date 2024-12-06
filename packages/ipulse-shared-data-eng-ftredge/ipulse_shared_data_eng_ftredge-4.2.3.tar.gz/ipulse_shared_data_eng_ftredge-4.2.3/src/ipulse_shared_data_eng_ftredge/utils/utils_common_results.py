from types import SimpleNamespace

def result_nmspc_to_dict(obj):
    if isinstance(obj, SimpleNamespace):
        return {key: result_nmspc_to_dict(value) for key, value in vars(obj).items()}
    elif isinstance(obj, dict):
        return {key: result_nmspc_to_dict(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple, set)):
        return type(obj)(result_nmspc_to_dict(item) for item in obj)
    else:
        return obj