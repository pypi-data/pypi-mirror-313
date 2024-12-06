"""This module contains the Base Thoughtful Object."""

import json
import os
import pickle

from pydantic import BaseModel, TypeAdapter


class _BaseThoughtfulObject(BaseModel):
    """This class is the base class for all Thoughtful objects."""

    def to_json_str(self, include_fields: list[str] = None) -> str:
        """Convert an episode to a json string."""
        return self.model_dump_json(indent=4, include=include_fields)

    def to_dict(self) -> dict:
        """Convert an object to a dictionary."""
        return self.model_dump()

    def save_to_json_file(self, file_path: str = "", include_fields: list[str] = None) -> str:
        """Save an episode to a json file.

        Args:
            file_path (str): The path to the file.
            include_fields (list[str], optional): The fields to include in the json file.
        """
        folder_path = os.path.join(os.getcwd(), "output")
        if not os.path.exists(folder_path):
            folder_path = os.getcwd()
        self._custom_model_config["json_file_path"] = os.path.join(folder_path, f"{self.__class__.__name__}-%s.json")

        file_path = file_path or self._get_json_default_file_path()
        if not file_path:
            raise ValueError("File path must be provided or set in the model config.")
        _, extension = os.path.splitext(file_path)
        if extension != ".json":
            raise ValueError(f"File extension must be .json, not {extension}")

        with open(file_path, "w") as file:
            file.write(self.to_json_str(include_fields))
        return file_path

    def save_to_pickle_file(self, file_path: str) -> str:
        """Save an object to a pickle file.

        Args:
            file_path (str): The path to the file.
        """
        file_path = file_path or self.model_config.get("pickle_file_name")
        if not file_path:
            raise ValueError("File path must be provided or set in the model config.")
        with open(file_path, "wb") as file:
            pickle.dump(self, file)
        return file_path

    def pretty_string(self) -> str:
        """Convert an object to a string."""
        text = f"\n==={self.__class__.__name__}===\n"
        for key, value in self.__dict__.items():
            value_type = f"<{value.__class__.__name__}>"
            if isinstance(value, list):
                text += f"{key}: LIST[{len(value)}] \n"
                for number, item in enumerate(value):
                    text += f" [{number}] <{item.__class__.__name__}> {self._add_space(item)} \n"
            elif isinstance(value, tuple):
                text += f"{key}: TUPLE[{len(value)}] \n"
                for number, item in enumerate(value):
                    text += f" [{number}] <{item.__class__.__name__}> {self._add_space(item)} \n"
            elif isinstance(value, dict):
                text += f"{key}: DICT[{len(value.keys())}] \n"
                for k, v in value.items():
                    text += f" [{k}] <{v.__class__.__name__}> {self._add_space(v)} \n"
            else:
                text += f"{key}: {value_type} {self._add_space(value)} \n"
        return text[:-1]

    def _add_space(self, text: object):
        text = text.pretty_string() if isinstance(text, _BaseThoughtfulObject) else str(text)
        spaces = 4
        return text.replace("\n", "\n" + spaces * " ")

    @classmethod
    def load_from_pickle_file(cls, file_path: str):
        """Load an object from a pickle file and returns the object.

        Args:
            file_path (str): The path to the file.

        Returns:
            object: The objects.
        """
        try:
            with open(file_path, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to load file {file_path}. File not Found.")

    @classmethod
    def load_from_json_file(cls, file_path: str) -> "_BaseThoughtfulObject":
        """Load an object from a json file and returns the object.

        Args:
            file_path (str): The path to the file.

        Returns:
            object: The objects.
        """
        try:
            with open(file_path, "r") as file:
                return cls.model_validate_json(file.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to load file {file_path}. File not Found.")

    def get_json_schema(self, file_path):
        """Return the json schema for the object."""
        _, extension = os.path.splitext(file_path)
        if extension != ".json":
            raise ValueError(f"File extension must be .json, not {extension}")

        with open(file_path, "w") as file:
            file.write(json.dumps(self.model_json_schema(), indent=4))

    def _get_json_default_file_path(self):
        """Get default json file path."""
        try:
            self._custom_model_config["json_file_counter"] += 1
            return self._custom_model_config["json_file_path"] % (self._custom_model_config["json_file_counter"])
        except KeyError:
            return None

    @classmethod
    def save_objects_list_to_json_file(cls, object_list: list["_BaseThoughtfulObject"], file_path: str = ""):
        """Save a list of objects to a JSON file.

        Args:
            object_list (list[_BaseThoughtfulObject]): The list of objects to be saved.
            file_path (str, optional): The path to the JSON file. If not provided, a default file path will be used.

        Raises:
            ValueError: If the file path is not provided or set in the model config.
            ValueError: If the file extension is not ".json".

        """
        folder_path = os.path.join(os.getcwd(), "output")
        if not os.path.exists(folder_path):
            folder_path = os.getcwd()
        file_path = file_path or os.path.join(folder_path, f"{cls.__name__}-list.json")
        if not file_path:
            raise ValueError("File path must be provided or set in the model config.")
        _, extension = os.path.splitext(file_path)
        if extension != ".json":
            raise ValueError(f"File extension must be .json, not {extension}")

        with open(file_path, "w") as file:
            res = ""
            for objects in object_list:
                res += f"{objects.model_dump_json(indent=4)}, \n"
            res = f"[{res[:-3]}]"
            file.write(res)

    @classmethod
    def load_objects_list_from_json_file(cls, file_path: str) -> list["_BaseThoughtfulObject"]:
        """Load a list of objects from a JSON file and returns the list.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            list[_BaseThoughtfulObject]: The list of objects.

        Raises:
            ValidationError: If some fields are missing in the JSON data.
            FileNotFoundError: If the file is not found.
            Exception: If there is an error loading the file.

        """
        ta = TypeAdapter(list[cls])
        try:
            with open(file_path, "r") as file:
                data = file.read()
                return ta.validate_json(data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to load file {file_path}. File not Found.")
