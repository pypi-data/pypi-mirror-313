"""Module containing Python code for the Python Object JSON Tool.

Attributes:
    __author__ (str): Python package template author.
    __email__ (str): Python package template author email.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

import json
from inspect import getfullargspec
from pathlib import Path
from typing import Dict, Any


class PythonObjectJson(object):
    """Base Python Object with JSON serialization and deserialization compatibility."""

    """Instantiate the Python Package Template example class.

    Args:
        example_init_parameter (str): Example class init parameter for the Python Package Template.
    
    Attributes:
        example_init_parameter (str): Example class attribute for the Python Package Template.
    
    """

    def __init__(self, **kwargs):
        """Instantiate the PythonObjectJson class with all keyword arguments.

        Args:
            kwargs (dict): Key/value pairs to be passed to the PythonObjectJson class.

        """
        vars(self).update(kwargs)

    def __str__(self):
        return self.to_json_str()

    def __repr__(self):
        return self.to_json_str()

    @staticmethod
    def _complex_json_handler(obj: Any) -> Any:
        """Custom handler to allow custom objects to be serialized into JSON.

        Args:
            obj (Any): Custom object to be serialized into JSON.

        Returns:
            obj (Any): Serializable version of the custom object.

        """
        if hasattr(obj, "_serialized"):
            # noinspection PyProtectedMember
            return obj._serialized()
        else:
            try:
                return str(obj)
            except TypeError:
                raise TypeError(
                    f"Object of type {type(obj)} with value of {repr(obj)} is not JSON serializable."
                )

    def _base_subclasses(self) -> Dict[str, Any]:
        """Create dict with snakecase keys derived from custom object type camelcase class names.

        Returns:
            dict[str, Any]: Dictionary with snakecase strings of all subclasses of PythonObjectJson as keys and
            subclasses as values.

        """
        return {
            cls.__name__.lower(): cls
            for cls in self.__class__.__mro__[-2].__subclasses__()
        }

    def _clean_data_dict(self) -> Dict[str, Any]:
        """Recursive method to un-type custom class type objects for serialization.

        Returns:
            dict[str, Any]: Dictionary that extracts serializable data from custom objects.

        """
        clean_dict = {}
        for k, v in vars(self).items():
            # noinspection PyProtectedMember
            clean_dict[k] = (
                v._clean_data_dict()
                if type(v) in self._base_subclasses().values()
                else v
            )
        return clean_dict

    def _serialized(self) -> Dict[str, Any]:
        """Pack up all object content into nested dictionaries for JSON serialization.

        Returns:
            dict[str, Any]: Serializable dictionary.

        """
        serializable_dict = dict()
        for att, val in self._clean_data_dict().items():
            if hasattr(val, "_serialized"):
                # noinspection PyProtectedMember
                serializable_dict[att] = val._serialized()
            elif isinstance(val, set):
                serializable_dict[att] = list(val)
            else:
                serializable_dict[att] = val
        return {self.__class__.__name__.lower(): serializable_dict}

    def _deserialized(self, json_data: Any) -> Any:
        """
        Args:
            json_data (Any): JSON data to be deserialized.

        Returns:
            obj (Any): Object deserialized from JSON.
        """
        if isinstance(json_data, list):
            return [self._deserialized(item) for item in json_data]
        elif isinstance(json_data, dict):
            base_subclasses = self._base_subclasses()
            # noinspection PyUnboundLocalVariable
            if (
                len(json_data) == 1
                and (single_key := next(iter(json_data.keys())))
                and single_key in base_subclasses
            ):
                # noinspection PyPep8Naming
                ClassObject = self._base_subclasses()[single_key]

                class_args = getfullargspec(ClassObject.__init__).args[1:]

                class_attributes: Dict[str, Any] = json_data[single_key]

                class_instance = ClassObject(
                    **{
                        k: self._deserialized(v)
                        for k, v in class_attributes.items()
                        if k in class_args
                    }
                )

                vars(class_instance).update(
                    {k: self._deserialized(v) for k, v in class_attributes.items()}
                )

                return class_instance
            else:
                return {k: self._deserialized(v) for k, v in json_data.items()}
        else:
            return json_data

    def to_json_str(self) -> str:
        """Serialize the class object to a JSON string.

        Returns:
            str: JSON string derived from the serializable version of the class object.

        """
        return json.dumps(
            self._serialized(),
            ensure_ascii=False,
            indent=2,
            default=self._complex_json_handler,
        )

    def save_to_json_file(self, json_file_path: Path) -> None:
        """Save the class object to a JSON file.

        Args:
            json_file_path (Path): Target JSON file path to which the class object will be saved.

        Returns:
            None

        """
        if not json_file_path.exists():
            json_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(json_file_path, "w", encoding="utf-8") as json_file_out:
            # TODO: fix incorrect file input type warning for json.dump from PyCharm bug https://youtrack.jetbrains.com/issue/PY-73050/openfile.txt-r-return-type-should-be-inferred-as-TextIOWrapper-instead-of-TextIO
            # noinspection PyTypeChecker
            json.dump(
                self._serialized(),
                json_file_out,
                indent=2,
                default=self._complex_json_handler,
                ensure_ascii=False,
            )

    def load_from_json_file(self, json_file_path: Path) -> None:
        """Load the class object from a JSON file.

        Args:
            json_file_path (Path): Target JSON file path from which the class object will be loaded.

        Returns:
            None

        """
        if not json_file_path.exists():
            raise FileNotFoundError(
                f"File {json_file_path} does not exist. Unable to load saved data."
            )

        with open(json_file_path, "r", encoding="utf-8") as json_file_in:
            loaded_class_instance = self._deserialized(json.load(json_file_in))
            vars(self).update(**vars(loaded_class_instance))
