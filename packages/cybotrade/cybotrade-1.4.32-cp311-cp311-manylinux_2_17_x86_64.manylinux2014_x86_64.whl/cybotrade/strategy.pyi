import collections
from typing import Any, List, Dict
from .models import (
    ActiveOrder,
    Exchange,
    OrderSide,
    OrderUpdate,
    Symbol
)
from .runtime import StrategyTrader

import logging

class Strategy:
    """
    This class is a handler that will be used by the Runtime to handle events such as
    `on_candle_closed`, `on_order_update`, etc. The is a base class and every new strategy
    should be inheriting this class and override the methods.
    """

    logger = logging
    LOG_FORMAT: str
    split_data_map: Dict[str, Dict[str, collections.deque]] = {}
    data_map: Dict[str, Dict[str,collections.deque]]
    manager_url: str

    def __init__(
            self,
            log_level: int = logging.INFO,
            handlers: List[logging.Handler] = [],
    ):
        """
        Set up the logger
        """

    def send_signal(self, id: str, side: OrderSide, signal_params: Any):
        """
        forward signal or sumn
        """

    def get_exchange(
        self,
        topic: str,
    ) -> Exchange:
        """
        This method is used to extract the exchange from candle topics
        """

    def on_init(
            self,
            strategy: StrategyTrader,
    ):
        """
        This method is called when the strategy is started successfully.
        """
    
    async def set_param(
            self,
            identifier: str,
            value: str 
    ):
        """
        Set up parameter for permutation
        """


    async def on_order_update(
            self,
            strategy: StrategyTrader,
            update: OrderUpdate,
    ):
        """
        This method is called when receiving an order update from the exchange.
        """

    async def on_backtest_complete(
            self, strategy: StrategyTrader
    ):
        """
        This method is called when backtest is completed.
        """

    async def on_datasource_interval(
            self, strategy: StrategyTrader, topic: str, data_list: List[Dict[str, str]]
    ):
        """
        This method is called when the requested Datasources' Interval has elapsed.
        E.g 'coinglass|4h|funding' -> this gets called every 4h
        """

    async def on_active_order_interval(
            self, strategy: StrategyTrader, active_orders: List[ActiveOrder]
    ):
        """
        This method is called when the passed in `active_order_interval` time has elapsed. This will return a list of client_order_ids of all active orders.
        """

    async def on_candle_closed(
            self, strategy: StrategyTrader, topic: str, symbol: Symbol,
    ):
        """
        This method is called when the requested candles have closed.
        """
    
    async def initialize_ringbuffer(
        self, topics: List[str], deque_length: int, data: Dict[str, List[Dict[str, str]]]
    ):
        """
        ***This method should never be overidden as it is used internally by the runtime.***
        """

    async def initialize_split_ringbuffer(
        self, topics: List[str], deque_length: int, data: Dict[str, List[Dict[str, str]]]
    ):
        """
        ***This method should never be overidden as it is used internally by the runtime to do splitting.***
        """

    async def update_ringbuffer(
            self, topic: str, data: Dict[str, str]
    ):
        """
        ***This method should never be overidden as it is used internally by the runtime.***
        """

    async def update_split_ringbuffer(
            self, topic: str, data: Dict[str, str]
    ):
        """
        ***This method should never be overidden as it is used internally by the runtime.***
        """

    def get_data_map(self):
        """
        ***This method is to get the data_map from python base strategy class***
        """

    def on_shutdown(self):
        """
        ***This method is invoked when the Strategy is being shutdown.*** 
        """

    async def on_periodic_resync(self, strategy):
        """
        Experimental periodic resync feature
        """
        # logging.debug(f"[on_active_order_interval] Received active orders: {active_orders.__repr__()}")
