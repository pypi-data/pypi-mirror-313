import pytest

from crypto_connector.base.exchange import Exchange


@pytest.mark.parametrize(
    "exchange,market",
    argvalues=[
        ("Binance", "XRPUSDC"),
        ("HTX", "XRPUSDT"),
    ],
    indirect=["exchange"],
)
def test_get_market_price(exchange: Exchange, market: str) -> None:
    assert exchange.get_market_price(market) > 0


if __name__ == "__main__":
    pytest.main([__file__])
