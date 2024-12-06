"""Pytest test for Python Package Template code.

Note:
    Tests helloworld.py module.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

import pytest


def test_example_method_default(python_package_template):
    result = python_package_template.example_method()

    assert result == "Hello, World!"


def test_example_method_custom(python_package_template):
    result = python_package_template.example_method("Everyone")

    assert result == "Hello, Everyone!"


def test_example_method_none(python_package_template):
    with pytest.raises(ValueError, match="Invalid argument provided for example_parameter."):
        python_package_template.example_method("")
