import os

def get_ROOT_PATH( layers, file ):
    """add sys path
    sys.path.insert(0, _ROOT_PATH)
    """
    _ROOT_PATH = os.path.abspath(file)
    for _ in range(layers):
        _ROOT_PATH = os.path.dirname(_ROOT_PATH)
    return _ROOT_PATH