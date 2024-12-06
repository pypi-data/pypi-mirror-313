from decimal import Decimal
from freezegun import freeze_time
from pyqqq.data.daily import get_all_ohlcv_for_date, get_ohlcv_by_codes_for_period
from pyqqq.data.minutes import get_all_day_data
from pyqqq.datatypes import OrderType, OrderSide
from pyqqq.utils.market_schedule import get_last_trading_day
import asyncio
import datetime as dtm
import importlib
import os
import pandas as pd
import yaml


class DummyBroker:
    def __init__(self):
        self.account_info = {}
        self.pending_orders = []
        self.positions = []

        self.account_info = {
            "account_no": "12345",
            "total_balance": 1000000,
            "purchase_amount": 0,
            "evaluated_amount": 0,
            "pnl_amount": 0,
            "pnl_rate": Decimal('0.0'),
        }

    def get_account(self):
        return self.account_info

    def get_possible_quantity(
        self, asset_code: str, order_type: OrderType, price: int = 0
    ):
        today = dtm.date.today()
        prices_df = get_all_ohlcv_for_date(today)
        cash = self.account_info["total_balance"]
        price = int(prices_df.loc[asset_code, "close"])
        quantity = cash // price
        amount = price * quantity

        return {
            "investable_cash": cash,
            "reuseable_cash": 0,
            "price": prices_df.loc[asset_code, "close"],
            "quantity": quantity,
            "amount": amount,
        }

    def get_positions(self):
        return []

    def get_historical_daily_data(
        self,
        asset_code: str,
        first_date: dtm.date,
        last_date: dtm.date,
        adjusted_price: bool = True,
    ):
        dfs = get_ohlcv_by_codes_for_period(
            [asset_code], first_date, last_date, adjusted_price
        )
        return dfs[asset_code]

    def get_today_minute_data(self, asset_code):
        dfs = get_all_day_data(dtm.date.today(), [asset_code])
        return dfs[asset_code]

    def get_price(self, asset_code):
        today = dtm.date.today()

        prices_df = get_all_ohlcv_for_date(today)
        series = prices_df.loc[asset_code]
        data = {
            "open_price": series["open"],
            "high_price": series["high"],
            "low_price": series["low"],
            "current_price": series["close"],
            "volume": series["volume"],
            "min_price": series["open"] * 0.7,
            "max_price": series["open"] * 1.3,
            "diff": series["diff"],
            "diff_rate": series["diff_rate"],
        }
        return data

    def get_price_for_multiple_stock(self, asset_codes):
        dataset = []
        today = dtm.date.today()
        prices_df = get_all_ohlcv_for_date(today)
        print(today, prices_df)

        for asset_code in asset_codes:
            series = prices_df.loc[asset_code]
            data = {
                "code": asset_code,
                "open_price": series["open"],
                "high_price": series["high"],
                "low_price": series["low"],
                "current_price": series["close"],
                "volume": series["volume"],
                "max_price": series["open"] * 0.7,
                "min_price": series["open"] * 1.3,
                "diff": series["diff"],
                "diff_rate": series["diff_rate"],
            }
            dataset.append(data)

        df = pd.DataFrame(dataset)
        df.set_index("code", inplace=True)
        return df

    def create_order(
        self,
        asset_code: str,
        side: OrderSide,
        quantity: int,
        order_type: OrderType,
        price: int = 0,
    ):
        raise NotImplementedError

    def update_order(
        self,
        org_order_no: str,
        asset_code: str,
        order_type: OrderType,
        price: int,
        quantity: int = 0,
    ):
        raise NotImplementedError

    def cancel_order(self, org_order_no: str, asset_code: str, quantity: int):
        raise NotImplementedError

    def get_pending_orders(self):
        return []

    def get_today_order_history(self):
        return []

    def get_tick_data(self):
        return []


async def maybe_awaitable(result):
    if asyncio.iscoroutine(result) or isinstance(result, asyncio.Future):
        return await result
    else:
        return result


def has_hook(module, func_name: str) -> bool:
    """사용자가 구현한 함수가 있는지 확인"""
    return hasattr(module, func_name) and callable(
        getattr(module, func_name)
    )


async def test_hook(filename):
    app = None
    if os.path.exists("app.yaml"):
        with open("app.yaml", "r") as f:
            app = yaml.safe_load(f)

    if app is None or app.get("executor") != "hook":
        return

    spec = importlib.util.spec_from_file_location("hook", filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    last_trading_day = get_last_trading_day()

    with freeze_time(last_trading_day):
        broker = DummyBroker()
        account_info = broker.get_account()
        pending_orders = broker.get_pending_orders()
        positions = broker.get_positions()

        if has_hook(module, "on_initialize"):
            await maybe_awaitable(module.on_initialize())
        if has_hook(module, "on_market_open"):
            await maybe_awaitable(module.on_market_open(account_info, pending_orders, positions, broker))
        if has_hook(module, "trade_func"):
            await maybe_awaitable(module.trade_func(account_info, pending_orders, positions, broker))
        if has_hook(module, "on_market_close"):
            await maybe_awaitable(module.on_market_close(account_info, pending_orders, positions, broker))
