import os
import sys


# Note: platformdirs distinguishes Darwin and Unix, but we use the Unix
# conventions on Darwin.
if sys.platform == "win32":
    from platformdirs.windows import Windows as PlatformDirs
else:
    from platformdirs.unix import Unix as PlatformDirs


class NoApiKey(Exception):
    pass


def api_key_from_env():
    return os.environ.get("IMANDRA_API_KEY")


def api_key_from_file(fpath):
    try:
        with open(fpath) as f:
            return f.read().strip()
    except OSError:
        return None


def get_api_key(api_key=None):
    api_key = (
        api_key
        or api_key_from_env()
        or api_key_from_file(
            PlatformDirs(appname="imandra").user_config_path / "api_key"
        )
        or api_key_from_file(
            PlatformDirs(appname="imandrax").user_config_path / "api_key"
        )
    )
    if api_key is None:
        raise NoApiKey("Please provide an API key.")
    return api_key
