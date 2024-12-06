import os

import lazy_loader as lazy

submodules = [
    "events",
    "states",
    "utils",
    "stimuli",
]

__getattr__, __dir__, __all__ = lazy.attach_stub(
    __name__,
    f"{os.path.dirname(__file__)}/stubs/__init__.pyi",
)
