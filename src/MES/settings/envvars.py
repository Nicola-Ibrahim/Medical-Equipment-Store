"""This script is responsible to override settings variable from .env file"""

from MES.core.utils.collections import deep_update
from MES.core.utils.settings import get_settings_from_environment

# update the project settings variables with environment variables
deep_update(globals(), get_settings_from_environment(ENVVAR_SETTINGS_PREFIX))  # type: ignore
