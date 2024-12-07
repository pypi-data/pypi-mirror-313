__all__ = [
    "benchmark",
    "codecs",
    "compressor",
    "dataset",
    "metrics",
    "model",
]

import inspect as _inspect
import sys as _sys

# fix-up submodule imports for the _fcbench extension module
from . import _fcbench

_modules = [
    ("fcbench._fcbench", _fcbench, _name, _module)
    for _name, _module in _inspect.getmembers(_fcbench)
    if _inspect.ismodule(_module)
]
while len(_modules) > 0:
    _parent_path, _parent, _name, _module = _modules.pop()
    _module_path = f"{_parent_path}.{_name}"
    _sys.modules[_module_path] = getattr(_parent, _name)
    for _child_name, _child in _inspect.getmembers(_module):
        if _inspect.ismodule(_child):
            _modules.append((_module_path, _module, _child_name, _child))

from . import (  # noqa: E402
    benchmark,
    codecs,
    compressor,
    dataset,
    metrics,
    model,
)

# polyfill for fcpy imports
_sys.modules["fcpy"] = _sys.modules[__name__]
