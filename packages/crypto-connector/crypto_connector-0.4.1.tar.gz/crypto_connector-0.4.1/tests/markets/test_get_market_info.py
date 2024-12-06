import pytest

from crypto_connector.base.errors import ExchangeError
from crypto_connector.base.exchange import Exchange
from crypto_connector.base.schemas import Market


@pytest.mark.parametrize(
    "exchange,market",
    argvalues=[
        ("Binance", "SOLUSDT"),
        ("Binance", "solusdt"),
        ("HTX", "SOLUSDT"),
        ("HTX", "solusdt"),
    ],
    indirect=["exchange"],
)
def test_get_market_info(exchange: Exchange, market: str) -> None:
    info = exchange.get_market_info(market)
    assert isinstance(Market.model_validate(info), Market)


@pytest.mark.parametrize(
    "exchange,market",
    argvalues=[
        ("Binance", "XYZ"),
        ("HTX", "XYZ"),
    ],
    indirect=["exchange"],
)
def test_get_market_info_wrong_symbol(exchange: Exchange, market: str) -> None:
    with pytest.raises(ExchangeError):
        exchange.get_market_info(market)


@pytest.mark.parametrize(
    "exchange,market",
    argvalues=[
        ("Binance", ""),
        ("HTX", ""),
    ],
    indirect=["exchange"],
)
def test_get_market_info_empty_symbol(exchange: Exchange, market: str) -> None:
    with pytest.raises(ValueError):
        exchange.get_market_info(market)


if __name__ == "__main__":
    pytest.main([__file__])
