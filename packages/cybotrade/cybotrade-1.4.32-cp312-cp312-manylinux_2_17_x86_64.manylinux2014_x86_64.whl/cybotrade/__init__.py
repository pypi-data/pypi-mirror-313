# import the contents of the Rust library into the Python extension
# optional: include the documentation from the Rust module
from .cybotrade import *
from .cybotrade import __all__, __doc__

# This is for adding exports from Python
__all__ = __all__ + ["PythonClass"]


class PythonClass:
    def __init__(self, value: int) -> None:
        self.value = value
