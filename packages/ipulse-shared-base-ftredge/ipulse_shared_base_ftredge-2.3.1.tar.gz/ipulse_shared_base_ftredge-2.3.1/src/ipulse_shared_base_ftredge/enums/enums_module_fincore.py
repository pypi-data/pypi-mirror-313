# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
from enum import Enum

class FinCoreCategory(Enum):
    MARKET="market" # Market prices data
    CORPORATE="corp" # Corporate data such as financial statements and earnings, similar to fundamental data
    FUNDAMENTAL="fundam"
    ECONOMY="economy"
    NEWS="news"
    SENTIMENT="sntmnt"
    SOCIAL="social"
    POLITICS="poltcs"
    OTHER="other"

    def __str__(self):
        return self.value

class FincCoreSubCategory(Enum):
    STOCKS = "stock"
    BONDS = "bond"
    COMMODITIES = "commdt"
    CURRENCIES = "curncy"
    CRYPTOCURRENCIES = "crypto"
    REAL_ESTATE = "realest"
    EQUITY_INDICES = "eqindx"
    OPTIONS = "options"
    FUTURES = "futures"
    ETF = "etf"
    ECONOMIC_INDICATORS = "ecoind"
    FUNDAMENTALS = "fundam"
    OTHER = "other"

    def __str__(self):
        return self.value

class FinCoreRecordsCategory(Enum):
    PRICE="pric"
    SPOT= "spot"
    OHLCVA="ohlcva"
    OHLCV="ohlcv"
    OPEN="open"
    HIGH="high"
    LOW="low"
    CLOSE="close"
    VOLUME="volume"
    ADJC="adjc"
    FUNDAMENTAL="fundam" # treat this differently
    EARNINGS="earnings"
    CASH_FLOW="cashflw"
    BALANCE_SHEET="blnce_sht"
    INTERNAL_TRANSACTIONS="internaltrans"
    INDICATORS="indic"
    ARTICLE="article"
    INSTA_POST="isntapost"
    TWEET="tweet"
    OTHER="othr"

    def __str__(self):
        return self.value

class FinancialExchangeOrPublisher(Enum):
    CC="CC"
    US="US" # mix of all major US exchanges incl NASDAQ, NYSE, etc.
    NASDAQ="NASDAQ"
    NYSE="NYSE"
    SHG="SHG"
    LSE="LSE"
    

    def __str__(self):
        return self.value