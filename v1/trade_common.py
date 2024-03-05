import re
from titlecase import titlecase
import copy
from ratelimit import limits, sleep_and_retry
from utils import UrlHelper,TradeExceedsMaxSharesException
from session_singleton import Session
from lxml import html
from constants import *
import warnings
from queries import Queries
import json
import warnings


class InvalidTradeTypeException(Exception):
    pass


class InvalidOrderTypeException(Exception):
    pass


class InvalidOrderDurationException(Exception):
    pass


class TradeNotValidatedException(Exception):
    pass

class DuplicateTradeException(Exception):
    pass


# def convert_trade_props(func):
#     @wraps(func)
#     def wrapper(self, *arg, **kwargs):
#         copy_kwargs = copy.deepcopy(kwargs)
#         copy_kwargs.update(dict(zip(func.__code__.co_varnames[1:], args)))
#         trade_type = copy_kwargs.get('trade_type', None)
#         order_type = copy_kwargs.get('order_type', None)
#         duration = copy_kwargs.get('duration', None)

#         if trade_type is not None and type(trade_type) == str:
#             copy_kwargs['trade_type'] = TransactionType(trade_type)
#         if order_type is not None and type(order_type) == str:
#             copy_kwargs['order_type'] = OrderLimit.fromstring(order_type)
#         if duration is not None and type(duration) == str:
#             copy_kwargs['duration'] = Expiration(duration)

#         return func(self, **copy_kwrags)
#     return wrapper


class TransactionType(str):
    @classmethod
    def BUY_TO_OPEN(cls):
        return cls('BUY_TO_OPEN')

    @classmethod
    def SELL_TO_CLOSE(cls):
        return cls('SELL_TO_CLOSE')

    @classmethod
    def BUY(cls):
        return cls('BUY')

    @classmethod
    def SELL(cls):
        return cls('SELL')

    @classmethod
    def SELL_SHORT(cls):
        return cls('SELL_SHORT')

    @classmethod
    def BUY_TO_COVER(cls):
        return cls('BUY_TO_COVER')

class OrderLimit(dict):
    @classmethod
    def MARKET(cls):
        return cls({'limit': None})
    
    @classmethod
    def LIMIT(cls,price):
        return cls({'limit': int(price)})
    
    @classmethod
    def STOP(cls,price):
        return cls({'stop': int(price)})
    
    @classmethod
    def TRAILING_STOP(cls,val):
        val = str(val)
        dict_val = {'trailingStop': None}
        pct_regex = re.search(r'^(\d+)\%$',val)
        dol_regex = re.search(r'^\$?(\d+)$',val)
        if pct_regex:
            dict_val['trailingStop'] = {'percentage': int(pct_regex.group(1))}
            return cls(dict_val)
        
        elif dol_regex:
            dict_val['trailingStop'] = {'price': int(dol_regex.group(1))}
            return cls(dict_val)
        
        else:
            raise InvalidOrderTypeException("Invalid argument for TRAILING_STOP.  Call with OrderType.TRAILING_STOP('5%') or OrderType.TRAILING_STOP(5)")

class Expiration(dict):
    @classmethod
    def END_OF_DAY(cls):
        return cls({'expiryType':"END_OF_DAY"})
    
    @classmethod
    def GOOD_UNTIL_CANCELLED(cls):
        return cls({'expiryType':'GOOD_UNTIL_CANCELLED'})
    
    @classmethod
    def DAY_ONLY(cls):
        return cls.END_OF_DAY()


class Trade(object):
    pass

