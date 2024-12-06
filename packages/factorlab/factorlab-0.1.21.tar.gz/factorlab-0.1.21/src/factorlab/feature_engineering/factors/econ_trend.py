from __future__ import annotations
import pandas as pd
import numpy as np
from typing import Union, Optional

from factorlab.factors.trend import Trend
from factorlab.feature_analysis.time_series_analysis import linear_reg
from factorlab.feature_engineering.transform import Transform


class EconTrend(Trend):
    """
    Economic Trend factor.
    """


