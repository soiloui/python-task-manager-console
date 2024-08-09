import json
import os.path
from typing import Any, Optional
from utils.print_utils import print_error


def is_valid_json_file_exists(file_path: str) -> bool:
    """Check if a valid JSON file exists and is non-empty."""
    if not os.path.exists(file_path):
        return False
    if os.stat(file_path).st_size == 0:
        return False

    try:
        with open(file_path, 'r') as json_file:
            json.load(json_file)
    except (ValueError, json.JSONDecodeError) as e:
        return False

    return True


def load_data_from_json_file(file_path: str) -> Optional[Any]:
    """Load data from a JSON file, or return None if the file is invalid."""
    if not is_valid_json_file_exists(file_path):
        return None

    try:
        with open(file_path) as json_file:
            return json.load(json_file)
    except (ValueError, json.JSONDecodeError, IOError) as e:
        return None


def write_data_to_json_file(file_path: str, data: Any) -> None:
    """Write data to a JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print_error(f"Failed to write data to JSON file: {e}")
        raise e


def write_data_to_txt_file(file_path: str, data: str) -> None:
    """ Writes data to a text file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data)
    except IOError as e:
        print_error(f"Failed to write data to text file: {e}")
        raise e
