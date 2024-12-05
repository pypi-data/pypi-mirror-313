from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class ManagerRuntimeConfig:
    exchange_keys_path: str
    active_order_interval: int

@dataclass
class RuntimeConfig:
    mode: RuntimeMode
    candle_topics: List[str]
    datasource_topics: List[str]
    active_order_interval: int

    api_key: Optional[str]
    api_secret: Optional[str]

    exchange_keys: Optional[str]

    # initial_capital is required on on Backtest
    initial_capital: Optional[float]

    # start_time is required when `mode` is [`RuntimeMode.Backtest`]
    start_time: Optional[datetime]

    # end_time is required when `mode` is [`RuntimeMode.Backtest`]
    end_time: Optional[datetime]

    # candle_length is required when `mode` is [`RuntimeMode.Live`]
    data_count: Optional[int]

    # Experimental data caching for multiple backtest re-runs.
    cache_path: Optional[str]

    # Experimental periodic resync feature.
    # Only relevant in [`RuntimeMode.LiveTestnet`] and [`RuntimeMode.Live`]
    periodic_resync: Optional[bool]

@dataclass
class ExchangeConfig:
    exchange: Exchange
    environment: Environment

@dataclass
class Symbol:
    base: str
    quote: str

@dataclass 
class Performance:
    trades: Dict[str, List[OpenedTrade]]

@dataclass
class Candle:
    symbol: Symbol
    open: float
    high: float
    low: float
    close: float
    volume: float
    trade_count: Optional[float]
    is_closed: bool
    exchange: Exchange
    start_time: datetime
    end_time: datetime
    interval: Interval

@dataclass
class OrderBookSubscriptionParams:
    depth: int
    speed: Optional[int]
    extra_params: Optional[dict[str, str]]

@dataclass
class LevelAction(Enum):
    Add = 0
    Remove = 1
    Update = 2

@dataclass
class Level:
    price: float
    quantity: float
    price_action: LevelAction

@dataclass 
class OrderBookSnapshot:
    symbol: Symbol
    last_update_time: datetime
    last_update_id: int | None
    bids: List[Level]
    asks: List[Level]
    exchange: Exchange

@dataclass
class LocalOrderBookUpdate:
    best_bid: float
    bids: List[Level]
    best_ask: float
    asks: List[Level]
    spread: float
    depth: int
    exchange: Exchange

@dataclass
class OrderResponse:
    exchange: Exchange
    exchange_order_id: str
    client_order_id: str

@dataclass
class OrderUpdate:
    symbol: Symbol
    order_type: OrderType
    side: OrderSide
    time_in_force: TimeInForce
    exchange_order_id: str
    order_time: datetime
    updated_time: datetime
    size: float
    filled_size: float
    remain_size: float
    price: float
    client_order_id: str
    status: OrderStatus
    exchange: Exchange
    is_reduce_only: bool
    is_hedge_mode: bool

@dataclass
class PositionData:
    quantity: float
    avg_price: float

@dataclass
class Position:
    symbol: Symbol
    long: PositionData
    short: PositionData
    updated_time: int

@dataclass
class ExchangePosition:
    symbol: Symbol
    quantity: float
    value: float
    entry_price: float
    cumulative_realized_pnl: Optional[float]
    unrealized_pnl: float
    liquidation_price: float
    position_side: PositionSide
    margin: Optional[PositionMargin]
    initial_margin: float
    leverage: float
    exchange: Exchange

@dataclass
class Balance:
    exchange: Exchange
    coin: str
    wallet_balance: float
    available_balance: float
    initial_margin: Optional[float]
    margin_balance: Optional[float]
    maintenance_margin: Optional[float]

@dataclass
class Order:
    exchange_order_id: str
    client_order_id: str
    symbol: Optional[str]
    time_in_force: Optional[TimeInForce]
    side: Optional[OrderSide]
    order_type: Optional[OrderType]
    exchange: Exchange
    price: float
    quantity: float
    is_reduce_only: Optional[bool]

@dataclass
class OrderSize:
    unit: OrderSizeUnit
    value: float

@dataclass
class StopParams:
    trigger_direction: Direction
    trigger_price: float

@dataclass
class OrderParams:
    side: OrderSide
    quantity: float
    symbol: Symbol
    exchange: Exchange
    is_hedge_mode: bool
    client_order_id: Optional[str]
    limit: Optional[float]
    stop: Optional[StopParams]
    reduce: Optional[bool]
    client_order_id: Optional[str]
    market_price: Optional[float]
    is_post_only: Optional[bool]

@dataclass
class OpenedTrade:
    quantity: float
    side: OrderSide
    price: float
    time: datetime

@dataclass
class FloatWithTime:
    value: float
    timestamp: datetime

@dataclass 
class ActiveOrderParams:
    quantity: float
    take_profit: Optional[float]
    stop_loss: Optional[float]
    side: OrderSide

@dataclass
class ActiveOrder:
    params: ActiveOrderParams
    symbol: Symbol
    exchange: Exchange
    updated_time: int
    created_time: int
    exchange_order_id: str
    client_order_id: str

@dataclass 
class SymbolInfo:
    symbol: Symbol
    quantity_precision: int 
    price_precision: int 
    exchange: Exchange
    tick_size: float
    max_qty: float
    min_qty: float
    max_amount: float
    min_amount: float
    quanto_multiplier: float

class RuntimeMode(Enum):
    Backtest = 0
    Paper = 1
    Live = 2
    LiveTestnet = 3

class OrderSizeUnit(Enum):
    Base = 0
    Quote = 1
    Percentage = 2

class Exchange(Enum):
    BybitLinear = 0
    BinanceLinear = 1
    OkxLinear = 2
    BitgetLinear = 3
    ZoomexLinear = 4

class Environment(Enum):
    Testnet = 0
    Demo = 1
    Mainnet = 2

class OrderSide(Enum):
    Buy = 0
    Sell = 1

class OrderType(Enum):
    Market = 0
    Limit = 1

class OrderStatus(Enum):
    Created = 0
    PartiallyFilled = 1
    PartiallyFilledCancelled = 2
    Filled = 3
    Cancelled = 4
    Rejected = 5
    CancelRejected = 6
    Untriggered = 7
    Triggered = 8
    Deactivated = 9
    Active = 10
    Updated = 11
    ReplaceRejected = 12

class TimeInForce(Enum):
    GTC = 0
    IOC = 1
    FOK = 2
    PostOnly = 3

class PositionSide(Enum):
    Closed = 0
    OneWayLong = 1
    OneWayShort = 2
    HedgeLong = 3
    HedgeShort = 4

class PositionMargin(Enum):
    Cross = 0
    Isolated = 1

class Interval(Enum):
    OneMinute = 0
    ThreeMinute = 1
    FiveMinute = 2
    FifteenMinute = 3
    ThirtyMinute = 4
    OneHour = 5
    TwoHour = 6
    FourHour = 7
    SixHour = 8
    TwelveHour = 9
    OneDay = 10
    ThreeDay = 11
    OneWeek = 12
    OneMonth = 13

class Direction(Enum):
    Up = 0
    Down = 1

