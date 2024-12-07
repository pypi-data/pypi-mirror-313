import importlib as _importlib

_TOP_LEVEL_IMPORTS = {"get_input": "union_runtime._lib.inputs"}

__all__ = list(_TOP_LEVEL_IMPORTS)


def __getattr__(name):
    if name in _TOP_LEVEL_IMPORTS:
        module = _importlib.import_module(_TOP_LEVEL_IMPORTS[name])
        return getattr(module, name)
    else:
        try:
            return globals()[name]
        except KeyError:
            raise AttributeError(f"Module 'union_runtime' has no attribute '{name}'")
