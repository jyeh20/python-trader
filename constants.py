from enum import Enum

# Constants
API_RETRY_LIMIT = 3
MARKET_OPEN_HOUR = 7  # 9 AM
MARKET_CLOSE_HOUR = 14  # 4 PM

# File paths
TICKERS_JSON_PATH = 'tickers.json'
TICKER_ARRAY = "watchlist"

# Enums
class Trend(Enum):
    BULLISH = 'bullish'
    BEARISH = 'bearish'
    NONE = 'none'

class Frequency(Enum):
    MINUTE = 'minute'
    HOURLY = 'hourly'
    MONDAY_WEDNESDAY = 'monday_wednesday'
    MONTHLY = 'monthly'
