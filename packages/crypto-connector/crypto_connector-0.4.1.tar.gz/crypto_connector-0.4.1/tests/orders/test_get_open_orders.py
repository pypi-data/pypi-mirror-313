import pytest

from crypto_connector.base.exchange import Exchange
from crypto_connector.base.schemas import Order


@pytest.mark.parametrize(
    "exchange",
    argvalues=[
        ("Binance"),
        ("HTX"),
    ],
    indirect=["exchange"],
)
def test_get_open_orders(exchange: Exchange) -> None:
    orders = exchange.get_open_orders()
    for order in orders:
        assert isinstance(Order.model_validate(order), Order)


if __name__ == "__main__":
    pytest.main([__file__])
