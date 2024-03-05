from constants import *
from session_singleton import Session
from utils import UrlHelper
import re
from itertools import chain
import datetime
from decimal import Decimal

from utils import subclass_method, coerce_method_params, date_regex
from stock_trade import StockTrade
from option_trade import OptionTrade


class OpenOrder(object):
    @coerce_method_params
    def __init__(
        self: object,
        order_id: int,
        cancel_fn: object,
        symbol: str,
        quantity: int,
        order_price: Decimal,
        trade_type: str
    ):
        self.order_id = order_id
        self.cancel_fn = cancel_fn
        # strptime with %-m/%-d/%Y %-I:%M:%S %p SHOULD WORK
        # because it looks like this: 4/1/2019 11:10:35 PM
        self.trade_type = trade_type
        self.symbol = symbol
        self.quantity = quantity
        self.order_price = order_price
        self.active = True

    def cancel(self):        
        cancelled =  self.cancel_fn()
        if cancelled:
            self.active = False
            print("Order ID %s cancelled!" % self.order_id)



class SubPortfolio(object):
    def __init__(self,portfolio_id,market_value,day_gain_dollar,day_gain_percent,total_gain_dollar,total_gain_percent):
        self.portfolio_id = portfolio_id
        self.market_value = market_value
        self.day_gain_dollar = day_gain_dollar
        self.day_gain_percent = day_gain_percent
        self.total_gain_dollar = total_gain_dollar
        self.total_gain_percent = total_gain_percent

class Portfolio(object):
    allowable_portfolios = {
        'LongPosition': ['StockPortfolio'],
        'ShortPosition': ['ShortPortfolio'],
        'OptionPosition': ['OptionPortfolio']
    }
    @coerce_method_params
    def __init__(
        self: object,
        portfolio_id: int,
        game_id: int,
        game_name: str,
        account_value: Decimal,
        buying_power: Decimal,
        cash: Decimal,
        annual_return_pct: Decimal,
        stock_portfolio: object,
        short_portfolio: object,
        option_portfolio: object,
        open_orders: object
    ):
        self.portfolio_id = portfolio_id
        self.game_id = game_id
        self.game_name = game_name
        self.account_value = account_value
        self.buying_power = buying_power
        self.cash = cash
        self.annual_return_pct = annual_return_pct

        self._stock_portfolio = stock_portfolio
        self._short_portfolio = short_portfolio
        self._option_portfolio = option_portfolio
        self._open_orders = open_orders

    @classmethod
    def _validate_append(cls, portfolio, position):
        portfolio_type = type(portfolio).__name__
        position_type = type(position).__name__
        assert_val = (
            portfolio_type in cls.allowable_portfolios[position_type])
        assert assert_val, "Cannot insert a %s into a %s" % (
            position_type, portfolio_type)

    @property
    @subclass_method
    def total_value(self):
        return sum((p.total_value) for p in self)

    @property
    @subclass_method
    def total_change(self):
        return sum(p.total_change for p in self)

    def sfind(self, sym):
        stfn = self.stock_portfolio.find
        shfn = self.short_portfolio.find
        opfn = self.option_portfolio.find

        for position in [opfn(sym), shfn(sym), stfn(sym)]:
            if position is not None:
                yield position

    def find(self, symbol):
        if type(self).__name__ == 'Portfolio':
            return self.sfind(symbol)

        for position in self:
            if position.symbol.upper() == symbol.upper():
                return position

    def append(self, item):
        self.__class__._validate_append(self, item)
        super().append(item)

    @property
    def stock_portfolio(self):
        return self._stock_portfolio

    @property
    def short_portfolio(self):
        return self._short_portfolio

    @property
    def option_portfolio(self):
        return self._option_portfolio
    
    @property
    def open_orders(self):
        orders = []
        for oo in self._open_orders:
            if oo.active:
                orders.append(oo)

        return orders


class StockPortfolio(SubPortfolio, list):
    def __init__(self, positions=[], **kwargs):
        super().__init__(**kwargs)
        for p in positions:
            self.append(p)

        self.positions = self


class ShortPortfolio(SubPortfolio, list):
    def __init__(self, positions=[], **kwargs):
        super().__init__(**kwargs)
        for p in positions:
            self.append(p)


