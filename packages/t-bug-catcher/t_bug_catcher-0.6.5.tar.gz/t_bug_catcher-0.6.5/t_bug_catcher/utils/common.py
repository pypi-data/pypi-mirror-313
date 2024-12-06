import copy
import json
import os
import re
import traceback
import urllib
from datetime import date, datetime
from pathlib import Path
from types import TracebackType
from typing import List

from ..config import CONFIG


class Encoder(json.JSONEncoder):
    """This class is used to encode the Episode object to json."""

    def default(self, o):
        """This method is used to encode the Episode object to json.

        Args:
            o (object): The object to be encoded.

        Returns:
            str: The json string.
        """
        try:
            object_copy = copy.deepcopy(o)
        except (TypeError, AttributeError):
            return str(o)[: CONFIG.LIMITS.STACK_TEXT_LENGTH]
        try:
            if hasattr(object_copy, "__dict__"):
                keys_to_remove = [
                    key
                    for key in object_copy.__dict__.keys()
                    if any(s in str(key).lower() for s in CONFIG.KEYS_TO_REMOVE)
                ]
                for key in keys_to_remove:
                    del object_copy.__dict__[key]
                return {
                    str(key): str(value)[: CONFIG.LIMITS.STACK_TEXT_LENGTH]
                    for key, value in object_copy.__dict__.items()
                }
            if isinstance(object_copy, (datetime, date)):
                return object_copy.isoformat()
            if isinstance(object_copy, Path):
                return str(object_copy)
            return super().default(self, object_copy)
        except TypeError:
            return str(object_copy)[: CONFIG.LIMITS.STACK_TEXT_LENGTH]


def get_frames(exc_traceback: TracebackType) -> List:
    """Get the frames of the exception.

    Args:
        exc_traceback (TracebackType): The traceback of the exception.

    Returns:
        List: The frames of the exception.
    """
    frames = [
        frame for frame in traceback.extract_tb(exc_traceback) if "site-packages" not in str(frame.filename).lower()
    ]
    if not frames:
        frames = [frame for frame in traceback.extract_tb(exc_traceback)]
    return frames


def convert_keys_to_primitives(data: dict) -> dict:
    """A function that recursively converts keys in a nested dictionary to primitives.

    Args:
        data (dict): The input dictionary to convert keys.

    Returns:
        dict: A new dictionary with keys converted to strings.
    """
    new_dict = {}
    for key, value in data.items():
        if isinstance(value, list) or isinstance(value, tuple):
            value = value[: CONFIG.LIMITS.STACK_ITEM_LENGTH]
        if isinstance(value, dict):
            items_list = list(value.items())
            sliced_list = items_list[: CONFIG.LIMITS.STACK_ITEM_LENGTH]
            value = dict(sliced_list)
            new_dict[str(key)] = convert_keys_to_primitives(value)
        else:
            new_dict[str(key)] = value
    return new_dict


def strip_path(path: str):
    """A function to strip the current working directory path from the input.

    Args:
        path (str): The path from which to strip the current working directory path.

    Returns:
        str: The stripped path.
    """
    return path.replace(os.getcwd(), "").strip(os.sep)


def remove_holotree_id(path: str) -> str:
    """A function to remove the value after 'holotree' from the path.

    Args:
        path (str): The path from which to remove the value after 'holotree'.

    Returns:
        str: The modified path.
    """
    pattern = r"(holotree\/)[^\/]+\/"
    return re.sub(pattern, r"\1", path)


def retrieve_build_info():
    """Logs build information."""
    if not os.path.exists(CONFIG.BUILD_INFO_FILE):
        return
    with open(CONFIG.BUILD_INFO_FILE, "r") as json_file:
        commit_info = json.load(json_file)
    repository_url = commit_info["repository_url"]
    current_branch = commit_info["branch"]
    encoded_branch = urllib.parse.quote(current_branch)
    commit_info["branch_url"] = f"{repository_url}/src/{commit_info['last_commit']}/?at={encoded_branch}"
    commit_info["commit_url"] = f"{repository_url}/commits/{commit_info['last_commit']}/"
    return commit_info
