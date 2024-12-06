from typing import Literal

import pytest

from crypto_connector.base.errors import ExchangeError
from crypto_connector.base.exchange import Exchange
from crypto_connector.base.schemas import Order


@pytest.mark.parametrize(
    "exchange,market,type,side,qty,price",
    argvalues=[
        ("Binance", "EURUSDC", "limit", "buy", 8, 0.95),
        ("HTX", "USDCUSDT", "limit", "buy", 12, 0.95),
    ],
    indirect=["exchange"],
)
def test_place_order_ok(
    exchange: Exchange,
    market: str,
    type: Literal["limit", "market"],
    side: Literal["buy", "sell"],
    qty: float,
    price: float,
) -> None:
    order = exchange.place_order(
        market,
        type=type,
        side=side,
        qty=qty,
        price=price,
    )
    assert Order.model_validate(order)
    assert order.get("orderId") is not None

    # cancel order
    result = exchange.cancel_order(order["orderId"])
    assert result["success"] is True


@pytest.mark.parametrize(
    "exchange,market,type,side,qty,price",
    argvalues=[
        ("Binance", "EURUSDC", "limit", "buy", 1000, 0.95),
        ("HTX", "USDCUSDT", "limit", "buy", 1000, 0.95),
    ],
    indirect=["exchange"],
)
def test_insufficient_balance_order(
    exchange: Exchange,
    market: str,
    type: Literal["limit", "market"],
    side: Literal["buy", "sell"],
    qty: float,
    price: float,
) -> None:
    with pytest.raises(ExchangeError):
        exchange.place_order(market, type=type, side=side, qty=qty, price=price)


@pytest.mark.parametrize(
    "exchange,market,type,side,qty,price",
    argvalues=[
        ("Binance", "EURUSDC", "limit", "buy", 500, 0.95),
        ("HTX", "USDCUSDT", "limit", "buy", 500, 0.95),
    ],
    indirect=["exchange"],
)
def test_order_insufficient_balance(
    exchange: Exchange,
    market: str,
    type: Literal["limit", "market"],
    side: Literal["buy", "sell"],
    qty: float,
    price: float,
) -> None:
    with pytest.raises(ExchangeError):
        exchange.place_order(market, type=type, side=side, qty=qty, price=price)


@pytest.mark.parametrize(
    "exchange,market,type,side,qty,price",
    argvalues=[
        ("Binance", "ETHUSDC", "limit", "buy", 1e-09, 1000),
        ("HTX", "ETHUSDT", "limit", "buy", 1e-09, 1000),
    ],
    indirect=["exchange"],
)
def test_place_order_wrong_precision(
    exchange: Exchange,
    market: str,
    type: Literal["limit", "market"],
    side: Literal["buy", "sell"],
    qty: float,
    price: float,
) -> None:
    with pytest.raises(ExchangeError):
        exchange.place_order(market, type=type, side=side, qty=qty, price=price)


if __name__ == "__main__":
    pytest.main([__file__])
