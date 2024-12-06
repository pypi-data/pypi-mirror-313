import pytest

from crypto_connector.base.exchange import Exchange


@pytest.mark.parametrize(
    "exchange",
    argvalues=[
        ("Binance"),
        ("HTX"),
    ],
    indirect=["exchange"],
)
def test_get_server_time(exchange: Exchange) -> None:
    assert exchange.get_server_time() > 1


if __name__ == "__main__":
    pytest.main([__file__])
    pytest.main([__file__])
