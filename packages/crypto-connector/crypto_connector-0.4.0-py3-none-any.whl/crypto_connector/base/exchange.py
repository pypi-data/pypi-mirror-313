import logging
from datetime import datetime, timezone
from decimal import Decimal
from json.decoder import JSONDecodeError
from typing import Any, Literal

import requests

from crypto_connector.base.errors import NotSupported


class Exchange:
    """Base exchange class"""

    base_url: str
    name: str
    recv_window = 5000
    timeframes: dict[str, Any]
    timeout = 10000

    def __init__(self, **kwargs):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        self.logger = logging.getLogger(__name__)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @staticmethod
    def _convert_to_str(d: dict) -> dict:
        out = {}
        for k in d.keys():
            if isinstance(d[k], bool):
                out[k] = str(d[k]).lower()
            elif isinstance(d[k], int | float):
                out[k] = str(d[k])
            else:
                out[k] = d[k]
        return out

    @staticmethod
    def _clean_none_values(d: dict) -> dict:
        out = {}
        for k in d.keys():
            if d[k] is not None:
                out[k] = d[k]
        return out

    @staticmethod
    def truncate_float(f: float, decimal_places: int) -> float | int:
        """Truncates a float f to n decimal places without rounding.
        Inspired by https://stackoverflow.com/a/783927
        """
        if not isinstance(f, int | float):
            raise ValueError("The input must be a float or an int.")

        if (not isinstance(decimal_places, int)) or (decimal_places < 0):
            raise ValueError("`decimal_places` argument must a positive int.")

        s = "{}".format(f)
        if "e" in s or "E" in s:
            res = "{0:.{1}f}".format(f, decimal_places)
            return float(res)

        left, _, right = s.partition(".")

        if decimal_places == 0:
            return int(left)

        res = ".".join([left, (right + "0" * decimal_places)[:decimal_places]])
        return float(res)

    @staticmethod
    def decimal_places(n: int | float) -> int:
        """
        Returns the precision (number of decimal places) of a decimal number
        """
        if not isinstance(n, (float, int)):
            raise ValueError("The input must be a float or an integer")

        d = Decimal(f"{n}")
        return int(str(d.as_tuple().exponent).lstrip("-"))

    def compute_quote_qty(self, qty, market) -> float:
        raw_qty = qty * self.get_market_price(market=market)
        market_info = self.get_market_info(market)
        quote_qty = self.truncate_float(
            raw_qty, decimal_places=market_info["precision"]
        )
        return quote_qty

    @staticmethod
    def sort_by(array, key, descending=False, default=0):
        return sorted(
            array,
            key=lambda k: k[key] if k[key] is not None else default,
            reverse=descending,
        )

    @staticmethod
    def dt_to_unix(
        dt: datetime, tzinfo: timezone = timezone.utc, unit: str = "ms"
    ) -> int | None:
        unit_map = {"s": 1, "ms": 1e3, "ns": 1e6}
        if unit not in unit_map.keys():
            raise ValueError(
                f"Wrong unit {unit}. "
                f"Unit should be one of {list(unit_map.keys())}"
            )

        if dt is None:
            return None
        return int(dt.replace(tzinfo=tzinfo).timestamp() * unit_map[unit])

    @staticmethod
    def str_to_dt(
        string: str,
        format: str = "%Y-%m-%dT%H:%M:%SZ",
        tz: timezone = timezone.utc,
    ) -> datetime:
        return datetime.strptime(string, format).replace(tzinfo=tz)

    @staticmethod
    def _cast_values(params: dict[str, Any]) -> dict:
        return {}

    def prepare_params(self, params: dict[str, Any]) -> dict[str, Any]:
        return self._cast_values(self._clean_none_values(params))

    def handle_exception(self, r: requests.Response) -> None:
        return

    def request(
        self,
        http_method: str,
        url_path: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | str | None = None,
    ) -> Any:
        if not params:
            params = {}

        url = f"{self.base_url}{url_path}"

        if http_method == "GET":
            prep_params = self.prepare_params(params)
            r = self.session.request(http_method, url=url, params=prep_params)
        else:
            r = self.session.request(http_method, url=url, data=data)

        self.handle_exception(r)

        try:
            content = r.json()
        except JSONDecodeError:
            content = {"data": r.text}

        return content

    def signed_request(
        self,
        http_method: str,
        url_path: str,
        params: dict | None = None,
        data: dict | None = None,
    ) -> dict[str, Any]:
        return {}

    #################
    # EXCHANGE INFO #
    #################
    def get_server_time(self) -> Any:
        raise NotSupported(
            f"{self.name}: get_server_time() is not supported yet"
        )

    ###########
    # ACCOUNT #
    ###########
    def get_api_key_info(self) -> dict:
        raise NotSupported(
            f"{self.name}: get_api_key_info() is not supported yet"
        )

    def get_balance(self) -> dict:
        raise NotSupported(f"{self.name}: get_balance() is not supported yet")

    def get_transfer_history(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        **kwargs,
    ) -> list[dict]:
        raise NotSupported(
            f"{self.name}: get_transfer_history() is not supported yet"
        )

    ###########
    # MARKETS #
    ###########
    def get_markets(self, **kwargs) -> list[dict]:
        raise NotSupported(f"{self.name}: get_markets() is not supported yet")

    def get_market_price(self, market: str) -> float:
        raise NotSupported(f"{self.name}: get_markets() is not supported yet")

    def get_market_info(self, market: str, **kwargs) -> dict[str, Any]:
        raise NotSupported(
            f"{self.name}: get_market_info() is not supported yet"
        )

    def get_ohlcv(
        self,
        market: str,
        timeframe: str = "1d",
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        **kwargs,
    ) -> list[list]:
        raise NotSupported(f"{self.name}: get_ohlcv() is not supported yet")

    #########
    # ORDER #
    #########
    def place_test_order(
        self,
        market: str,
        type: Literal["limit", "market"],
        side: Literal["buy", "sell"],
        qty: float,
        price: float | None = None,
        **kwargs,
    ):
        raise NotSupported(
            f"{self.name}: place_test_order() is not supported yet"
        )

    def place_order(
        self,
        market: str,
        type: Literal["limit", "market"],
        side: Literal["buy", "sell"],
        qty: float,
        price: float | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        raise NotSupported(f"{self.name}: place_order() is not supported yet")

    def get_open_orders(self, market: str | None = None) -> list[dict]:
        raise NotSupported(f"{self.name}: place_order() is not supported yet")

    def cancel_order(self, id: str) -> dict[str, Any]:
        raise NotSupported(f"{self.name}: cancel_order() is not supported yet")

    def cancel_orders(
        self, market: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        raise NotSupported(
            f"{self.name}: cancel_orders() is not supported yet"
        )