class OptionPortfolio(SubPortfolio, list):
    def __init__(self, positions=[], **kwargs):
        
        for p in positions:
            self.append(p)

    def find(self, symbol):
        for pos in self:
            if pos.underlying.upper() == symbol.upper():
                return pos

    def find_exact(self, symbol):
        for pos in self:
            if pos.symbol.upper() == symbol.upper():
                return pos


class Position(object):
    @coerce_method_params
    def __init__(
            self: object,
            symbol: str,
            quantity: int,
            description: str,
            purchase_price: Decimal,
            market_value: Decimal,
            day_gain_dollar: Decimal,
            day_gain_percent: Decimal,
            total_gain_dollar: Decimal,
            total_gain_percent: Decimal
        ):

        self.symbol = symbol
        self.quantity = quantity
        self.description = description
        self.purchase_price = purchase_price
        self.market_value = market_value
        self.day_gain_dollar = day_gain_dollar
        self.day_gain_percent = day_gain_percent
        self.total_gain_dollar = total_gain_dollar
        self.total_gain_percent = total_gain_percent
        self.current_price = self.market_value / self.quantity



class LongPosition(Position):
    stock_type_assertion = 'long'

    def __init__(self, quote_fn, stock_type, **kwargs):
        super().__init__(**kwargs)
        assert(stock_type == self.stock_type_assertion)
        self.stock_type = stock_type
        self._quote_fn = quote_fn
        self._quote = None

    @property
    def change(self):
        return self.current_price - self.purchase_price

    @property
    def quote(self):
        return self._quote_fn()

    def sell(self, **trade_kwargs):
        trade_kwargs['symbol'] = self.symbol
        trade_kwargs.setdefault('quantity', self.quantity)
        trade_kwargs['trade_type'] = 'sell'
        return StockTrade(**trade_kwargs)


class ShortPosition(Position):
    stock_type_assertion = 'short'

    def __init__(self, quote_fn, stock_type, **kwargs):
        super().__init__(**kwargs)
        assert stock_type == self.stock_type_assertion
        self.stock_type = stock_type
        self._quote_fn = quote_fn
        self._quote = None

    # note that short positions value go up when the underlying security goes down
    @property
    def change(self):
        return self.purchase_price - self.current_price

    @property
    def quote(self):
        return self._quote_fn()
    

    def cover(self, **trade_kwargs):
        trade_kwargs['symbol'] = self.symbol
        trade_kwargs.setdefault('quantity', self.quantity)
        trade_kwargs['trade_type'] = 'buy_to_cover'
        return StockTrade(**trade_kwargs)


class OptionPosition(Position):
    stock_type_assertion = 'option'

    def __init__(self, option_contract, quote_fn, stock_type, **kwargs):
        super().__init__(**kwargs)
        assert stock_type == self.stock_type_assertion
        self._quote_fn = quote_fn
        self._contract = option_contract
        self.underlying = self._contract.base_symbol
        self.stock_type = stock_type
        self.strike_price = self._contract.strike_price
        self.contract_type = self._contract.contract_type
        self.expiration = self._contract.expiration
        self._is_expired = None
        self._quote_fn = quote_fn
        self._quote = None

    @property
    def contract(self):
        for val in self._contract.lazy_values():
            if val is None:
                return self.quote
        return self._contract

    @property
    def quote(self):
        if self._quote is None:
            self._contract = self._quote_fn()
            self._quote = True
        return self._contract

    @property
    def is_expired(self):
        if self._is_expired is None:
            self._is_expired = False
            if datetime.date.today() > self.expiration:
                self._is_expired = True

        return self._is_expired

    def close(self, **trade_kwargs):
        trade_kwargs['contract'] = self.contract
        trade_kwargs.setdefault('quantity', self.quantity)
        trade_kwargs['trade_type'] = 'sell to close'
        return OptionTrade(**trade_kwargs)


class StockQuote(object):
    @coerce_method_params
    def __init__(
        self: object,
        symbol: str,
        name: str,
        exchange: str,
        previous_close: Decimal,
        bid: Decimal,
        ask: Decimal,
        volume: int,
        day_high: Decimal,
        day_low: Decimal

    ):
        self.symbol = symbol
        self.name = name
        self.last = ask
        self.exchange = exchange
        self.volume = volume
        self.day_high = day_high
        self.day_low = day_low
        self.previous_close = previous_close
        self.bid = bid
        self.ask = ask
        self.last = self.ask
        self.change = self.ask - self.previous_close
        self.change_percent = round(self.change / self.last * 100,2)
