# from typing import List, Optional
# from .models import (
#     Order,
#     OrderResponse,
#     OrderSide,
#     OrderType,
#     OrderUpdate,
#     Environment,
#     Exchange,
#     Position,
#     Symbol,
#     TimeInForce,
# )
#
# class Trader:
#     """
#     A class for making trade and tracking updates of placed trades on exchanges.
#     """
#
#     @staticmethod
#     async def connect(
#         secret_id: str,
#         access_token: str,
#         exchange: Exchange,
#         environment: Environment,
#         api_url: Optional[str],
#     ) -> Trader:
#         """
#         Instantiate the `Trader` class by connecting to the specified exchange.
#
#         Parameters
#         ----------
#         exchanges : List[ExchangeConfig]
#             the list of exchanges to connect to.
#
#         Returns
#         -------
#         Trader
#             a Trader instance
#
#         Raises
#         ------
#         Exception
#             If there is an error connecting to the exchange.
#         """
#     async def place_order(
#         self,
#         symbol: Symbol,
#         side: OrderSide,
#         order_type: OrderType,
#         time_in_force: TimeInForce,
#         quantity: float,
#         price: float,
#         reduce_only: bool,
#         post_only: bool,
#         hedge_mode: bool,
#         client_order_id: Optional[str],
#         extra_params: Optional[dict[str, str]],
#     ) -> OrderResponse:
#         """
#         Place an order on the specified exchange.
#
#         Parameters
#         ----------
#         request : OrderRequest
#             the request parameters for the order.
#
#         Returns
#         -------
#         OrderResponse
#             the order response returned from the exchange.
#
#         Raises
#         ------
#         Exception
#             If there is an error placing order on the exchange.
#         """
#     async def cancel_order(
#         self,
#         symbol: Optional[Symbol],
#         exchange_order_id: Optional[str],
#         client_order_id: Optional[str],
#         extra_params: Optional[dict[str, str]],
#     ) -> OrderResponse:
#         """
#         Place an order on the specified exchange.
#         NOTE: Either `exchange_order_id` or `client_order_id` must be specified.
#
#         Parameters
#         ----------
#         symbol : Optional[Symbol]
#             the trading pair to cancel orders on eg. BTC/USDT.
#         exchange_order_id : Optional[str]
#             the order id from exchange.
#         client_order_id : Optional[str]
#             the order id that was specified when placing order.
#         extra_params : Optional[dict[str, str]]
#             extra parameters for the request.
#
#         Returns
#         -------
#         OrderResponse
#             the order response returned from the exchange.
#
#         Raises
#         ------
#         Exception
#             If there is an error cancelling order on the exchange.
#         """
#     async def cancel_all_order(
#         self,
#         symbol: Symbol,
#         extra_params: Optional[dict[str, str]],
#     ):
#         """
#         Place an order on the specified exchange.
#
#         Parameters
#         ----------
#         symbol : Symbol
#             the trading pair to cancel orders on eg. BTC/USDT.
#         extra_params : Optional[dict[str, str]]
#             extra parameters for the request.
#
#         Raises
#         ------
#         Exception
#             If there is an error placing order on the exchange.
#         """
#     async def get_open_orders(
#         self,
#         symbol: Optional[Symbol],
#         extra_params: Optional[dict[str, str]],
#     ) -> List[Order]:
#         """
#         Get current open orders from exchange.
#
#         Parameters
#         ----------
#         symbol : Optional[Symbol]
#             the trading pair to get open orders on eg. BTC/USDT.
#         extra_params : Optional[dict[str, str]]
#             extra parameters for the request.
#
#         Raises
#         ------
#         Exception
#             If there is an error getting open orders from the exchange.
#         """
#     async def get_open_positions(
#         self,
#         symbol: Optional[Symbol],
#         extra_params: Optional[dict[str, str]],
#     ) -> List[Position]:
#         """
#         Get current open positions from exchange.
#
#         Parameters
#         ----------
#         symbol : Optional[Symbol]
#             the trading pair to get positions on eg. BTC/USDT.
#         extra_params : Optional[dict[str, str]]
#             extra parameters for the request.
#
#         Raises
#         ------
#         Exception
#             If there is an error getting positions from the exchange.
#         """
#     async def get_wallet_balance(
#         self,
#         coins: Optional[List[str]],
#         extra_params: Optional[dict[str, str]],
#     ) -> List[Position]:
#         """
#         Get current wallet balance from exchange.
#
#         Parameters
#         ----------
#         coins : Optional[List[str]]
#             the list of coins for getting wallet balances eg. BTC
#         extra_params : Optional[dict[str, str]]
#             extra parameters for the request.
#
#         Raises
#         ------
#         Exception
#             If there is an error getting wallet balances from the exchange.
#         """
#     async def subscribe_order_update(self):
#         """
#         Subscribe the private order update from exchange.
#
#         Raises
#         ------
#         Exception
#             If there is an error subscribing to the private order update stream from the exchange.
#         """
#     async def subscribe_position_update(self):
#         """
#         Subscribe the private position update from exchange.
#
#         Raises
#         ------
#         Exception
#             If there is an error subscribing to the private position update stream from the exchange.
#         """
#     async def subscribe_wallet_update(self):
#         """
#         Subscribe the private wallet update from exchange.
#
#         Raises
#         ------
#         Exception
#             If there is an error subscribing to the private wallet update stream from the exchange.
#         """
#     async def listen_execution_update(self) -> OrderUpdate:
#         """
#         Listen for the latest order update.
#
#         Returns
#         -------
#         OrderUpdate
#             the latest order update from the exchange.
#
#         Raises
#         ------
#         Exception
#             If there is an error retrieving the latest order update from the exchange.
#         """
#     async def listen_position_update(self) -> List[Position]:
#         """
#         Listen for the latest position update.
#
#         Returns
#         -------
#         List[Position]
#             the latest position update from the exchange.
#
#         Raises
#         ------
#         Exception
#             If there is an error retrieving the latest position update from the exchange.
#         """  # noqa: E501
#     async def listen_wallet_update(self) -> List[Position]:
#         """
#         Listen for the latest wallet update.
#
#         Returns
#         -------
#         List[Balance]
#             the latest wallet balance update from the exchange.
#
#         Raises
#         ------
#         Exception
#             If there is an error retrieving the latest wallet update from the exchange.
#         """
