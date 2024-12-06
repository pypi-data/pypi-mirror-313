import hashlib
import hmac
import time
from datetime import datetime
from json import JSONDecodeError
from typing import Any, Literal
from urllib.parse import urlencode

from requests import Response

from crypto_connector.base.errors import (
    BadResponse,
    ExchangeError,
    MissingCredentials,
    OrderNotFound,
)
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


class Binance(Exchange):
    base_url = "https://api.binance.com"
    name = "Binance"
    order_statuses = {
        "NEW": OrderStatus.open,
        "PARTIALLY_FILLED": OrderStatus.open,
        "ACCEPTED": OrderStatus.open,
        "FILLED": OrderStatus.closed,
        "CANCELED": OrderStatus.canceled,
        "CANCELLED": OrderStatus.canceled,
        "PENDING_CANCEL": OrderStatus.canceling,
        "REJECTED": OrderStatus.rejected,
        "EXPIRED": OrderStatus.expired,
        "EXPIRED_IN_MATCH": OrderStatus.expired,
    }
    transfer_statuses = {
        "SUCCESS": TranferStatus.success,
        "PROCESS": TranferStatus.pending,
        "FAILURE": TranferStatus.failed,
    }
    timeframes = {
        "1m": "1m",
        "5m": "5m",
        "15m": "15m",
        "1h": "1h",
        "4h": "4h",
        "1d": "1d",
        "1w": "1w",
        "1M": "1M",
    }

    def __init__(
        self,
        sub_api_key: str | None = None,
        sub_api_secret: str | None = None,
        sub_email: str | None = None,
        master_api_key: str | None = None,
        master_api_secret: str | None = None,
        headers: bool = False,
        **kwargs,
    ) -> None:
        super().__init__()
        self.sub_api_key = sub_api_key
        self.sub_api_secret = sub_api_secret
        self.sub_email = sub_email
        self.master_api_key = master_api_key
        self.master_api_secret = master_api_secret
        self.headers = headers

    @staticmethod
    def get_timestamp() -> int:
        return int(time.time() * 1000)

    @staticmethod
    def _cast_values(params: dict) -> dict:
        upper_params = ["symbol"]
        out = {}
        for key, value in params.items():
            if key in upper_params:
                if isinstance(key, str):
                    out[key] = value.upper()
                else:
                    raise ValueError(f"{key} should be a string.")
            else:
                if isinstance(value, bool):
                    out[key] = str(value).lower()
                else:
                    out[key] = str(value)
        return out

    @staticmethod
    def hash(api_secret: str, query_str: str) -> str:
        hash_obj = hmac.new(
            key=api_secret.encode("utf-8"),
            msg=query_str.encode("utf-8"),
            digestmod=hashlib.sha256,
        )
        return hash_obj.hexdigest()

    @staticmethod
    def _urlencode_dict(query: dict) -> str:
        return urlencode(query, doseq=True)

    def signed_request(
        self,
        http_method: str,
        url_path: str,
        params: dict | None = None,
        data: dict | None = None,
        master: bool = False,
    ) -> Any:
        if (
            (not self.sub_api_key)
            or (not self.sub_api_secret)
            or (not self.sub_email)
            or (not self.master_api_key)
            or (not self.master_api_secret)
        ):
            raise MissingCredentials(
                "To use private endpoints, user must pass credentials."
            )

        if params and data:
            raise ValueError("Can only pass `params` or `data`, but not both.")

        if master:
            api_key = self.master_api_key
            api_secret = self.master_api_secret
        else:
            api_key = self.sub_api_key
            api_secret = self.sub_api_secret

        payload = params or data or {}
        payload.update(
            {"timestamp": self.get_timestamp(), "recvWindow": self.recv_window}
        )
        payload = self._cast_values(self._clean_none_values(payload))
        urlencoded_payload = self._urlencode_dict(payload)
        signature = self.hash(api_secret, query_str=urlencoded_payload)  # type: ignore[arg-type] # noqa: E501
        payload.update({"signature": signature})
        self.session.headers.update({"X-MBX-APIKEY": api_key})
        if http_method == "GET":
            return self.request(http_method, url_path=url_path, params=payload)
        else:
            return self.request(http_method, url_path=url_path, data=payload)

    def handle_exception(self, r: Response) -> None:
        if r.status_code == 200:
            return

        try:
            rjson = r.json()
        except JSONDecodeError:
            raise BadResponse(f"Could not decode response text: {r.text}")

        error = {}
        error["error_code"] = rjson["code"]
        error["msg"] = rjson["msg"]
        if self.headers:
            error["headers"] = r.headers
        raise ExchangeError(error)

    #################
    # EXCHANGE INFO #
    #################
    def get_server_time(self) -> int:
        """
        Fetch the current timestamp in millisecondsfrom the exchange server.
        :see: https://binance-docs.github.io/apidocs/spot/en/#test-connectivity
        """  # noqa: E501
        r = self.request("GET", "/api/v3/time")
        # {
        #   "serverTime": 1499827319559
        # }
        return r.get("serverTime", -1)

    ###########
    # ACCOUNT #
    ###########
    def _parse_api_key_info(self, api_info: dict[str, Any]) -> dict[str, Any]:
        api_obj = API(
            created=api_info["createTime"],
            timestamp=api_info["createTime"],
            spot_enabled=api_info["enableSpotAndMarginTrading"],
            ip_restricted=api_info["ipRestrict"],
            ips=api_info["ipList"],
            info=api_info,
        )
        return api_obj.model_dump()

    def get_api_key_info(self) -> dict[str, Any]:
        """
        Return API KEY info of the current user.
        :see: https://binance-docs.github.io/apidocs/spot/en/#get-api-key-permission-user_data
        """  # noqa: E501
        r = self.signed_request("GET", "/sapi/v1/account/apiRestrictions")
        # {
        #     'ipRestrict': True,
        #     'createTime': 1670109589000,
        #     'enableReading': True,
        #     'enableSpotAndMarginTrading': True,
        #     'enableWithdrawals': False,
        #     'enableInternalTransfer': False,
        #     'enableMargin': False,
        #     'enableFutures': False,
        #     'permitsUniversalTransfer': False,
        #     'enableVanillaOptions': False,
        #     'enablePortfolioMarginTrading': False
        # }
        params = {
            "email": self.sub_email,
            "subAccountApiKey": self.sub_api_key,
        }
        r2 = self.signed_request(
            "GET",
            "/sapi/v1/sub-account/subAccountApi/ipRestriction",
            params=params,
            master=True,
        )
        # {
        #     "ipRestrict": "true",
        #     "ipList": [
        #         "69.210.67.14",
        #         "8.34.21.10"
        #     ],
        #     "updateTime": 1636371437000,
        #     "apiKey": "XXXXX"
        # }
        r["ipList"] = r2["ipList"]
        api_key_info = self._parse_api_key_info(r)
        return api_key_info

    def _get_balance_value(self):
        """
        Get balance value in dollars.
        :see: https://binance-docs.github.io/apidocs/spot/en/#query-user-wallet-balance-user_data
        """  # noqa: E501
        r = self.signed_request("GET", "/sapi/v1/asset/wallet/balance")
        spot_balance_btc = float(
            [balance["balance"] for balance in r if balance["walletName"] == "Spot"][0]
        )
        balance_usd = spot_balance_btc * self.get_market_price("BTCUSDT")
        return balance_usd

    @staticmethod
    def _parse_balance_asset(asset: dict[str, Any]) -> BalanceAsset:
        return BalanceAsset(
            coin=asset["asset"],
            free=asset["free"],
            total=float(asset["free"]) + float(asset["locked"]),
        )

    def get_balance(self) -> dict:
        """
        Query for balance and get the amount of funds available for trading
        or funds locked in orders.
        :see: https://binance-docs.github.io/apidocs/spot/en/#account-information-user_data
        """  # noqa: E501
        params = {"omitZeroBalances": True}
        r = self.signed_request("GET", "/api/v3/account", params=params)
        # {'accountType': 'SPOT',
        # 'balances':
        #   [{'asset': 'BTC', 'free': '0.00000907', 'locked': '0.00000000'},
        #    {'asset': 'ETH', 'free': '0.00006900', 'locked': '0.00000000'},
        #    {'asset': 'USDT', 'free': '19.94000000', 'locked': '0.00000000'},
        #    {'asset': 'UNI', 'free': '0.99900000', 'locked': '0.00000000'}],
        # 'brokered': False,
        # 'buyerCommission': 0,
        # 'canDeposit': True,
        # 'canTrade': True,
        # 'canWithdraw': True,
        # 'commissionRates': {'buyer': '0.00000000',
        #                     'maker': '0.00100000',
        #                     'seller': '0.00000000',
        #                     'taker': '0.00100000'},
        # 'makerCommission': 10,
        # 'permissions': ['TRD_GRP_011'],
        # 'preventSor': False,
        # 'requireSelfTradePrevention': False,
        # 'sellerCommission': 0,
        # 'takerCommission': 10,
        # 'uid': 526318869,
        # 'updateTime': 1718115238667}
        balance_assets = []
        for raw_asset in r["balances"]:
            asset = self._parse_balance_asset(raw_asset)
            balance_assets.append(asset)
        balance_usd = self._get_balance_value()
        balance = Balance(equity=balance_usd, assets=balance_assets)
        return balance.model_dump()

    def _parse_transfer(self, transfer: dict[str, Any]) -> dict[str, Any]:
        tr = Transfer(
            transferId=transfer["tranId"],
            date=transfer["time"],
            status=self.transfer_statuses[transfer["status"]],
            from_id=transfer["from"],
            to_id=transfer["to"],
            direction="in" if transfer["to"] == self.sub_email else "out",
            coin=transfer["asset"],
            qty=transfer["qty"],
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
        :see: https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-spot-asset-transfer-history-for-master-account
        """  # noqa: E501
        params = {"toEmail": self.sub_email, **kwargs}
        if start_date:
            params.update({"startTime": self.dt_to_unix(start_date)})
        if end_date:
            params.update({"endTime": self.dt_to_unix(end_date)})
        r = self.signed_request(
            "GET",
            "/sapi/v1/sub-account/sub/transfer/history",
            params=params,
            master=True,
        )
        # [{'asset': 'USDT',
        # 'from': 'xxx@xxx.com',
        # 'qty': '30.00000000',
        # 'status': 'SUCCESS',
        # 'time': 1716820838000,
        # 'to': 'yyy@yyy.com',
        # 'tranId': 175189153797}]
        transfers = [self._parse_transfer(tr) for tr in r]
        return transfers

    ###########
    # MARKETS #
    ###########
    def _parse_market(self, market) -> dict[str, Any]:
        new_filters = {item["filterType"]: item for item in market["filters"]}

        market_obj = Market(
            name=market["symbol"],
            active=market["status"] == "TRADING",
            base=market["baseAsset"],
            info=market,
            min_amt=float(new_filters["NOTIONAL"]["minNotional"]),
            min_qty=float(new_filters["LOT_SIZE"]["minQty"]),
            precision=self.decimal_places(float(new_filters["LOT_SIZE"]["stepSize"])),
            quote=market["quoteAsset"],
            spot=market["isSpotTradingAllowed"],
        )
        return market_obj.model_dump()

    def get_markets(self, **kwargs) -> list[dict]:
        """
        Retrieve data on all SPOT markets.
        :see: https://binance-docs.github.io/apidocs/spot/en/#exchange-information
        """  # noqa: E501
        params = {"permissions": "SPOT", **kwargs}
        r = self.request("GET", "/api/v3/exchangeInfo", params=params)
        # {'active': True,
        # 'base': 'ETH',
        # 'info': {'allowTrailingStop': True,
        #         'allowedSelfTradePreventionModes': ['EXPIRE_TAKER',
        #                                             'EXPIRE_MAKER',
        #                                             'EXPIRE_BOTH'],
        #         'baseAsset': 'ETH',
        #         'baseAssetPrecision': 8,
        #         'baseCommissionPrecision': 8,
        #         'cancelReplaceAllowed': True,
        #         'defaultSelfTradePreventionMode': 'EXPIRE_MAKER',
        #         'filters': [{'filterType': 'PRICE_FILTER',
        #                     'maxPrice': '1000000.00000000',
        #                     'minPrice': '0.01000000',
        #                     'tickSize': '0.01000000'},
        #                     {'filterType': 'LOT_SIZE',
        #                     'maxQty': '9000.00000000',
        #                     'minQty': '0.00010000',
        #                     'stepSize': '0.00010000'},
        #                     {'filterType': 'ICEBERG_PARTS', 'limit': 10},
        #                     {'filterType': 'MARKET_LOT_SIZE',
        #                     'maxQty': '2040.56915833',
        #                     'minQty': '0.00000000',
        #                     'stepSize': '0.00000000'},
        #                     {'filterType': 'TRAILING_DELTA',
        #                     'maxTrailingAboveDelta': 2000,
        #                     'maxTrailingBelowDelta': 2000,
        #                     'minTrailingAboveDelta': 10,
        #                     'minTrailingBelowDelta': 10},
        #                     {'askMultiplierDown': '0.2',
        #                     'askMultiplierUp': '5',
        #                     'avgPriceMins': 5,
        #                     'bidMultiplierDown': '0.2',
        #                     'bidMultiplierUp': '5',
        #                     'filterType': 'PERCENT_PRICE_BY_SIDE'},
        #                     {'applyMaxToMarket': False,
        #                     'applyMinToMarket': True,
        #                     'avgPriceMins': 5,
        #                     'filterType': 'NOTIONAL',
        #                     'maxNotional': '9000000.00000000',
        #                     'minNotional': '5.00000000'},
        #                     {'filterType': 'MAX_NUM_ORDERS', 'maxNumOrders': 200},  # noqa: E501
        #                     {'filterType': 'MAX_NUM_ALGO_ORDERS',
        #                     'maxNumAlgoOrders': 5}],
        #         'icebergAllowed': True,
        #         'isMarginTradingAllowed': True,
        #         'isSpotTradingAllowed': True,
        #         'ocoAllowed': True,
        #         'orderTypes': ['LIMIT',
        #                         'LIMIT_MAKER',
        #                         'MARKET',
        #                         'STOP_LOSS_LIMIT',
        #                         'TAKE_PROFIT_LIMIT'],
        #         'otoAllowed': False,
        #         'permissionSets': [['SPOT',
        #                             'MARGIN',
        #                             'TRD_GRP_004',
        #                             'TRD_GRP_005',
        #                             'TRD_GRP_006',
        #                             'TRD_GRP_009',
        #                             'TRD_GRP_010',
        #                             'TRD_GRP_011',
        #                             'TRD_GRP_012',
        #                             'TRD_GRP_013',
        #                             'TRD_GRP_014',
        #                             'TRD_GRP_015',
        #                             'TRD_GRP_016',
        #                             'TRD_GRP_017',
        #                             'TRD_GRP_018',
        #                             'TRD_GRP_019',
        #                             'TRD_GRP_020',
        #                             'TRD_GRP_021',
        #                             'TRD_GRP_022',
        #                             'TRD_GRP_023',
        #                             'TRD_GRP_024',
        #                             'TRD_GRP_025']],
        #         'permissions': [],
        #         'quoteAsset': 'USDT',
        #         'quoteAssetPrecision': 8,
        #         'quoteCommissionPrecision': 8,
        #         'quoteOrderQtyMarketAllowed': True,
        #         'quotePrecision': 8,
        #         'status': 'TRADING',
        #         'symbol': 'ETHUSDT'},
        # 'min_amt': 0.01,
        # 'min_qty': 0.0001,
        # 'name': 'ETHUSDT',
        # 'precision': 4,
        # 'quote': 'USDT',
        # 'spot': True}
        markets = [self._parse_market(market) for market in r["symbols"]]
        return markets

    def get_market_info(self, market: str, **kwargs) -> dict[str, Any]:
        """
        Retrieve data on a specific market.
        :see: https://binance-docs.github.io/apidocs/spot/en/#exchange-information
        """  # noqa: E501
        if not market:
            raise ValueError(f"`market` cannot be empty, value passed: '{market}'")

        params = {"symbol": market, **kwargs}
        r = self.request("GET", "/api/v3/exchangeInfo", params=params)
        parsed_market: dict[str, Any] = self._parse_market(r["symbols"][0])
        return parsed_market

    @staticmethod
    def _parse_ohlcv(data: list[list]) -> list[list]:
        return [
            [
                int(x[0]),
                float(x[1]),
                float(x[2]),
                float(x[3]),
                float(x[4]),
                float(x[5]),
            ]
            for x in data
        ]

    def get_ohlcv(
        self,
        market: str,
        timeframe: str = "1d",
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        **kwargs,
    ) -> list[list]:
        """
        Fetch historical candlestick data containing
        the open, high, low, and close price, and the volume of a market.
        :see: https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
        """  # noqa: E501
        params = {
            "symbol": market,
            "interval": timeframe,
            "limit": kwargs.get("limit", 200),
            **kwargs,
        }
        if start_date:
            params.update({"startTime": self.dt_to_unix(start_date)})
        if end_date:
            params.update({"endTime": self.dt_to_unix(end_date)})

        r = self.request("GET", "/api/v3/klines", params=params)
        # [
        #   [
        #     1499040000000,      // Kline open time
        #     "0.01634790",       // Open price
        #     "0.80000000",       // High price
        #     "0.01575800",       // Low price
        #     "0.01577100",       // Close price
        #     "148976.11427815",  // Volume
        #     1499644799999,      // Kline Close time
        #     "2434.19055334",    // Quote asset volume
        #     308,                // Number of trades
        #     "1756.87402397",    // Taker buy base asset volume
        #     "28.46694368",      // Taker buy quote asset volume
        #     "0"                 // Unused field, ignore.
        #   ]
        # ]
        ohlcv = self._parse_ohlcv(r)
        return ohlcv

    def get_market_price(self, market: str) -> float:
        """
        Return the current price of a market.
        see: https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker
        """  # noqa: E501
        params = {"symbol": market}
        r = self.request("GET", "/api/v3/ticker/price", params=params)
        # {"symbol": "LTCBTC", "price": "4.00000200"}
        return float(r["price"])

    #########
    # ORDER #
    #########
    def _parse_order(self, order: dict[str, Any]) -> dict[str, Any]:
        order_obj = Order(
            orderId=order["orderId"],
            dt=order["time"],
            market=order["symbol"],
            type=order["type"].lower(),
            side=order["side"].lower(),
            qty=order["origQty"],
            filled=order["executedQty"],
            amount=order["cummulativeQuoteQty"],
            price=order["price"],
            status=self.order_statuses[order["status"]],
            time_in_force=order["timeInForce"],
            fee=None,
            info=order,
        )
        return order_obj.model_dump()

    def get_order(self, id: str, market: str, **kwargs) -> dict[str, Any]:
        """
        Get information on an order made by the user.
        :see: https://binance-docs.github.io/apidocs/spot/en/#query-order-user_data
        """  # noqa: E501
        params = {"orderId": id, "symbol": market, **kwargs}
        r = self.signed_request("GET", "/api/v3/order", params=params)
        # {'clientOrderId': 'nOIUBuoybuyBUOYBbJnGfT',
        # 'cummulativeQuoteQty': '0.00000000',
        # 'executedQty': '0.00000000',
        # 'icebergQty': '0.00000000',
        # 'isWorking': True,
        # 'orderId': 17967599781,
        # 'orderListId': -1,
        # 'origQty': '0.01000000',
        # 'origQuoteOrderQty': '0.00000000',
        # 'price': '1000.00000000',
        # 'selfTradePreventionMode': 'EXPIRE_MAKER',
        # 'side': 'BUY',
        # 'status': 'NEW',
        # 'stopPrice': '0.00000000',
        # 'symbol': 'ETHUSDT',
        # 'time': 1717160522940,
        # 'timeInForce': 'GTC',
        # 'type': 'LIMIT',
        # 'updateTime': 1717160522940,
        # 'workingTime': 1717160522940}
        order = self._parse_order(r)
        return order

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
        :see: https://binance-docs.github.io/apidocs/spot/en/#new-order-trade
        """
        time_in_force = None
        if type.lower() == "limit":
            time_in_force = kwargs.get("timeInForce", "GTC")

        data = {
            "symbol": market,
            "side": side,
            "type": type,
            "quantity": qty,
            "price": price,
            "timeInForce": time_in_force,
            **kwargs,
        }
        data.update(kwargs)
        r = self.signed_request("POST", "/api/v3/order", data=data)
        # {'clientOrderId': 'YUBKHJgbUYGVBYUGFVByuj',
        #  'cummulativeQuoteQty': '0.00000000',
        #  'executedQty': '0.00000000',
        #  'fills': [],
        #  'orderId': 17967599781,
        #  'orderListId': -1,
        #  'origQty': '0.01000000',
        #  'price': '1000.00000000',
        #  'selfTradePreventionMode': 'EXPIRE_MAKER',
        #  'side': 'BUY',
        #  'status': 'NEW',
        #  'symbol': 'ETHUSDT',
        #  'timeInForce': 'GTC',
        #  'transactTime': 1717160522940,
        #  'type': 'LIMIT',
        #  'workingTime': 1717160522940}
        order = self.get_order(id=r["orderId"], market=r["symbol"])
        return order

    def get_open_orders(
        self, market: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """
        Get all currently unfilled open orders.
        :see: https://binance-docs.github.io/apidocs/spot/en/#current-open-orders-user_data
        """  # noqa: E501
        params = {"symbol": market, **kwargs}
        r = self.signed_request("GET", "/api/v3/openOrders", params=params)
        # [{'clientOrderId': 'NIOUniunui45BNIUjhbjHg',
        #   'cummulativeQuoteQty': '0.00000000',
        #   'executedQty': '0.00000000',
        #   'icebergQty': '0.00000000',
        #   'isWorking': True,
        #   'orderId': 17964589418,
        #   'orderListId': -1,
        #   'origQty': '0.01000000',
        #   'origQuoteOrderQty': '0.00000000',
        #   'price': '1000.00000000',
        #   'selfTradePreventionMode': 'EXPIRE_MAKER',
        #   'side': 'BUY',
        #   'status': 'NEW',
        #   'stopPrice': '0.00000000',
        #   'symbol': 'ETHUSDT',
        #   'time': 1717145002434,
        #   'timeInForce': 'GTC',
        #   'type': 'LIMIT',
        #   'updateTime': 1717145002434,
        #   'workingTime': 1717145002434}]
        orders = [self._parse_order(order) for order in r]
        return orders

    def cancel_order(self, id: str, **kwargs) -> dict[str, Any]:
        """
        Cancel an open order.
        :see: https://binance-docs.github.io/apidocs/spot/en/#cancel-order-trade
        """  # noqa: E501
        orders = self.get_open_orders()
        market = [order["market"] for order in orders if order["orderId"] == id]
        if not market:
            raise OrderNotFound(f"Could not find an open order with this id '{id}'")

        data = {"orderId": id, "symbol": market[0], **kwargs}
        r = self.signed_request("DELETE", "/api/v3/order", data=data)
        # {'clientOrderId': 'niluBUYbuykvbUYLB156NU',
        #  'cummulativeQuoteQty': '0.00000000',
        #  'executedQty': '0.00000000',
        #  'orderId': 18007366952,
        #  'orderListId': -1,
        #  'origClientOrderId': 'bIULYGBjkhb6K7GKuyvuyv',
        #  'origQty': '0.01000000',
        #  'price': '1000.00000000',
        #  'selfTradePreventionMode': 'EXPIRE_MAKER',
        #  'side': 'BUY',
        #  'status': 'CANCELED',
        #  'symbol': 'ETHUSDT',
        #  'timeInForce': 'GTC',
        #  'transactTime': 1717505772211,
        #  'type': 'LIMIT'}
        order_obj = OrderCancelled(
            orderId=r["orderId"], success=(r["status"] == "CANCELED")
        )
        return order_obj.model_dump()

    def cancel_orders(
        self, market: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """
        Cancel all open orders.
        :see: https://binance-docs.github.io/apidocs/spot/en/#cancel-all-open-orders-on-a-symbol-trade
        """  # noqa: E501
        orders = self.get_open_orders()
        markets = [order["market"] for order in orders]
        resp = []
        data: dict[str, Any] = {}
        if market:
            if market not in markets:
                return []
            data = {"symbol": market}
            resp = self.signed_request("DELETE", "/api/v3/openOrders", data=data)
        else:
            for market in markets:
                data = {"symbol": market}
                r = self.signed_request("DELETE", "/api/v3/openOrders", data=data)
                resp.extend(r)

        cancelled_orders = []
        for order in resp:
            cancelled_orders.append(
                OrderCancelled(
                    orderId=order["orderId"], success=order["status"] == "CANCELED"
                ).model_dump()
            )
        return cancelled_orders
