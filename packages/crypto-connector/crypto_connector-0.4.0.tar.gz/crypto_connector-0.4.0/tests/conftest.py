import os
import sys

import pytest
from dotenv import load_dotenv

import crypto_connector as cc
from crypto_connector.base.exchange import Exchange

load_dotenv()


CREDENTIALS = {
    "Binance": {
        "sub_api_key": os.getenv("BINANCE_SUB_API_KEY_TEST"),
        "sub_api_secret": os.getenv("BINANCE_SUB_API_SECRET_TEST"),
        "sub_email": os.getenv("BINANCE_SUB_EMAIL_TEST"),
        "master_api_key": os.getenv("BINANCE_MASTER_API_KEY_TEST"),
        "master_api_secret": os.getenv("BINANCE_MASTER_API_SECRET_TEST"),
    },
    "HTX": {
        "api_key": os.getenv("HTX_API_KEY_TEST"),
        "api_secret": os.getenv("HTX_API_SECRET_TEST"),
    },
}


@pytest.fixture(scope="session")
def exchange(request: pytest.FixtureRequest) -> Exchange:
    # cannot run 'exchange' tests on github runners (because hosted in the US)
    if not sys.platform.startswith("win"):
        pytest.skip(
            reason="tests for windows only",
            allow_module_level=True,
        )

    exchange_name = request.param
    exchange = getattr(cc, exchange_name)(**CREDENTIALS[exchange_name])
    return exchange
