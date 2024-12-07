import inspect
import sys

from . import auth

try:
    from imandrax_api import (  # pyright: ignore [reportMissingImports]
        Client as BaseClient,
    )
except ModuleNotFoundError as err:
    note = """
        Install imandra with the optional 'core' dependency to enable imandra.core:

            pip install 'imandra[core]>=2.0.0'
    """
    err.msg += "\n\n" + inspect.cleandoc(note)
    v = sys.version_info
    if (v.major, v.minor) < (3, 12):
        note = f"""
        Note that imandrax_api requires Python >= 3.12. You are using Python {v.major}.{v.minor}.{v.micro}.
        """
        err.msg += "\n\n" + inspect.cleandoc(note)
    raise


class Client(BaseClient):
    def __init__(self, api_key=None, url=None, **kwargs):
        kwargs["url"] = url or "https://api.imandra.ai/internal/imandrax"
        kwargs["auth_token"] = auth.get_api_key(api_key)
        super().__init__(**kwargs)
