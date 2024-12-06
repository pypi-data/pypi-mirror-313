import pytest

from crypto_connector.base.errors import NotSupported
from crypto_connector.base.exchange import Exchange


@pytest.mark.parametrize(
    "exchange,market",
    argvalues=[
        ("Binance", "ETHUSDC"),
    ],
    indirect=["exchange"],
)
def test_get_ohlcv_ok(exchange: Exchange, market: str) -> None:
    ohlcv = exchange.get_ohlcv(market)
    assert len(ohlcv) > 0


@pytest.mark.parametrize(
    "exchange,market",
    argvalues=[
        ("HTX", "ETHUSDC"),
    ],
    indirect=["exchange"],
)
def test_get_ohlcv_not_supported(exchange: Exchange, market: str):
    with pytest.raises(NotSupported):
        exchange.get_ohlcv(market)


if __name__ == "__main__":
    pytest.main([__file__])
