import pickle


def pickle(filename_or_variable: str | object, target_file: str | None = None):
    if not target_file and isinstance(filename_or_variable, str):
        return read_from_pickle(filename_or_variable)

    if target_file and isinstance(filename_or_variable, object):
        write_to_pickle(filename_or_variable, target_file)

    raise Exception("Wrong pickle helper inputs")


def write_to_pickle(data, filename):
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def read_from_pickle(filename):
    with open(filename, "rb") as f:
        data = pickle.load(f)
        return data
