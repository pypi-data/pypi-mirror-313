import asyncio
import logging
import signal
import shutil
import gc
from datetime import datetime
from itertools import product
from typing import Any, Dict, List, Type
import json
from .strategy import Strategy
from .models import Performance, RuntimeConfig, RuntimeMode 
from .runtime import Runtime

class BacktestPerformance:
    def __init__(self, config: RuntimeConfig):
        self.candle_topics = config.candle_topics

        if config.initial_capital == None:
            self.initial_capital = 10_000
        else:
            self.initial_capital = config.initial_capital 

        self.trades = {}

        if config.start_time != None:
            self.start_time = int(config.start_time.timestamp()) * 1000

        if config.end_time != None:
            self.end_time = int(config.end_time.timestamp()) * 1000

        self.version = "1.2.0"


    def set_trade_result(self, id: str, perf: Performance):
        self.trades[id] = perf

    def is_empty(self):
        for key in self.trades.keys():
            trade = self.trades[key].trades
            for trade_key in trade.keys():
                if len(trade[trade_key]) != 0:
                    return False

        return True

    def generate_json(self):
        perf_json = json.dumps(self.__dict__, default=str)
        date = datetime.now().date()
        date = ''.join(str(date).split('-'))
        time = datetime.now().time()
        time = ''.join(str(time).split('.')[0].replace(':', '-'))

        file = open(f"performance_{date}-{time}.json", "w")
        file.write(perf_json)

class Permutation:
    results = []
    fetched = False
    mutex = asyncio.Lock()
    checked = False

    def __init__(self, config: RuntimeConfig):
        self.config = config
    
    async def run(self, strategy_params: Dict[str, List[Any]], strategy):
        result = BacktestPerformance(self.config)
        
        keys = list(strategy_params.keys())
        permutations = list(product(*(strategy_params[key] for key in keys)))
        # coro_list = []

        if len(permutations) == 0:
            await self.process_permutations([], [], strategy)
        else:
            for perm in permutations:
                await self.process_permutations(keys, perm, strategy)
                # coro_list.append(self.process_permutations(keys, perm, strategy))

        for id, perf in self.results:
            result.set_trade_result(id, perf)
        
        if not result.is_empty():
            result.generate_json()
            
    async def process_permutations(self, keys: List[str], perm, strategy_class):
        strategy = strategy_class()
        runtime = Runtime()

        if not self.checked:
            def signal_handler(signum, frame):
                strategy.on_shutdown()
                exit()
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            self.checked = True

        await runtime.connect(self.config, strategy)
        
        if (self.config.mode == RuntimeMode.Backtest):
            free = shutil.disk_usage("/")
            if (free[2] / float(1<<30)) < 10.0:
                logging.warn(f"Available disk space on current partition is < 10.0 GiB! ({free[2] / float(1<<30)} GiB remaining)")
        
            await self.mutex.acquire()
            if (not self.fetched):
                result = await runtime.setup_backtest()
                if (not result):
                    raise Exception("Failed to retrieve data for backtest.")
                self.fetched = True
            self.mutex.release()

        permutation_key = []

        for i in range(len(keys)):
            await runtime.set_param(keys[i], str(perm[i]))
            permutation_key.append(f"{keys[i]}={perm[i]}")

        result = await runtime.start()
        self.results.append([",".join(permutation_key), result])
