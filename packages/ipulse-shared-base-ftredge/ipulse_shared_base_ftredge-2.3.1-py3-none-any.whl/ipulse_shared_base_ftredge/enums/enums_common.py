
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long

from enum import Enum



class ProgressStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    RESTARTED = "restarted"
    SUCCESS_COMPLETED = "success_completed"
    PARTIALLY_COMPLETED = "partially_completed"
    FAILED_GRACEFULLY_COMPLETED = "failed_gracefully_completed"
    FAILED_EXITED = "failed_exited"
    DELAYED = "delayed"
    PENDING = "pending"
    PAUSED = "paused"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"
    EXCEPTION = "exception"
    ERROR = "error"
    ERRORS = "errors"
    WARNING = "warning"
    WARNINGS = "warnings"


class Status(Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    ESCALATED = "escalated"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    RESOLVED = "resolved"
    IGNORED = "ignored"
    CANCELLED = "cancelled"
    CLOSED = "closed"

    def __str__(self):
        return self.value

### Exception during full exection, partially saved
# Exception during ensemble pipeline; modifications collected in local object , nothing persisted
# Exception during ensemble pipeline; modifications persisted , metadata failed
# Exception during ensemble pipeline; modifications persisted , metadata persisted
# Exception during ensemble pipeline; modifications persisted , metadata persisted

class Unit(Enum):
    MIX="MIX"
    # Currency and Financial Values
    USD = "USD"  # United States Dollar
    EUR = "EUR"  # Euro
    JPY = "JPY"  # Japanese Yen
    GBP = "GBP"  # British Pound Sterling
    AUD = "AUD"  # Australian Dollar
    CAD = "CAD"  # Canadian Dollar
    CHF = "CHF"  # Swiss Franc
    CNY = "CNY"  # Chinese Yuan Renminbi
    SEK = "SEK"  # Swedish Krona
    NZD = "NZD"  # New Zealand Dollar
    MXN = "MXN"  # Mexican Peso
    SGD = "SGD"  # Singapore Dollar
    HKD = "HKD"  # Hong Kong Dollar
    NOK = "NOK"  # Norwegian Krone
    KRW = "KRW"  # South Korean Won
    RUB = "RUB"  # Russian Ruble
    INR = "INR"  # Indian Rupee
    BRL = "BRL"  # Brazilian Real
    ZAR = "ZAR"  # South African Rand
    CURRENCY = "currency"    # General currency, when specific currency is not needed

    # Stock Market and Investments
    SHARES = "shares"        # Number of shares
    PERCENT = "prcnt"      # Percentage, used for rates and ratios
    BPS = "bps"              # Basis points, often used for interest rates and financial ratios

    # Volume and Quantitative Measurements
    VOLUME = "volume"        # Trading volume in units
    MILLIONS = "mills"    # Millions, used for large quantities or sums
    BILLIONS = "bills"    # Billions, used for very large quantities or sums

    # Commodity Specific Units
    BARRELS = "barrels"      # Barrels, specifically for oil and similar liquids
    TONNES = "tonnes"        # Tonnes, for bulk materials like metals or grains
    TROY_OUNCES = "troy_oz" # Troy ounces, specifically for precious metals

    # Real Estate and Physical Properties
    SQUARE_FEET = "sq_ft"    # Square feet, for area measurement in real estate
    METER_SQUARE = "m2"      # Square meters, for area measurement in real estate
    ACRES = "acres"          # Acres, used for measuring large plots of land

    # Miscellaneous and Other Measures
    UNITS = "units"          # Generic units, applicable when other specific units are not suitable
    COUNT = "count"          # Count, used for tallying items or events
    INDEX_POINTS = "index_pnts"  # Index points, used in measuring indices like stock market indices
    RATIO = "ratio"          # Ratio, for various financial ratios

    def __str__(self):
        return self.value

class Frequency(Enum):
    ONE_MIN = "1min"
    FIVE_MIN="5min"
    FIFTEEN_MIN="15min"
    THIRTY_MIN = "30min"
    ONE_H = "1h"
    TWO_H = "2h"
    SIX_H = "6h"
    TWELVE_H = "12h"
    FOUR_H = "4h"
    EOD="eod"
    ONE_D = "1d"
    TWO_D = "2d"
    THREE_D = "3d"
    ONE_W = "1w"
    ONE_M = "1m"
    TWO_M="2m"
    THREE_M="3m"
    SIX_M="6m"
    ONE_Y="1y"
    THREE_Y="3y"

    def __str__(self):
        return self.value


class Days(Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
    MON_TO_FRI = "mon_to_fri"
    MON_TO_SAT = "mon_to_sat"
    SUN_TO_THU = "sun_to_thu"
    WEEKEND = "weekend"
    WEEKDAYS = "weekdays"
    ALL_DAYS = "all_days"

    def __str__(self):
        return self.value