class StockTrade(Trade):
    def __init__(
            self,
            portfolio_id,
            symbol,
            quantity,
            transaction_type,
            order_limit=OrderLimit.MARKET(),
            expiration=Expiration.END_OF_DAY()):
        
        self._portfolio_id = portfolio_id
        self._symbol = symbol
        self._quantity = quantity
        self._transaction_type = transaction_type
        self._order_limit = order_limit
        self._expiration = expiration
        self._validated = False
        self._executed = False

    @property
    def portfolio_id(self):
        return self._portfolio_id
    
    @portfolio_id.setter
    def portfolio_id(self,portfolio_id):
        self._validated = False
        self._portfolio_id = portfolio_id

    @property
    def symbol(self):
        return self._symbol
    
    @symbol.setter
    def symbol(self,symbol):
        self._validated = False
        self._symbol = symbol

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self,quantity):
        self._validated = False
        self._quantity = quantity

    @property
    def transaction_type(self):
        return self._transaction_type
    
    @transaction_type.setter
    def transaction_type(self,transaction_type):
        self._validated = False
        self._transaction_type = transaction_type
    
    @property
    def order_limit(self):
        return self._order_limit
    
    @order_limit.setter
    def order_limit(self,order_limit):
        self._validated = False
        self._order_limit = order_limit

    @property
    def expiration(self):
        return self._expiration
    
    @expiration.setter
    def expiration(self,expiration):
        self._validated = False
        self._expiration = expiration

    def validate(self):
        session = Session()
        resp = session.post(API_URL,data=Queries.validate_stock_trade(self))
        resp.raise_for_status()
        resp_json = json.loads(resp.text)
        if resp_json.get('errors',None) is not None:
            for error in resp_json['errors']:
                warnings.warn(error['message'])
            self._validated = False
            return

        elif resp_json['data']['previewStockTrade'].get('errorMessages',None) is not None:
            errors = resp_json['data']['previewStockTrade']['errorMessages']
            for error in errors:
                warnings.warn(error)
            self._validated = False
            return
        
        print("Trade validated!")
        self._validated = True

    def execute(self):
        if not self._validated:
            raise TradeNotValidatedException("Trade not validated!")
        
        if self._executed:
            raise DuplicateTradeException("Trade already executed.  Call reset() on Trade object to submit trade again")
        
        session = Session()
        resp = session.post(API_URL, data=Queries.execute_stock_trade(self))

        resp.raise_for_status()
        resp_json = json.loads(resp.text)
        if resp_json.get('errors',None) is not None:
            for error in resp_json['errors']:
                warnings.warn(error['message'])
            self._executed = False
            self._validated = False
            return

        elif resp_json['data']['submitStockTrade'].get('errorMessages',None) is not None:
            errors = resp_json['data']['previewStockTrade']['errorMessages']
            for error in errors:
                warnings.warn(error)
            self._executed = False
            self._validated = False
            return
        
        self._executed = True
        print("Trade executed!")

    def reset(self):
        self._validated = False
        self._executed = False
       


# class Trade(object):
#     def __init__(
#             self,
#             symbol,
#             quantity,
#             trade_type,
#             order_type=OrderLimit.MARKET(),
#             duration=Expiration.GOOD_UNTIL_CANCELLED,
#             send_email=True):

#         if type(trade_type) == str:
#             trade_type = TradeType(trade_type)

#         if type(order_type) == str:
#             order_type = oR.fromstring(order_type)

#         if type(duration) == str:
#             duration = Duration(duration)

#         self.form_data = {
#             'isShowMax': 0,
#         }

#         self.query_params = {}

#         if send_email:
#             self.form_data['sendConfirmationEmailCheckBox'] = 'on'

#         self.symbol = symbol
#         self.quantity = quantity
#         self.trade_type = trade_type
#         self.order_type = order_type
#         self.duration = duration
#         self._form_token = None
#         self.validated = False

#     def execute(self):
#         if not self.validated:
#             self.validate()
#             return self.execute()

#     @property
#     def symbol(self):
#         return self._symbol

#     @symbol.setter
#     def symbol(self, symbol):
#         if self.security_type == 'stock':
#             self.form_data['symbolTextbox'] = symbol
#         elif self.security_type == 'option':
#             self.query_params['m'] = symbol
#         self._symbol = symbol

#     @property
#     def quantity(self):
#         return self._quantity

#     @quantity.setter
#     def quantity(self, q):
#         if self.security_type == 'stock':
#             self.form_data['quantityTextbox'] = q
#         elif self.security_type == 'option':
#             self.form_data['txtNumContracts'] = q
#             self.query_params.update({'nc': q})
#         self._quantity = q

#     @property
#     def trade_type(self):
#         return str(self._trade_type)

#     @trade_type.setter
#     def trade_type(self, trade_type):
#         if type(trade_type) == str:
#             trade_type = TradeType(trade_type)

#         self.form_data.update(trade_type.form_data)
#         self._trade_type = trade_type

#     @property
#     def duration(self):
#         return str(self._duration)

#     @duration.setter
#     def duration(self, duration):
#         if type(duration) == str:
#             duration = Duration(duration)

#         self.form_data.update(duration.form_data)
#         self._duration = duration

#     @property
#     def order_type(self):
#         return str(self._order_type)

#     @order_type.setter
#     def order_type(self, order_type):
#         if type(order_type) == str:
#             order_type = OrderType.fromstring(order_type)

#         self.form_data.update(order_type.form_data)
#         self._order_type = order_type

#     @property
#     def form_token(self):
#         return self._form_token

#     @form_token.setter
#     def form_token(self, token):
#         if token is None:
#             self.form_data.pop('formToken', None)
#             self._form_token = None
#         else:
#             self.form_data.update({'formToken': token})
#             self._form_token = token

