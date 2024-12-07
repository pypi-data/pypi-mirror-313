import json

from .models import *


class JSONEncoder(json.JSONEncoder):
    RECOGNIZED_TYPES = (
        Exchange,
        Environment,
        OrderSide,
        OrderType,
        OrderStatus,
        TimeInForce,
        PositionSide,
        PositionMargin,
        Interval,
        Direction,
        RuntimeMode,
        Performance,
        OrderSizeUnit,
        ExchangeConfig,
        OrderBookSubscriptionParams,
        Symbol,
        Candle,
        OrderResponse,
        OrderUpdate,
        Position,
        Balance,
        Order,
        Level,
        LocalOrderBookUpdate,
        OrderSize,
        RuntimeConfig,
        StopParams,
        OrderParams,
        OpenedTrade,
        FloatWithTime,
    )

    # If the object is a recognized type, we can serialize it.
    # Otherwise, we just use the default encoder.
    def default(self, o):
        for t in self.RECOGNIZED_TYPES:
            if isinstance(o, t):
                # `__repr__` is overrided in Rust to serialize the object as a JSON string.
                return json.loads(o.__repr__())

        return json.JSONEncoder.default(self, o)
