import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone
from json.decoder import JSONDecodeError
from typing import Any, Literal
from urllib.parse import urlencode, urlparse

from requests.models import Response

from crypto_connector.base.errors import BadResponse, ExchangeError, MissingCredentials
from crypto_connector.base.exchange import Exchange
from crypto_connector.base.schemas import (
    API,
    Balance,
    BalanceAsset,
    Market,
    Order,
    OrderCancelled,
    OrderStatus,
    TranferStatus,
    Transfer,
)


class HTX(Exchange):
    base_url = "https://api.huobi.pro"  # or api-aws.huobi.pro for aws client
    name = "HTX"
    order_statuses = {
        # spot
        "partial-filled": OrderStatus.open,
        "partial-canceled": OrderStatus.canceled,
        "filled": OrderStatus.closed,
        "canceled": OrderStatus.canceled,
        "submitted": OrderStatus.open,
        "created": OrderStatus.open,  # For stop orders
    }
    timeframes = {
        "1m": "1min",
        "5m": "5min",
        "15m": "15min",
        "1h": "60min",
        "4h": "4hour",
        "1d": "1day",
        "1w": "1week",
        "1M": "1mon",
    }

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        headers: bool = False,
        **kwargs,
    ) -> None:
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = headers

    @staticmethod
    def get_timestamp() -> str:
        return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def _urlencode_dict(query: dict) -> str:
        return urlencode(query, True)

    @staticmethod
    def _cast_values(params: dict) -> dict:
        lower_params = ["symbol", "symbols"]
        out = {}
        for key, value in params.items():
            if key in lower_params:
                if isinstance(key, str):
                    out[key] = value.lower()
                else:
                    raise ValueError(f"{key} should be a string.")
            else:
                out[key] = str(value)
        return out

    def _urlencode_params(self, params: dict) -> str:
        return self._urlencode_dict(self._cast_values(self._clean_none_values(params)))

    def _prepare_request_data(self, data: dict) -> str:
        casted_data = self._cast_values(self._clean_none_values(data))
        return json.dumps(casted_data)

    @staticmethod
    def sort_dict(d: dict) -> dict:
        """ASCII sort dict"""
        if not isinstance(d, dict):
            raise ValueError("The input must be a dictionary")
        return dict(sorted(d.items()))

    @staticmethod
    def hash(api_secret: str, query_str: str) -> bytes:
        hash_obj = hmac.new(
            api_secret.encode("utf-8"),
            msg=query_str.encode("utf-8"),
            digestmod=hashlib.sha256,
        )
        return hash_obj.digest()

    @staticmethod
    def base64_encode(hash: bytes) -> str:
        return base64.b64encode(hash).decode()

    def signed_request(
        self,
        http_method: str,
        url_path: str,
        params: dict | None = None,
        data: dict | None = None,
    ) -> dict[str, Any]:
        if (not self.api_key) or (not self.api_secret):
            raise MissingCredentials(
                "To use private endpoints, user must pass credentials."
            )

        if params and data:
            raise ValueError("Can only pass `params` or `data`, but not both.")

        payload = params or data or {}
        to_sign_payload = {
            "AccessKeyId": self.api_key,
            "SignatureMethod": "HmacSHA256",
            "SignatureVersion": 2,
            "Timestamp": self.get_timestamp(),
        }
        if http_method == "GET":
            to_sign_payload.update(payload)

        encoded_payload = self._urlencode_params(self.sort_dict(to_sign_payload))
        host = urlparse(self.base_url).hostname
        to_hash = f"{http_method}\n{host}\n{url_path}\n{encoded_payload}"
        hash_obj = self.hash(self.api_secret, query_str=to_hash)  # type: ignore[arg-type]  # noqa: E501
        signature = self.base64_encode(hash_obj)
        to_sign_payload.update({"Signature": signature})
        url_path += "?" + self._urlencode_params(to_sign_payload)

        if http_method == "GET":
            return self.request(http_method, url_path=url_path, params=None)
        else:
            prep_data = self._prepare_request_data(data=payload)
            return self.request(http_method, url_path=url_path, data=prep_data)

    def handle_exception(self, r: Response) -> None:
        try:
            rjson = r.json()
        except JSONDecodeError:
            raise BadResponse(f"Could not decode response text: {r.text}")

        if rjson.get("status") == "ok" or rjson.get("ok") is True:
            return

        error = {}
        error["status_code"] = rjson.get("err-code") or rjson.get("code")
        error["msg"] = rjson.get("err-msg") or rjson.get("message")
        if self.headers:
            error["headers"] = r.headers
        raise ExchangeError(error)

    ###############################
    # EXCHANGE SPECIFIC ENDPOINTS #
    ###############################
    def _get_uid(self) -> int:
        """This endpoint allow users to view the user ID of the account easily.
        :see: https://www.htx.com/en-us/opend/newApiPages/?id=7ec52d6c-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        r = self.signed_request("GET", "/v2/user/uid")
        # {'code': 200, 'data': 000000000, 'ok': True}
        return r.get("data", -1)

    @property
    def _account_id(self) -> int:
        r = self.signed_request("GET", "/v1/account/accounts")
        # {
        # "data":[
        #     {
        #         "id":01234567,
        #         "state":"working",
        #         "subtype":"",
        #         "type":"spot"
        #     }
        # ],
        # "status":"ok"
        # }
        return r.get("data", -1)[0]["id"]

    #################
    # EXCHANGE INFO #
    #################
    def get_server_time(self) -> int:
        """
        Fetch the current timestamp in millisecondsfrom the exchange server
        :see: https://www.htx.com/en-in/opend/newApiPages/?id=7ec4bb2c-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        r = self.request("GET", "/v1/common/timestamp")
        # {"status": "ok", "data": 1629715504949}
        return r.get("data", -1)

    # ###########
    # # ACCOUNT #
    # ###########
    def _parse_api_key_info(self, api_info: dict[str, Any]) -> dict[str, Any]:
        api_obj = API(
            created=api_info["createTime"],
            timestamp=api_info["createTime"],
            spot_enabled="trade" in api_info["permission"],
            ip_restricted=len(api_info["ipAddresses"]) > 0,
            ips=api_info["ipAddresses"].split(","),
            info=api_info,
        )
        return api_obj.model_dump()

    def get_api_key_info(self) -> dict[str, Any]:
        """
        Return API KEY info of the current user.
        :see: https://www.htx.com/en-in/opend/newApiPages/?id=7ec52c92-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        params = {"uid": self._get_uid(), "accessKey": self.api_key}
        r = self.signed_request("GET", "/v2/user/api-key", params=params)
        # {
        #     'code': 200,
        #     'data': [{'accessKey': '5cd012ef-ez2xc4vb6n-29e57c70-72b72',
        #            'createTime': 1716580080000,
        #            'ipAddresses': 'XX.XX.XX.XXX,XX.XXX.XXX.XX',
        #            'note': 'trading bot api',
        #            'permission': 'readOnly,trade',
        #            'status': 'normal',
        #            'updateTime': 1716580080000,
        #            'validDays': -1}],
        #     'message': 'success',
        #     'ok': True
        # }
        data = r.get("data")
        if not data:
            raise BadResponse(f"No data returned from server {r=}.")

        api_key_info = self._parse_api_key_info(data[0])
        return api_key_info

    def _get_balance_value(self):
        """Get balance value in dollars.
        :see: https://www.htx.com/en-us/opend/newApiPages/?id=7ec4ff6d-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        params = {"accountType": "spot", "valuationCurrency": "USD"}
        r = self.signed_request("GET", "/v2/account/asset-valuation", params=params)
        balance_usd = r["data"]["balance"]
        return float(balance_usd)

    @staticmethod
    def _parse_balance_asset(asset: dict) -> BalanceAsset:
        return BalanceAsset(
            coin=asset["currency"],
            free=asset["available"],
            total=asset["available"],
        )

    def get_balance(self) -> dict:
        """
        Query for balance and get the amount of funds available for trading
        or funds locked in orders.
        :see: https://www.htx.com/en-us/opend/newApiPages/?id=7ec4b429-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        account_id = self._account_id
        r = self.signed_request("GET", f"/v1/account/accounts/{account_id}/balance")
        # {
        #   "status": "ok",
        #   "data": {
        #     "id": 1000001,
        #     "type": "spot",
        #     "state": "working",
        #     "list": [
        #       {
        #         "currency": "usdt",
        #         "type": "trade",
        #         "balance": "91.850043797676510303",
        #         "debt": "invalid",
        #         "available": "invalid",
        #         "seq-num": "477"
        #       },
        #       {
        #         "currency": "usdt",
        #         "type": "frozen",
        #         "balance": "5.160000000000000015",
        #         "debt": "invalid",
        #         "available": "invalid",
        #         "seq-num": "477"
        #       },
        #       {
        #         "currency": "poly",
        #         "type": "trade",
        #         "balance": "147.928994082840236",
        #         "debt": "invalid",
        #         "available": "invalid",
        #         "seq-num": "2"
        #       }
        #     ]
        #   }
        # }
        balance_assets = []
        for raw_asset in r["data"]["list"]:
            if raw_asset["type"] == "frozen":
                continue
            asset = self._parse_balance_asset(raw_asset)
            if asset.free == 0:
                continue
            balance_assets.append(asset)
        balance_usd = self._get_balance_value()
        balance = Balance(equity=balance_usd, assets=balance_assets)
        return balance.model_dump()

    def _parse_transfer(self, transfer: dict[str, Any]) -> dict[str, Any]:
        tr = Transfer(
            transferId=transfer["record-id"],
            date=transfer["transact-time"],
            status=TranferStatus.success,
            from_id=transfer["source-id"],
            to_id=transfer["account-id"],
            direction=("in" if transfer["account-id"] == self._account_id else "out"),
            coin=transfer["currency"],
            qty=transfer["transact-amt"],
            info=transfer,
        )
        return tr.model_dump()

    def get_transfer_history(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        **kwargs,
    ) -> list[dict]:
        """
        Return transfer history (in and out) of the current account.
        :see: https://www.htx.com/en-us/opend/newApiPages/?id=7ec4b85b-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        params = {
            "account-id": self._account_id,
            "transact-types": "transfer",
            **kwargs,
        }
        if start_date:
            params.update({"start-time": self.dt_to_unix(start_date)})
        if end_date:
            params.update({"end-time": self.dt_to_unix(end_date)})
        r = self.signed_request("GET", "/v1/account/history", params=params)
        # {'data': [{'account-id': 61775802,
        #         'acct-balance': '30.0000000000000000',
        #         'avail-balance': '30.0000000000000000',
        #         'currency': 'usdt',
        #         'record-id': 1104073401938149557,
        #         'source-id': 3068183988,
        #         'transact-amt': '30.0000000000000000',
        #         'transact-time': 1716821954841,
        #         'transact-type': 'transfer'}],
        # 'status': 'ok'}
        transfers = [self._parse_transfer(tr) for tr in r["data"]]
        return transfers

    # ###########
    # # MARKETS #
    # ###########
    def _parse_market(self, market) -> dict[str, Any]:
        market_obj = Market(
            name=market["symbol"],
            active=market["state"] == "online",
            base=market["bc"],
            info=market,
            min_amt=market["minov"],
            min_qty=market["minoa"],
            precision=market["ap"],
            quote=market["qc"],
            spot=True,
        )
        market = market_obj.model_dump()
        return market

    def get_markets(self, **kwargs) -> list[dict]:
        """
        Retrieves data on all (SPOT/MARGIN) markets.
        :see: https://www.htx.com/en-us/opend/newApiPages/?id=7ec4f5d6-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        params = {**kwargs}
        r = self.request("GET", "/v1/settings/common/market-symbols", params=params)
        # {
        # "status": "ok",
        # "data": [
        #     {
        #     "symbol": "btc3lusdt",
        #     "state": "online",
        #     "bc": "btc3l",
        #     "qc": "usdt",
        #     "pp": 4,
        #     "ap": 4,
        #     "sp": "main",
        #     "vp": 8,
        #     "minoa": 0.01,
        #     "maxoa": 199.0515,
        #     "minov": 5,
        #     "lominoa": 0.01,
        #     "lomaxoa": 199.0515,
        #     "lomaxba": 199.0515,
        #     "lomaxsa": 199.0515,
        #     "smminoa": 0.01,
        #     "blmlt": 1.1,
        #     "slmgt": 0.9,
        #     "smmaxoa": 199.0515,
        #     "bmmaxov": 2500,
        #     "msormlt": 0.1,
        #     "mbormlt": 0.1,
        #     "maxov": 2500,
        #     "u": "btcusdt",
        #     "mfr": 0.035,
        #     "ct": "23:55:00",
        #     "rt": "00:00:00",
        #     "rthr": 4,
        #     "in": 16.3568,
        #     "at": "enabled",
        #     "tags": "etp,nav,holdinglimit,activities"
        #     }
        # ],
        # "ts": "1641880897191",
        # "full": 1
        # }
        markets = [self._parse_market(market) for market in r["data"]]
        return markets

    def get_market_info(self, market: str, **kwargs) -> dict[str, Any]:
        """
        Retrieves data on a specific market.
        :see: https://www.htx.com/en-us/opend/newApiPages/?id=7ec4f5d6-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        if not market:
            raise ValueError(f"`market` cannot be empty, value passed: '{market}'")

        params = {"symbols": market}
        r = self.request("GET", "/v1/settings/common/market-symbols", params=params)
        # {'data': [{'ap': 4,
        #            'at': 'enabled',
        #            'bc': 'eth',
        #            'blmlt': 1.1,
        #            'bmmaxov': 1000000,
        #            'lomaxba': 10000,
        #            'lomaxoa': 10000,
        #            'lomaxsa': 10000,
        #            'lominoa': 0.001,
        #            'lr': 5,
        #            'maxoa': 10000,
        #            'mbormlt': 0.1,
        #            'minoa': 0.001,
        #            'minov': 10,
        #            'msormlt': 0.1,
        #            'pp': 2,
        #            'qc': 'usdt',
        #            'slmgt': 0.9,
        #            'smlr': 3,
        #            'smmaxoa': 500,
        #            'smminoa': 0.001,
        #            'sp': 'main',
        #            'state': 'online',
        #            'symbol': 'ethusdt',
        #            'tags': '',
        #            'vp': 8}],
        #  'full': 1,
        #  'status': 'ok',
        #  'ts': '1717592823163'}
        parsed_market = self._parse_market(r["data"][0])
        return parsed_market

    def get_market_price(self, market: str) -> float:
        """
        Return the current price of a market.
        :see: https://www.htx.com/en-us/opend/newApiPages/?id=7ec4a2cd-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        params = {"symbol": market}
        r = self.request("GET", "/market/detail", params=params)
        # {'ch': 'market.btcusdt.detail',
        #  'status': 'ok',
        #  'tick': {'amount': 4482.995312047257,
        #           'close': 67956.81,
        #           'count': 1252252,
        #           'high': 68921.56,
        #           'id': 342212175986,
        #           'low': 67273.65,
        #           'open': 68122.0,
        #           'version': 342212175986,
        #           'vol': 305856161.36989886},
        #  'ts': 1716988289671}
        return r["tick"]["close"]

    # #########
    # # ORDER #
    # #########
    def _parse_order(self, order: dict[str, Any]) -> dict[str, Any]:
        # handle typos in HTX response
        filled_amount = order.get("filled-amount", order.get("field-amount", 0))
        filled_cash_amount = order.get(
            "filled-cash-amount", order.get("field-cash-amount", 0)
        )
        filled_fees = order.get("filled-fees", order.get("field-fees", 0))

        order_obj = Order(
            orderId=order["id"],
            dt=order["created-at"],
            market=order["symbol"],
            type=order["type"].split("-")[-1],
            side=order["type"].split("-")[0],
            qty=filled_amount,
            filled=filled_amount,
            amount=filled_cash_amount,
            price=order["price"],
            status=self.order_statuses[order["state"]],
            time_in_force=None,
            fee=filled_fees,
            info=order,
        )
        return order_obj.model_dump()

    def place_order(
        self,
        market: str,
        type: Literal["limit", "market"],
        side: Literal["buy", "sell"],
        qty: float,
        price: float | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Place an order.
        :see: https://www.htx.com/en-us/opend/newApiPages/?id=7ec4ee16-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        # qty: for buy market order, it's order value
        if (type.lower() == "market") and (side.lower() == "buy"):
            qty = self.compute_quote_qty(qty, market=market)

        data = {
            "account-id": self._account_id,
            "symbol": market,
            "type": f"{side}-{type}",
            "amount": qty,
            "price": price,
            **kwargs,
        }
        r = self.signed_request(
            http_method="POST",
            url_path="/v1/order/orders/place",
            data=data,
        )
        # {'data': '1086175400829771', 'status': 'ok'}
        order = self.get_order(r["data"])
        if order["price"] == 0:
            order["price"] = self.get_market_price(order["market"])
        return order

    # def _get_order_history(self, **kwargs) -> dict:
    #     """Query order history."""
    #     orders = []
    #     next_page_cursor = ""
    #     while True:
    #         r = self.client.get_order_history(
    #             category="spot", cursor=next_page_cursor, **kwargs
    #         )
    #         orders.extend(r["result"]["list"])
    #         next_page_cursor = r["result"]["nextPageCursor"]
    #         if not next_page_cursor:
    #             break
    #     return orders

    def get_order(self, id: str) -> dict:
        """Get information on an order made by the user.
        :see: https://www.htx.com/en-us/opend/newApiPages/?id=7ec4e31c-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        r = self.signed_request("GET", f"/v1/order/orders/{id}")
        # {'data': {'account-id': 61775802,
        #           'amount': '0.01',
        #           'canceled-at': 0,
        #           'client-order-id': '',
        #           'created-at': 1717085707510,
        #           'field-amount': '0',
        #           'field-cash-amount': '0',
        #           'field-fees': '0',
        #           'finished-at': 0,
        #           'ice-amount': '0',
        #           'id': 1077577805408812,
        #           'is-ice': False,
        #           'market-amount': '0',
        #           'price': '1000',
        #           'source': 'spot-api',
        #           'state': 'submitted',
        #           'symbol': 'ethusdt',
        #           'type': 'buy-limit',
        #           'updated-at': 1717085707510},
        #  'status': 'ok'}
        order = self._parse_order(r["data"])
        return order

    def get_open_orders(self, market: str | None = None, **kwargs) -> list[dict]:
        """
        Get all currently unfilled open orders.
        :see: https://www.htx.com/en-us/opend/newApiPages/?id=7ec4e04b-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        params = {"symbol": market, **kwargs}
        r = self.signed_request(
            http_method="GET", url_path="/v1/order/openOrders", params=params
        )
        # {'data': [{'account-id': 61775802,
        #         'amount': '0.010000000000000000',
        #         'client-order-id': '',
        #         'created-at': 1717085707510,
        #         'filled-amount': '0.0',
        #         'filled-cash-amount': '0.0',
        #         'filled-fees': '0.0',
        #         'ice-amount': '0.0',
        #         'id': 1077577805408812,
        #         'price': '1000.000000000000000000',
        #         'source': 'api',
        #         'state': 'submitted',
        #         'symbol': 'ethusdt',
        #         'type': 'buy-limit'}],
        # 'status': 'ok'}
        orders = [self._parse_order(order) for order in r["data"]]
        return orders

    def cancel_order(self, id: str) -> dict[str, Any]:
        """
        Cancels an open order.
        :see: https://www.htx.com/en-us/opend/newApiPages/?id=7ec4e938-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        r = self.signed_request("POST", f"/v1/order/orders/{id}/submitcancel")
        # {'data': '1077586051442359', 'status': 'ok'}
        order_obj = OrderCancelled(orderId=r["data"], success=(r["status"] == "ok"))
        return order_obj.model_dump()

    def cancel_orders(
        self, market: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """
        Cancel all open orders.
        :see: https://www.htx.com/en-us/opend/newApiPages/?id=7ec4eb66-7773-11ed-9966-0242ac110003
        """  # noqa: E501
        orders = self.get_open_orders(market=market)
        if not orders:
            return []

        data = {"symbol": market, **kwargs}
        self.signed_request("POST", "/v1/order/orders/batchCancelOpenOrders", data=data)
        # {
        # "data":{
        #     "failed-count":0,
        #     "next-id":-1,
        #     "success-count":2
        # },
        # "status":"ok"
        # }
        cancelled_orders = []
        for order in orders:
            cancelled_orders.append(
                OrderCancelled(orderId=order["orderId"], success=True).model_dump()
            )
        return cancelled_orders
