from __future__ import annotations
import pandas as pd
import numpy as np
from typing import Union


from factorlab.transform import Transform


class Liquidity:
    """
    Liquidity factor.
    """
    def __init__(self,
                 df: pd.DataFrame,
                 vwap: bool = True,
                 log: bool = True,
                 st_lookback: int = None,
                 lookback: int = 20,
                 lt_lookback: int = None,
                 smoothing: str = None,
                 lags: int = 0,
                 ):
        """
        Constructor

        Parameters
        ----------
        df: pd.DataFrame - MultiIndex
            DataFrame MultiIndex with DatetimeIndex (level 0), ticker (level 1) and prices (cols).
         vwap: bool, default False
            Compute signal on vwap price.
        log: bool, default False
            Converts to log price.
        st_lookback: int
            Number of observations in short-term moving window.
        lookback: int
            Number of observations in moving window.
        lt_lookback: int
            Number of observations in long-term moving window.
        smoothing: str, {'median', 'smw', 'ewm'}, default None
            Smoothing method to use.
        lags: int, default 0
            Number of periods to lag values by.
        """
        self.df = df.astype(float)
        self.vwap = vwap
        self.log = log
        self.st_lookback = st_lookback
        self.lookback = lookback
        self.lt_lookback = lt_lookback
        self.smoothing = smoothing
        self.lags = lags


