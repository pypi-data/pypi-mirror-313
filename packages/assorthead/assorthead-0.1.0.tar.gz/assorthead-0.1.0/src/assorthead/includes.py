import inspect
import os
from typing import List


def includes() -> str:
    """Provides access to assorted C++ headers for downstream packages.

    Returns:
        str: Path to a directory containing lots of header files.
    """
    dirname = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return os.path.join(dirname, "include")
