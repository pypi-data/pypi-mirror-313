import logging
import os

import requests

from . import constants as c

log = logging.getLogger(__name__)


def callhome_version() -> None:
    build_tag = os.getenv(c.ENV_BUILD_TAG, os.getenv(c.ENV_COMMIT_TAG))
    call_home_token = os.getenv(c.ENV_CALLHOME_TOKEN)
    if call_home_token is not None:
        resp = requests.post(
            "https://jfk-enterprise.com/api/callhome/version/",
            timeout=10,
            headers={
                "Authorization": f"Bearer {call_home_token}",
            },
            json={
                "version": build_tag,
            },
        )
        log.debug(f"Resp {resp.status_code} - {resp.json()}")  # noqa: G004
    else:
        log.warning("No Call Home Token")


def callhome_keep_alive() -> None:
    call_home_token = os.getenv(c.ENV_CALLHOME_TOKEN)
    if call_home_token is not None:
        resp = requests.post("https://jfk-enterprise.com/api/callhome/keep-alive", timeout=10)
        log.debug(f"Resp {resp.status_code} - {resp.json()}")  # noqa: G004
