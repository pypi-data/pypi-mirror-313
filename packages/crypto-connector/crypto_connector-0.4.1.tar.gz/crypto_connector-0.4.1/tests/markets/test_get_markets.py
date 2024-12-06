import pytest

from crypto_connector.base.exchange import Exchange
from crypto_connector.base.schemas import Market


@pytest.mark.parametrize(
    "exchange",
    argvalues=[
        ("Binance"),
        ("HTX"),
    ],
    indirect=["exchange"],
)
def test_get_markets(exchange: Exchange) -> None:
    markets = exchange.get_markets()
    for market in markets[:10]:
        assert isinstance(Market.model_validate(market), Market)


if __name__ == "__main__":
    pytest.main([__file__])
