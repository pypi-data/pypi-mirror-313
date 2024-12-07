import logging
import os
import tempfile
from pathlib import Path

from hashboard.utils.json_file import read_json_file, write_json_key, delete_json_key

def read_session_state_value(key: str):
    try:
        filepath = _get_session_state_filepath()
        values = read_json_file(filepath)
        return values.get(key, None)
    except Exception:
        logging.debug(f"Error reading state file", exc_info=True)
        return None

def write_session_state_value(key: str, value: str):
    try:
        filepath = _get_session_state_filepath()
        write_json_key(filepath, key, value)
    except Exception:
        logging.debug(f"Error updating session state file", exc_info=True)

def delete_session_state_value(key: str):
    try:
        filepath = _get_session_state_filepath()
        delete_json_key(filepath, key)
        remaining_values = read_json_file(filepath)
        if not remaining_values == 0:
            filepath.unlink()
    except Exception:
        logging.debug(f"Error updating session state file", exc_info=True)

def _get_session_state_filepath():
    temp_dir = tempfile.gettempdir()
    hashboard_cli_dir = os.path.join(temp_dir, 'hashboard-cli')
    os.makedirs(hashboard_cli_dir, exist_ok=True)
    session_pid = os.getppid()
    filepath = Path(hashboard_cli_dir) / f'{session_pid}'
    if not filepath.exists():
        filepath.write_text('')
    return filepath
