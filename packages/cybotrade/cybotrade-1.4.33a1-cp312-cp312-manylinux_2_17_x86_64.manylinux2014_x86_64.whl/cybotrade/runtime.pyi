from typing import List
from .models import (
    SymbolInfo,
    ActiveOrder,
    Balance,
    Exchange,
    OrderBookSnapshot,
    OrderSide,
    OrderUpdate,
    Performance,
    Position,
    RuntimeConfig,
    OrderParams,
    OrderResponse,
    Symbol,
    TimeInForce,
)
from .strategy import Strategy

class StrategyTrader:
    config: RuntimeConfig
    async def open(
        self,
        exchange: Exchange,
        symbol: Symbol,
        side: OrderSide,
        quantity: float,
        client_order_id: str | None,
        limit: float | None,
        take_profit: float | None,
        stop_loss: float | None,
        time_in_force: TimeInForce | None,
        is_hedge_mode: bool | None,
        is_post_only: bool | None) -> OrderResponse:
        """
        Places an open order. This method guarantees that take_profit/stop_loss will be handled for the User.
        """
    async def get_user_config(self): 
        """
        Retrieve user config.
        """
    async def order(self, params: OrderParams) -> OrderResponse:
        """
        Places an order, do note that this function does not take into account current position,
        it merely executes whatever parameters was given.
        """
    async def cancel(self, exchange: Exchange, symbol: Symbol, id: str) -> OrderResponse:
        """
        Cancels a specific order by its id.
        """
    async def close(
            self,
            exchange: Exchange,
            symbol: Symbol,
            side: OrderSide,
            quantity: float,
            time_in_force: TimeInForce | None,
            is_hedge_mode: bool | None
        ):
        """
        Closes position with the same given side and given quantity. This function closes the trade with market
        order.
        """
    async def get_current_available_balance(self, exchange: Exchange, symbol: Symbol) -> float:
        """
        Get the current available balance of the running strategy.
        """
    async def get_balance_data(self, exchange: Exchange, symbol: Symbol) -> Balance:
        """
        Get the balance data of the running strategy.
        """
    async def get_open_orders(self, exchange: Exchange, symbol: Symbol) -> List[ActiveOrder]:
        """
        Get the current open orders on the account of the corresponding exchange.
        """
    async def get_order_book(self, exchange: Exchange, symbol: Symbol) -> OrderBookSnapshot:
        """
        Get the current open orders on the account of the corresponding exchange.
        """
    async def get_current_price(self, exchange: Exchange, symbol: Symbol) -> float:
        """
        Get the current price of the symbol requested.
        """
    async def position(self, exchange: Exchange, symbol: Symbol) -> Position:
        """
        Get the current position of the strategy.
        """
    async def all_position(self, exchange: Exchange) -> List[Position]:
        """
        Get all current holding position on the exchange.
        """
    async def get_order_details(self, exchange: Exchange, symbol: Symbol, client_order_id: str) -> OrderUpdate:
        """
        Get the order status (if it exists).
        """
    async def get_symbol_info(self, exchange: Exchange, symbol: Symbol) -> SymbolInfo:
        """
        symbol info
        """

class Runtime:
    """
    A class representation of the underlying strategy runtime which handle backtest,
    paper trade, live trade.
    """
    async def connect(self, config: RuntimeConfig, strategy: Strategy):
        """
        Instantiate the `Runtime` class by providing the configurations and a `Strategy`
        class which acts as the event handler.

        Parameters
        ----------
        config : RuntimeConfig
            the configuration for the runtime.
        strategy : Strategy
            the strategy to run within the runtime.

        Returns
        -------
        Runtime
            a Runtime instance

        Raises
        ------
        Exception
            If there is an error creating the runtime.
        """
    async def setup_backtest(self) -> bool:
        """
        Setup backtest data. This should never be called.
        """
    async def start(self) -> Performance:
        """
        Start the runtime and this method ideally will never return under live trade /
        paper trade unless interrupted, however this function will return when the backtest
        finishes.

        Raises
        ------
        Exception
            If there is an error during the runtime.
        """
    async def set_param(self, identifier: str, value: str):
        """
        Set parameters of the permutation
        """
