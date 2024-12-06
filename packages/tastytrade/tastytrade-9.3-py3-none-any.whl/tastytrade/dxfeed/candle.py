from decimal import Decimal
from typing import Optional

from .event import Event


class Candle(Event):
    """
    A Candle event with open, high, low, close prices and other information
    for a specific period. Candles are build with a specified period using a
    specified price type with data taken from a specified exchange.
    """

    #: transactional event flags
    event_flags: int
    #: unique per-symbol index of this candle event
    index: int
    #: timestamp of the candle in milliseconds
    time: int
    #: sequence number of this event
    sequence: int
    #: total number of events in the candle
    count: int
    #: the first (open) price of the candle
    open: Decimal
    #: the maximal (high) price of the candle
    high: Decimal
    #: the minimal (low) price of the candle
    low: Decimal
    #: the last (close) price of the candle
    close: Decimal
    #: the total volume of the candle
    volume: Optional[Decimal] = None
    #: volume-weighted average price
    vwap: Optional[Decimal] = None
    #: bid volume in the candle
    bid_volume: Optional[Decimal] = None
    #: ask volume in the candle
    ask_volume: Optional[Decimal] = None
    #: implied volatility in the candle
    imp_volatility: Optional[Decimal] = None
    #: open interest in the candle
    open_interest: Optional[int] = None
