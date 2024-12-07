from hashboard.utils.cli import getenv_bool
from hashboard.utils.env import env_with_fallback


HASHBOARD_DEBUG = getenv_bool("HASHBOARD_DEBUG")
DEFAULT_CREDENTIALS_FILEPATH = "~/.hashboard/hb_access_key.json"
HASHBOARD_BASE_URI = env_with_fallback("HASHBOARD_CLI_BASE_URI", "GLEAN_CLI_BASE_URI", "https://hashboard.com")
FILE_SIZE_LIMIT_MB = 50
