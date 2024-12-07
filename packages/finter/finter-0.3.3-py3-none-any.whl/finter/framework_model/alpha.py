from abc import ABCMeta, abstractmethod

import pandas as pd

from finter.framework_model import ContentModelLoader


class BaseAlpha(metaclass=ABCMeta):
    __CM_LOADER = ContentModelLoader()
    __cm_set = set()

    start, end, universe, data_handler = None, None, None, None

    @abstractmethod
    def get(self, start, end):
        pass

    @classmethod
    def get_cm(cls, key):
        if key.startswith("content."):
            cls.__cm_set.add(key)
        else:
            cls.__cm_set.add("content." + key)
        return cls.__CM_LOADER.load(key)

    def depends(self):
        return self.__cm_set

    @staticmethod
    def cleanup_position(position: pd.DataFrame):
        df_cleaned = position.loc[:, ~((position == 0) | (position.isna())).all(axis=0)]
        if df_cleaned.empty:
            df_cleaned = position

        return df_cleaned.fillna(0)

    def backtest(self, universe=None, start=None, end=None, data_handler=None):
        from finter.backtest.main import Simulator

        if universe is not None:
            self.universe = universe
        if start is not None:
            self.start = start
        if end is not None:
            self.end = end
        if data_handler is not None:
            self.data_handler = data_handler

        # Collect missing attributes in a list comprehension
        missing_attrs = [
            attr
            for attr in [
                "start",
                "end",
                "universe",
            ]
            if getattr(self, attr) is None
        ]
        if missing_attrs:
            # Raise a ValueError with a concise message
            raise ValueError(
                f"Missing required attributes: {', '.join(missing_attrs)}. Please set them before calling backtest(). or backtest(start, end, universe)"
            )

        simulator = Simulator(self.start, self.end, data_handler=self.data_handler)
        simulator = simulator.run(
            universe=self.universe, position=self.get(self.start, self.end)
        )
        return simulator.summary


"""
from finter import BaseAlpha
from finter.data import ContentFactory


class Alpha(BaseAlpha):
    universe = "id_stock"

    def get(self, start, end):
        cf = ContentFactory(self.universe, start, end)
        df = cf.get_df("price_close")
        return df


if __name__ == "__main__":
    alpha = Alpha()
    res = alpha.backtest(universe=alpha.universe, start=20230101, end=20240101)
"""
