from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints


class API(BaseModel):
    created: datetime
    timestamp: int
    spot_enabled: bool
    ip_restricted: bool
    ips: list[str] | None = []
    info: dict[str, Any]


class Market(BaseModel):
    name: Annotated[str, StringConstraints(to_upper=True)]
    active: bool
    base: Annotated[str, StringConstraints(to_upper=True)]
    info: dict[str, Any]
    min_amt: float
    min_qty: float
    precision: int
    quote: Annotated[str, StringConstraints(to_upper=True)]
    spot: bool


# class Fee(BaseModel):
#     currency: str
#     cost: float
#     rate: float | None


class OrderStatus(str, Enum):
    open = "open"
    closed = "closed"
    canceled = "canceled"
    rejected = "rejected"
    canceling = "canceling"
    expired = "expired"


class Order(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True, use_enum_values=True)

    orderId: str
    dt: datetime
    market: Annotated[str, StringConstraints(to_upper=True)]
    type: Literal["limit", "market"]
    side: Literal["buy", "sell"]
    qty: float
    amount: float
    price: float
    status: OrderStatus
    time_in_force: str | None = None
    filled: float
    fee: float | None = None
    info: dict[str, Any]


class OrderCancelled(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    orderId: str
    success: bool


class BalanceAsset(BaseModel):
    coin: Annotated[str, StringConstraints(to_upper=True)]
    free: float
    total: float


class Balance(BaseModel):
    equity: float
    assets: list[BalanceAsset]


class TranferStatus(str, Enum):
    success = "success"
    pending = "pending"
    failed = "failed"


class Transfer(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True, use_enum_values=True)

    transferId: str
    date: datetime
    status: TranferStatus
    from_id: str
    to_id: str
    direction: Literal["in", "out"]
    coin: str
    qty: float
    info: dict[str, Any]
