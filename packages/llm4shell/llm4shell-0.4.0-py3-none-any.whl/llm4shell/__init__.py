import getpass
import os
import sys
from pathlib import Path
import litellm
import logging
logging.getLogger("LiteLLM").setLevel(logging.WARNING)

from llm4shell.utils import check_click # noqa

if os.getenv("OR_SITE_URL") is None:
    os.environ["OR_SITE_URL"] = "localhost"

if os.getenv("OR_APP_NAME") is None:
    username = getpass.getuser()
    filename = Path(sys.argv[0]).name
    os.environ["OR_APP_NAME"] = f"{username}:{filename}"

litellm.openrouter_key = os.getenv("OPENROUTER_API_KEY")
