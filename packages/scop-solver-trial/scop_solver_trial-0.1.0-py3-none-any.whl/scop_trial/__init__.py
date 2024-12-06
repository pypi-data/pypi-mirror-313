from importlib.metadata import metadata

from .scop import (
    Alldiff,
    Constraint,
    Linear,
    Model,
    Parameters,
    Quadratic,
    Variable,
    plot_scop,
)

__all__ = ["Alldiff", "Constraint", "Linear", "Model", "Parameters", "Quadratic", "Variable", "plot_scop"]

_package_metadata = metadata(str(__package__))
__version__ = _package_metadata["Version"]
__author__ = _package_metadata.get("Author-email", "")
