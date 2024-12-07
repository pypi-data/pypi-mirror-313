from datetime import datetime
from finter.calendar import iter_trading_days

import numpy as np
import pandas as pd
from finter.framework_model.content import Loader

initial_date = 19820131


def safe_apply_fiscal(x):
    if pd.isna(x):
        return x
    return max(x.keys())


def safe_apply_value(x):
    if pd.isna(x):
        return x
    return x[max(x.keys())]


def slice_df(df, start, end):
    return df.dropna(how="all").loc[
        datetime.strptime(str(start), "%Y%m%d") : datetime.strptime(str(end), "%Y%m%d")
    ]


def safe_apply_boolean(cell, mask):
    if not mask:  # mask가 False이면 NaN 반환
        return np.nan
    return cell  # mask가 True이면 원래 값 유지


class CompustatFinancialPitLoader(Loader):
    def __init__(self, cm_name):
        self.__CM_NAME = cm_name
        self.__FREQ = cm_name.split(".")[-1]

    @staticmethod
    def _unpivot_df(raw):
        unpivot_df = raw.unstack().dropna().reset_index()
        unpivot_df.columns = ["id", "pit", "val"]
        m = (
            pd.DataFrame([*unpivot_df["val"]], unpivot_df.index)
            .stack()
            .rename_axis([None, "fiscal"])
            .reset_index(1, name="value")
        )
        result = unpivot_df[["id", "pit"]].join(m)
        return result.dropna(subset=["fiscal", "value"])

    def get_df(
        self,
        start: int,
        end: int,
        fill_nan=True,
        mode: str = "default",
        quantit_universe=True,
        *args,
        **kwargs
    ):
        """
        Fetch the financial data within a specified date range.

        Parameters
        ----------
        mode : str, optional
            Mode of data return. It can be one of the following:
            'default'  - Return the data with the safe apply function, which can be used directly after loading for modeling purposes (default behavior).
            'unpivot'  - Return the data in an unpivoted (long) format.
            'original' - Return the original raw data.

        Returns
        -------
        pandas.DataFrame
            The requested financial data in the specified format.

        Examples
        --------
        loader = CompustatFinancialPitLoader("some.cm.name")

        # Default data format
        df_default = loader.get_df(start=19820101, end=20230101, mode='default')

        # Unpivoted data format
        df_unpivot = loader.get_df(start=19820101, end=20230101, mode='unpivot')

        # Original raw data
        df_original = loader.get_df(start=19820101, end=20230101, mode='original')
        """
        assert mode in {
            "default",
            "unpivot",
            "original",
        }, "Mode must be one of 'default', 'unpivot', or 'original'."

        raw = self._load_cache(
            self.__CM_NAME,
            initial_date,
            end,
            freq=self.__FREQ,
            fill_nan=fill_nan,
            cache_t="hdf",
        ).dropna(how="all")

        if quantit_universe:
            univ = self._load_cache(
                "content.spglobal.compustat.universe.us-stock-constituent.1d",
                19980401,  # to avoid start dependency in dataset
                end,
                universe="us-compustat-stock",
                freq=self.__FREQ,
                fill_nan=fill_nan,
                *args,
                **kwargs,
            )
            univ.columns = [col[:6] for col in univ.columns]
            univ = univ.T.groupby(univ.columns).any().T
            univ = univ.reindex(pd.date_range(start=univ.index[0], end=univ.index[-1], freq='D')).fillna(method='ffill')

            raw = raw.where(univ, np.nan)

        if mode == "unpivot":
            raw = slice_df(raw, start, end)
            raw = CompustatFinancialPitLoader._unpivot_df(raw)
            return raw
        elif mode == "original":
            raw = slice_df(raw, start, end)
            trading_dates = sorted(iter_trading_days(start, end, "us"))
            return raw.reindex(trading_dates)
        else:
            trading_dates = sorted(iter_trading_days(start, end, "us"))
            max_fiscal = raw.applymap(safe_apply_fiscal).astype(float)
            raw = raw.applymap(safe_apply_value)
            return raw[max_fiscal == max_fiscal.cummax()].reindex(trading_dates)
