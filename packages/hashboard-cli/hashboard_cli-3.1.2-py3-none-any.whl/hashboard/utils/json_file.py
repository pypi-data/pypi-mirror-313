import json
from pathlib import Path
from typing import Any

def read_json_file(filepath: Path) -> dict:
    values = {}
    if filepath.exists():
        with open(filepath, "r") as f:
            content = f.read().strip()
            if content:
                values = json.loads(content)
    return values

def write_json_file(filepath: Path, data: dict):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def write_json_key(filepath: Path, key: str, value: Any):
    values = read_json_file(filepath)
    values[key] = value
    write_json_file(filepath, values)

def delete_json_key(filepath: Path, key: str):
    values = read_json_file(filepath)
    if key in values:
        del values[key]
    write_json_file(filepath, values)
