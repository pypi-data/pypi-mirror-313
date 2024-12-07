from cybotrade.models import ManagerRuntimeConfig
from cybotrade.runtime import StrategyTrader
from cybotrade.signal_manager import SignalManager 


class ManagerRuntime:
    """
    A class representation of the underlying strategy runtime which handle backtest,
    paper trade, live trade.
    """
    async def connect(self, config: ManagerRuntimeConfig, strategy: SignalManager):
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
    async def start(self):
        """
        Start the runtime and this method ideally will never return under live trade /
        paper trade unless interrupted, however this function will return when the backtest
        finishes.

        Raises
        ------
        Exception
            If there is an error during the runtime.
        """
    def retrieve_strategy_trader(self) -> StrategyTrader:
        """
        get strategy-trader
        """
