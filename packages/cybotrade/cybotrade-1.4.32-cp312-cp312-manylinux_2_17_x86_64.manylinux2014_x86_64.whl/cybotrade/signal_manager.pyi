import logging
from typing import List
from cybotrade.models import ActiveOrder, OrderUpdate
from cybotrade.runtime import StrategyTrader
from cybotrade.manager_server import ManagerServer

class SignalManager:
    server: ManagerServer | None = None
    LOG_FORMAT = (
        "%(levelname)s %(name)s %(asctime)-15s %(filename)s:%(lineno)d %(message)s"
    )
    handlers: List[logging.Handler] = []
    strategy: StrategyTrader
    logger = logging
    LOG_FORMAT: str

    def __init__(
            self,
            log_level: int = logging.INFO,
            handlers: List[logging.Handler] = [],
    ):
        """
        Set up the logger
        """

    def on_init(
            self,
    ):
        """
        This method is called when the strategy is started successfully.
        """

    def assign_strategy_trader(self, strategy: StrategyTrader):
        """
        do sumn
        """
    
    async def on_order_update(
            self,
            update: OrderUpdate,
    ):
        """
        This method is called when receiving an order update from the exchange.
        """

    async def on_active_order_interval(
            self, active_orders: List[ActiveOrder]
    ):
        """
        This method is called when the passed in `active_order_interval` time has elapsed. This will return a list of client_order_ids of all active orders.
        """

    def on_shutdown(self):
        """
        ***This method is invoked when the Strategy is being shutdown.*** 
        """

async def start_manager(manager, config):
    """
    start sumn
    """
