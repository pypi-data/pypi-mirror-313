import pandas as pd
import numpy as np
from typing import Union, Optional
from abc import ABC, abstractmethod


class Factor(ABC):
    """
    Abstract base class for factors.
    """
    def __init__(self,
                 prices: pd.DataFrame,
                 vwap: bool = True,
                 log: bool = True,
                 sign_flip: bool = True,
                 normalize: bool = True,
                 central_tendency: str = 'mean',
                 norm_method: str = 'std',
                 smoothing: bool = False,
                 smoothing_method: str = 'rolling',
                 window_size: int = 30,
                 short_window_size: int = None,
                 long_window_size: int = None,
                 window_type: str = 'rolling',
                 window_fcn: Optional[str] = None,
                 lags: int = 0,
                 ):
        """
        Constructor

        Parameters
        ----------
        prices: pd.DataFrame - MultiIndex
            DataFrame MultiIndex with DatetimeIndex (level 0), ticker (level 1) and prices (cols).
        vwap: bool, default True
            Use volume-weighted average price.
        log: bool, default True
            Logarithm transformation.
        sign_flip: bool, default True
            Flips sign of factor if true.
        normalize: bool, default True
            Normalizes factor values.
        central_tendency: str, {'mean', 'median'}, default 'mean'
            Measure of central tendency used for the rolling window.
        norm_method: str, {'std', 'mad'}, default 'std'
            Method for normalizing factor values.
        smoothing: bool, default False
            If True, factor series is smoothed.
        smoothing_method: str, {'rolling', 'expanding', 'ewm'}, default 'rolling'
            Type of window for smoothing.
        window_size: int, default 30
            Number of observations in moving window for smoothing.
        short_window_size: int, default None
            Short window size for computing dispersion.
        long_window_size: int, default None
            Long window size for computing dispersion.
        window_type: str, {'rolling', 'expanding', 'ewm'}, default 'rolling'
            Type of window.
        window_fcn: str, default None
            Provide a window function. If None, observations are equally-weighted in the rolling computation.
            See scipy.signal.windows for more information.
        lags: int, default 0
            Number of lags to include in the factor.
        """
        self.prices = prices
        self.vwap = vwap
        self.log = log
        self.sign_flip = sign_flip
        self.normalize = normalize
        self.central_tendency = central_tendency
        self.norm_method = norm_method
        self.smoothing = smoothing
        self.smoothing_method = smoothing_method
        self.window_size = window_size
        self.short_window_size = short_window_size
        self.long_window_size = long_window_size
        self.window_type = window_type
        self.window_fcn = window_fcn
        self.lags = lags
        self.factor = None
        self.convert_to_multiindex()

    @abstractmethod
    def convert_to_multiindex(self) -> pd.DataFrame:
        """
        Converts DataFrame to MultiIndex.

        Returns
        -------
        df: pd.DataFrame
            DataFrame with MultiIndex.
        """
        if not isinstance(self.prices.index, pd.MultiIndex):
            self.prices = self.prices.stack()
            self.prices.columns = ['price']

        return self.prices

    @abstractmethod
    def compute_factor(self) -> pd.DataFrame:
        """
        Computes factor.

        Returns
        -------
        factor: pd.DataFrame
            Factor.
        """
        pass

    @abstractmethod
    def compute_returns(self) -> pd.DataFrame:
        """
        Computes returns.

        Returns
        -------
        returns: pd.DataFrame
            Returns.
        """
        pass

    @abstractmethod
    def compute_vol(self) -> pd.DataFrame:
        """
        Computes volatility.

        Returns
        -------
        vol: pd.DataFrame
            Volatility.
        """
        pass

    @abstractmethod
    def compute_carry(self) -> pd.DataFrame:
        """
        Computes carry.

        Returns
        -------
        carry: pd.DataFrame
            Carry.
        """
        pass

    @abstractmethod
    def compute_size_factor(self) -> pd.DataFrame:
        """
        Computes size factor.

        Returns
        -------
        size: pd.DataFrame
            Size factor.
        """
        pass

    @abstractmethod
    def network_size(self) -> pd.DataFrame:
        """
        Computes the cross-sectional rank of network size values.

        Returns
        -------
        df: pd.DataFrame
            DataFrame with DatetimeIndex (level 0), tickers (level 1) and network size rank (cols).
        """
        pass

    @abstractmethod
    def network_growth(self) -> pd.DataFrame:
        """
        Computes the network growth over an n-period lookback window.

        Returns
        -------
        df: pd.DataFrame
            DataFrame with DatetimeIndex (level 0), tickers (level 1) and network size rank (cols).
        """
        pass

