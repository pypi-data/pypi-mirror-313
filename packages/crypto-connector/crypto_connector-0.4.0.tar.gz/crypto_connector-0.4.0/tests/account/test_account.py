import pytest

from crypto_connector.base.exchange import Exchange
from crypto_connector.base.schemas import Balance


@pytest.mark.parametrize(
    "exchange",
    argvalues=[
        ("Binance"),
        ("HTX"),
    ],
    indirect=["exchange"],
)
def test_get_api_key_info(exchange: Exchange) -> None:
    info = exchange.get_api_key_info()
    assert info["timestamp"] > 0


@pytest.mark.parametrize(
    "exchange",
    argvalues=[
        ("Binance"),
        ("HTX"),
    ],
    indirect=["exchange"],
)
def test_get_balance(exchange: Exchange) -> None:
    balance = exchange.get_balance()
    assert Balance.model_validate(balance)
    assert balance["equity"] >= 0


@pytest.mark.parametrize(
    "exchange",
    argvalues=[
        ("Binance"),
        ("HTX"),
    ],
    indirect=["exchange"],
)
def test_get_transfer_history(exchange: Exchange) -> None:
    transfers = exchange.get_transfer_history()
    assert isinstance(transfers, list)


if __name__ == "__main__":
    pytest.main([__file__])
