"""Pytest top-level conftest.py.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

from typing import Type

import pytest

from pyobjson.pyobjson import PythonObjectJson


@pytest.fixture(scope="module")
def python_object_json_class() -> Type[PythonObjectJson]:
    """Provide PythonObjectJson class for testing.

    Returns:
        Type[PythonObjectJson]: PythonObjectJson class.

    """
    return PythonObjectJson
