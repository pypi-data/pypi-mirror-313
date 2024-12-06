"""Module containing Python code for the Python Package Template.

This module is an example for the Python Package Template.

Attributes:
    __author__ (str): Python package template author.
    __email__ (str): Python package template author email.

"""
from __future__ import annotations

__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"


class PythonPackageTemplate(object):

    def __init__(self, example_init_parameter: str = "Hello"):
        """Instantiate the Python Package Template example class.

        Args:
            example_init_parameter (str): Example class init parameter for the Python Package Template.

        Attributes:
            example_init_parameter (str): Example class attribute for the Python Package Template.

        """
        self.example_init_parameter = example_init_parameter

    def example_method(self, example_parameter: str = "World") -> str:
        """Example method for the Python Package Template.

        Args:
            example_parameter (str): Example class method parameter for the Python Package Template.

        Examples:
            >>> from pypackitup.helloworld import PythonPackageTemplate
            >>> example_class_instance = PythonPackageTemplate()
            >>> print(example_class_instance.example_method())
            Hello, World!

        Returns:
            str: Example return string for the Python Package Template.

        """
        if not example_parameter:
            raise ValueError("Invalid argument provided for example_parameter.")

        return f"{self.example_init_parameter}, {example_parameter}!"


def main() -> None:
    """Example main function for the Python Package Template.

    Returns:
        None

    """
    example_class_instance = PythonPackageTemplate()
    print(example_class_instance.example_method())


if __name__ == "__main__":
    main()