#     def _get_trade_info(self, tree):
#         trade_info_tables = tree.xpath(
#             '//div[@class="box-table"]/table[contains(@class,"table1")]')
#         tt1 = trade_info_tables[0]
#         tt2 = trade_info_tables[1]

#         trade_info = {
#             'Description': tt1.xpath('tbody/tr[2]/td[1]/text()')[0],
#             'Transaction': tt1.xpath('tbody/tr[2]/td[2]/text()')[0],
#             'StopLimit': tt1.xpath('tbody/tr[2]/td[3]/text()')[0],
#             'Duration': tt1.xpath('tbody/tr[2]/td[4]/text()')[0],
#             'Price': tt2.xpath('tbody/tr[1]/td[3]/text()')[0],
#             'Quantity': tt2.xpath('tbody/tr[2]/td[2]/text()')[0],
#             'Commision': tt2.xpath('tbody/tr[3]/td[2]/text()')[0],
#             'Est_Total': tt2.xpath('tbody/tr[4]/td[2]/text()')[0],
#         }

#         return trade_info

#     @sleep_and_retry
#     @limits(calls=6, period=20)
#     def validate(self):
#         if self.form_token is None:
#             print("refreshing form token")
#             self.refresh_form_token()

#         if self.validated:
#             warnings.warn("Warning: trade has already been validated.  Revalidating...")
#             self.form_data.pop('btnReview',None)
#             self.refresh_form_token()
#             self.validated = False
#         assert type(self._trade_type).__name__ == 'TradeType'
#         assert type(self._order_type).__name__ == 'OrderType'
#         assert type(self._duration).__name__ == 'Duration'
#         assert type(self.quantity) == int
#         try:
#             assert self.security_type == 'stock' or self.security_type == 'option'
#         except AssertionError:
#             raise InvalidTradeException(
#                 "security type is not specified.  Must be either 'stock' or 'option'")

#         if self.security_type == 'stock':
#             try:
#                 assert self.trade_type in (
#                     'BUY', 'SELL', 'SELL_SHORT', 'BUY_TO_COVER')
#             except AssertionError:
#                 raise InvalidTradeException(
#                     "A stock's trade type must be one of the following: BUY,SELL,SELL_SHORT,BUY_TO_COVER.  Got %s " % self.trade_type)
#         if self.security_type == 'option':
#             try:
#                 assert self.trade_type in ('BUY_TO_OPEN', 'SELL_TO_CLOSE')
#             except AssertionError:
#                 raise InvalidTradeException(
#                     "An option's trade type must be one of the following: BUY_TO_OPEN,SELL_TO_CLOSE")
#         try:
#             max_shares = self._get_max_shares()
#             assert self.quantity <= max_shares
#         except AssertionError:
#             raise TradeExceedsMaxSharesException(
#                 "Quantity %s exceeds max of %s" % (self.quantity, max_shares), max_shares)
#         try:
#             resp = self.go_to_preview()
#             redirect_url = resp.history[0].headers['Location']
#             redirect_qp = UrlHelper.get_query_params(redirect_url)

#             tree = html.fromstring(resp.text)
#             self.refresh_form_token(tree)
#             trade_info = self._get_trade_info(tree)

#             submit_query_params = redirect_qp

#             submit_form_data = {
#                 'submitOrder': tree.xpath('//input[@name="submitOrder"]/@value')[0],
#                 'formToken': self.form_token
#             }

#             submit_url = UrlHelper.set_query(
#                 self.submit_url, submit_query_params)
#             prepared_trade = PreparedTrade(
#                 submit_url, submit_form_data, **trade_info)
#             self.execute = prepared_trade.execute
#             self.validated = True
#             return prepared_trade
#         except Exception as e:
#             print("trade failed for %s %s %s" % (self.symbol, self.quantity, self.trade_type))
#             print(e)
#             raise e
#             return False

#     def refresh_form_token(self, tree=None):
#         self.form_token = None

#         if tree is None:
#             self.form_token = None
#             uri = UrlHelper.set_query(self.base_url, self.query_params)
#             resp = Session().get(uri, data=self.form_data)
#             tree = html.fromstring(resp.text)
#         fon = lambda x: x[0] if len(x)>0 else None
#         token = fon(tree.xpath('//input[@name="formToken"]/@value'))
#         self.form_token = token
#         print("form token: %s" % self.form_token)
#         print("form data: %s" % self.form_data)


class PreparedTrade(dict):
    def __init__(self, url, form_data, **kwargs):
        self.url = url
        self.submit_form_data = form_data
        self.update(kwargs)

    @sleep_and_retry
    @limits(calls=6, period=20)
    def execute(self):
        session = Session()
        resp = session.post(self.url, data=self.submit_form_data)
        return resp
