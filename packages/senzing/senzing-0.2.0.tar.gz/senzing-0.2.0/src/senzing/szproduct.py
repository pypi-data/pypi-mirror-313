#! /usr/bin/env python3

"""
szproduct.py is the abstract class for all implementations of szproduct.
"""

# TODO: Determine specific SzError, Errors for "Raises:" documentation.
from abc import ABC, abstractmethod

from .szhelpers import construct_help

# Metadata

__all__ = ["SzProduct"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-27"

# -----------------------------------------------------------------------------
# SzProduct
# -----------------------------------------------------------------------------


class SzProduct(ABC):
    """
    SzProduct is the definition of the Senzing Python SDK that is
    implemented by packages such as szproduct.py.
    """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def get_license(self) -> str:
        """
        The `get_license` method retrieves information about the currently used license.

        Returns:
            str: A JSON document containing Senzing license metadata.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szproduct/get_license.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szproduct/get_license.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_version(self) -> str:
        """
        The `get_version` method returns the version of Senzing.

        Returns:
            str: A JSON document containing metadata about the Senzing Engine version being used.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szproduct/get_version.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szproduct/get_version.txt
                :linenos:
                :language: json
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------

    def help(self, method_name: str = "") -> str:
        """
        Return the help for a particular message.

        Args:
            method_name (str): The name of the method. (e.g. "init"). If empty, a list of methods and descriptions is returned.

        Returns:
            str: The Help information about the requested method
        """
        return construct_help(self, method_name=method_name)
