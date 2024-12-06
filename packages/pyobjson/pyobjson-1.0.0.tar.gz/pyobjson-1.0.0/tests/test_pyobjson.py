"""Pytest test for Python Object JSON Tool code.

Note:
    Tests pyobjson.py module.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

import json
from typing import List


def test_serialization_to_json_string(python_object_json_class):

    class TestChildClass(python_object_json_class):

        def __init__(self, test_param: str):
            super().__init__()
            self.test_param = test_param

    class TestParentClass(python_object_json_class):

        def __init__(self, test_child_class_list: List[TestChildClass]):
            super().__init__()
            self.test_parent_class_list = test_child_class_list

    serialized_test_parent_class = json.dumps(
        {
            "testparentclass": {
                "test_parent_class_list": [
                    {
                        "testchildclass": {
                            "test_param": "test_param_1"
                        }
                    },
                    {
                        "testchildclass": {
                            "test_param": "test_param_2"
                        }
                    }
                ]
            }
        },
        ensure_ascii=False,
        indent=2
    )

    test_parent_class_instance = TestParentClass(
        [TestChildClass(test_param="test_param_1"), TestChildClass(test_param="test_param_2")]
    )

    assert test_parent_class_instance.to_json_str() == serialized_test_parent_class
