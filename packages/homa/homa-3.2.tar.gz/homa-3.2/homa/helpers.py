import pickle as pickle_object
import torch


def flush(*args, **kwargs):
    kwargs["flush"] = True
    print(*args, **kwargs)


def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def pickle(
    filename_or_variable: str | object, target_file: str | None = None
) -> object | None:
    if not target_file and isinstance(filename_or_variable, str):
        return read_from_pickle(filename_or_variable)

    if target_file and isinstance(filename_or_variable, object):
        write_to_pickle(filename_or_variable, target_file)
        return

    raise Exception("Wrong pickle helper inputs")


def write_to_pickle(data, filename):
    with open(filename, "wb") as f:
        pickle_object.dump(data, f)


def read_from_pickle(filename):
    with open(filename, "rb") as f:
        return pickle_object.load(f)
