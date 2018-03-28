import json
from importlib import import_module
from .constants import LIBRARIES_FILE


with open(LIBRARIES_FILE) as f:
    LIBS = json.load(f)


import_cache = {}


def get_result(algorithm, seq1, seq2):
    if algorithm not in import_cache:
        variants = LIBS[algorithm]
        for path in variants:
            module_name, _, func_name = path.rpartition('.')
            try:
                module = import_module(module_name)
            except ImportError:
                continue
            import_cache[algorithm] = getattr(module, func_name)
            break
        else:
            import_cache[algorithm] = None

    func = import_cache[algorithm]
    if func:
        return func(seq1, seq2)