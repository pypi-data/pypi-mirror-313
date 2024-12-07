import datetime as dt
from enum import Enum
from typing import List, Tuple, Union

import pandas as pd
from pydantic import BaseModel


class Lookback(Enum):
    ONE_HOUR = "1H"
    SIX_HOURS = "6H"
    TWELVE_HOURS = "12H"
    ONE_DAY = "1D"
    ONE_WEEK = "7D"
    ONE_MONTH = "30D"
    THREE_MONTHS = "90D"
    ONE_YEAR = "365D"


class EntityType(Enum):
    FINANCIAL_ASSET = "financial_asset"
    COMPANY = "company"
    ORGANIZATION = "organization"
    PERSON = "person"
    PLACE = "place"


class AssetClass(Enum):
    CRYPTO = "crypto"
    COMMODITIES = "commodities"


class EntityMetricTransform(Enum):
    LAST = 'last'
    AVERAGE = 'average'
    TICKS = 'ticks'
    PRICE_SUMMARY = 'price_summary'


class EntityMetrics(Enum):
    MENTIONS = 'mentions'
    SENTIMENT = 'sentiment'
    EXCITEMENT = 'excitement'
    OPTIMISM = 'optimism'
    PESSIMISM = 'pessimism'
    FEAR = 'fear'
    UNCERTAINTY = 'uncertainty'
    SURPRISE = 'surprise'

class FinancialAssetMetrics(Enum):
    PRICE = 'price'

class SingleMetricTimeSeries(BaseModel):
    metric: Union[EntityMetrics, FinancialAssetMetrics, str]
    values: List[Tuple[Union[str,dt.datetime], float]]

    @property
    def df(self):
        df = pd.DataFrame(self.values, columns=['timestamp', getattr(self.metric, 'value', self.metric)])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df


class TimeSeriesResponse(BaseModel):
    entity_id: str
    time_series: List[SingleMetricTimeSeries]

class TimeSeriesResample(Enum):
    ONE_MINUTE = '1T'
    FIVE_MINUTES = '5T'
    FIFTEEN_MINUTES = '15T'
    THIRTY_MINUTES = '30T'
    ONE_HOUR = '1H'
    ONE_DAY = '1D'

class TimeHorizon(Enum):
    SHORT = 'short'
    LONG = 'long'
