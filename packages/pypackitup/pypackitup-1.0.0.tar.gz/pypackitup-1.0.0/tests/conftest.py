"""Pytest top-level conftest.py.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

import pytest

from pypackitup.helloworld import PythonPackageTemplate


@pytest.fixture(scope="module")
def python_package_template() -> PythonPackageTemplate:
    """Create a PythonPackageTemplate class object for testing.

    Returns:
        PythonPackageTemplate: Python package template class instance.

    """
    return PythonPackageTemplate()
