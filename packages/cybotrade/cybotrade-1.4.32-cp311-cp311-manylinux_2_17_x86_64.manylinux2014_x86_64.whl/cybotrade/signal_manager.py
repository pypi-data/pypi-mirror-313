import asyncio
import logging
from typing import Any, List
import signal
from cybotrade.manager_runtime import ManagerRuntime
from cybotrade.manager_server import ManagerServer
from cybotrade.runtime import StrategyTrader
from cybotrade.models import ActiveOrder, OrderSide, OrderUpdate

class SignalManager:
    LOG_FORMAT = (
        "%(levelname)s %(name)s %(asctime)-15s %(filename)s:%(lineno)d %(message)s"
    )
    handlers: List[logging.Handler] = []
    strategy: StrategyTrader
    port: int = 8001

    def __init__(
        self,
        log_level: int = logging.INFO,
        handlers: List[logging.Handler] = [],
    ):
        if len(self.handlers) == 0:
            default_handler = logging.StreamHandler()
            default_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
            self.handlers.append(default_handler)

        logging.root.setLevel(log_level)
        if not logging.root.hasHandlers():
            for handler in handlers:
                logging.root.addHandler(handler)

    def assign_strategy_trader(self, strategy: StrategyTrader):
        self.strategy = strategy

    async def on_init(self):
        self.server = ManagerServer(self, logger=logging.Logger(name="Manager Server"), strategy_trader=self.strategy)
        asyncio.create_task(self.server.start(self.port), name="Manager Signal Server")

    async def on_signal(self, id: str, side: OrderSide, signal_params: Any):
        """
        Do sumt
        """

    async def on_order_update(self, update: OrderUpdate):
        """
        on order_update 
        """

    async def on_active_order_interval(self, active_orders: List[ActiveOrder]):
        """
        on_active_order_interval
        """

    def on_shutdown(self):
        return 


async def start_manager(manager, config):
    manager = manager()
    rt = ManagerRuntime() 
    await rt.connect(config, manager)
    trader = rt.retrieve_strategy_trader()
    manager.assign_strategy_trader(trader)

    def signal_handler(signum, frame):
        manager.on_shutdown()
        exit()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    await rt.start()

