import pandas as pd
import numpy as np
from typing import Optional, Union, Any


class TCA:
    """
    Transaction cost analysis class.

    This class is used to analyze the transaction cost of a trading strategy.
    """
    def __init__(self,
                 signals: Union[pd.DataFrame, np.array],
                 ret: pd.Series,
                 strategy: str = 'ts_ls',
                 factor_bins: int = 5,
                 ret_bins: int = 3,
                 n_factors: int = 10,
                 disc_thresh: float = 0,
                 window_type: str = 'expanding',
                 window_size: int = 90,
                 ):
        """
        Constructor

        Parameters
        ----------
        signals
        ret
        strategy
        factor_bins
        ret_bins
        n_factors
        disc_thresh
        window_type
        window_size
        """
        self.signals = signals
        self.ret = ret
        self.strategy = strategy
        self.factor_bins = factor_bins
        self.ret_bins = ret_bins
        self.n_factors = n_factors
        self.disc_thresh = disc_thresh
        self.window_type = window_type
        self.window_size = window_size
        self.index = None
        self.weights = None
        self.port_ret = None

    def breakeven(self,
                  signal_type: Optional[str] = None,
                  centering: bool = True,
                  leverage: Optional[int] = None,
                  norm_method: Optional[str] = 'z-score',
                  winsorize: int = 3,
                  ts_norm: bool = False,
                  rebal_freq: Optional[Union[str, int]] = None,
                  tails: Optional[str] = None,
                  weighting: str = 'ew',
                  vol_target: float = 0.1,
                  ann_factor: int = 365,
                  plot_tcosts: bool = False,
                  source: Optional[str] = None
                  ):
        """
        Computes breakeven transaction costs.

        Finds value for transaction costs that would erode factor returns down to 0.

        Parameters
        ----------
        signal_type: str, {'norm', 'signal', 'signal_quantiles'}, default 'norm'
            norm: factor inputs are normalized into z-scores.
            signal: factor inputs are converted to signals between -1 and 1, and 0 and 2 for l/s and
            long-only strategies, respectively.
            signal_quantiles: factor inputs are converted to quantized signals between -1 and 1, or 0 and 2,
            with n bins.
        centering: bool, default True
            Centers values using the appropriate measure of central tendency used for the selected method. Otherwise,
            0 is used.
        leverage: int, default None
            Multiplies factors by integer to increase leverage
        norm_method: str, {'z-score', 'cdf', iqr', 'mod_z', 'min-max', 'percentile'}, default 'z-score'
                z-score: subtracts mean and divides by standard deviation.
                cdf: cumulative distribution function rescales z-scores to values between 0 and 1.
                iqr:  subtracts median and divides by interquartile range.
                mod_z: modified z-score using median absolute deviation.
                min-max: rescales to values between 0 and 1 by subtracting the min and dividing by the range.
                percentile: converts values to their percentile rank relative to the observations in the
                defined window type.
        winsorize: int, default 3
            Max/min value to use for winsorization/clipping for signals when method is z-score, iqr or mod z.
        ts_norm: bool, default False
            Normalizes factors over the time series before quantization over the cross section.
        rebal_freq: str or int, default None
            Rebalancing frequency. Can be day of week, e.g. 'monday', 'tuesday', etc, start, middle or end of month,
            e.g. 'month_end', '15th', or 'month_start', or an int for the number of days between rebalancing.
        tails: str, {'two', 'left', 'right'}, optional, default None
            Keeps only tail bins and ignores middle bins, 'two' for both tails, 'left' for left, 'right' for right
        weighting: str, {'ew', 'iv'}, default 'ew'
            Weights used to compute portfolio returns.
        vol_target: float, default 0.10
            Target annualized volatility.
        ann_factor: int, {12, 52, 252, 365}, default 365
            Annualization factor.
        plot_tcosts: bool, default False
            Plots breakeven transaction costs, sorted by values.
        source: str, default None
            Adds source info to bottom of plot.

        Returns
        -------
        be_tcosts: pd.Series
            Breakeven transaction costs for each factor.
        """
        # compute factors
        factors = self.compute_factors(signal_type=signal_type, centering=centering, leverage=leverage,
                                       norm_method=norm_method, winsorize=winsorize, ts_norm=ts_norm,
                                       rebal_freq=rebal_freq, tails=tails)
        if isinstance(factors, pd.Series):
            factors = factors.to_frame()

        # compute weights
        if weighting == 'iv':  # vol-adj weights
            inv_vol_df = self.compute_inv_vol_weights(vol_target=vol_target,
                                                      ann_factor=ann_factor)  # inv vol weights
            # scale factors
            scaled_factors_df = pd.concat([factors, inv_vol_df], axis=1)
            factors = scaled_factors_df.iloc[:, :-1].mul(scaled_factors_df.iloc[:, -1], axis=0)

        # gross factor ret
        df = pd.concat([factors.groupby(level=1).shift(1), self.ret], axis=1, join='inner')
        ret_df = df.iloc[:, :-1].mul(df.iloc[:, -1], axis=0).groupby(level=0).mean()
        cum_ret = ret_df.dropna().cumsum().iloc[-1]

        # compute turnover
        turn = abs(factors.groupby(level=1).diff().shift(1)).groupby(level=0).mean().dropna().cumsum().iloc[-1]

        # breakeven transaction costs, bps
        be_tcosts = (cum_ret / turn) * 10000

        # plot
        if plot_tcosts:
            # bar plot in Systamental style
            # plot size
            fig, ax = plt.subplots(figsize=(15, 7))

            # line colors
            colors = ['#98DAFF', '#FFA39F', '#6FE4FB', '#86E5D4', '#FFCB4D', '#D7DB5A', '#FFC2E3', '#F2CF9A',
                      '#BFD8E5']

            # plot
            be_tcosts.sort_values().plot(kind='barh', color=colors[7], ax=ax, rot=1)

            # grid
            ax.set_axisbelow(True)
            ax.grid(which="major", axis='x', color='#758D99', alpha=0.6, zorder=0)
            ax.set_facecolor("whitesmoke")
            ax.set_xlabel('Breakeven transaction cost, bps')

            # remove splines
            ax.spines[['top', 'right', 'left']].set_visible(False)

            # Reformat y-axis tick labels
            ax.yaxis.tick_right()

            # add systamental logo
            with resources.path("factorlab", "systamental_logo.png") as f:
                img_path = f
            img = Image.open(img_path)
            plt.figimage(img, origin='upper')

            # Add in title and subtitle
            plt.rcParams['font.family'] = 'georgia'
            ax.text(x=0.13, y=.92, s="Transaction Cost Analysis", transform=fig.transFigure, ha='left', fontsize=14,
                    weight='bold', alpha=.8, fontdict=None)
            ax.text(x=0.13, y=.89, s="Breakeven, bps", transform=fig.transFigure, ha='left', fontsize=12,
                    alpha=.8, fontdict=None)

            # Set source text
            if source is not None:
                ax.text(x=0.13, y=0.05, s=f"""Source: {source}""", transform=fig.transFigure, ha='left',
                        fontsize=10,
                        alpha=.8, fontdict=None)

        return be_tcosts


