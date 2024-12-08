import pandas as pd
import numpy as np
from typing import Union, Optional

from factorlab.feature_engineering.transformations import Transform


class Vol:
    """
    Vol factor, aka Low Vol, Beta or Betting against Beta.
    """
    def __init__(self,
                 df: pd.DataFrame,
                 method: str = 'vol',
                 price: str = 'close',
                 ret_method: str = 'log',
                 sign_flip: bool = True,
                 window_size: int = 30
                 ):
        """
        Constructor

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame with DatetimeIndex (level 0), ticker (level 1) and size metrics (col).
        method: str, {'vol', 'beta', 'iqr', 'atr', 'range', 'mad'}, default 'vol'
            Method for computing dispersion. Options are 'vol' or 'beta'.
        price: str, {'close', 'vwap'}, default 'close'
            Price series to use for computing returns.
        ret_method: str, default 'log'
            Method for computing returns. Options are 'log' or 'simple'.
        sign_flip: bool, default False
            Flips sign of factor if true.
        window_size: int, default 30
            Window size for computing volatility or beta.
        """
        self.df = df.to_frame() if isinstance(df, pd.Series) else df


        # check fields
        if price not in df.columns:
            raise ValueError("Price series must be provided for dataframe in order to compute returns.")

        self.df = df if isinstance(df, pd.DataFrame) else df.to_frame() if isinstance(df, pd.Series) else None
        self.price = self.df.loc[:, price] if price is not 'vwap' else Transform(df).vwap()
        self.ret_method = ret_method
        self.sign_flip = sign_flip
        self.window_size = window_size
        self.returns = self.compute_returns()
        self.dispersion = self.compute_vol()

    def convert_to_multiindex(self) -> pd.DataFrame:
        """
        Converts DataFrame to MultiIndex.

        Returns
        -------
        df: pd.DataFrame
            DataFrame with MultiIndex.
        """
        if not isinstance(self.df.index, pd.MultiIndex):
            self.df = self.df.stack()

        return self.df


    def compute_returns(self):
        """
        Computes returns from price series.

        Parameters
        ----------
        method: str, default 'log'
            Method for computing returns. Options are 'log' or 'simple'.

        Returns
        -------
        returns: pd.Series or pd.DataFrame
            Series or DataFrame with DatetimeIndex (level 0), ticker (level 1) and returns values (cols).
        """
        # compute returns
        self.returns = Transform(self.price).returns(method=self.ret_method)

        return self.returns

    def compute_vol(self):
        """
        Computes volatility from returns series.

        Returns
        -------
        vol: pd.Series or pd.DataFrame
            Series or DataFrame with DatetimeIndex (level 0), ticker (level 1) and vol values (cols).
        """
        # compute vol
        self.vol = Transform(self.price).dispersion(self.method)

        return self.vol


