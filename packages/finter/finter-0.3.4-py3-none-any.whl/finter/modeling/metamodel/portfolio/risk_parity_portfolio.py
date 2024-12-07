import os
import re
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

import numpy as np
import pandas as pd
from typing_extensions import Literal

from finter.backtest import USStockBacktestor, VietnamBacktestor, IndonesiaBacktestor
from finter.backtest.simulator import Simulator
from finter.data import ContentFactory, ModelData
from finter.framework_model.submission.helper_poetry import prepare_docker_submit_files
from finter.framework_model.submission.helper_submission import submit_model
from finter.modeling.metamodel.base import BaseMetaPortfolio
from finter.settings import logger


class RiskParityMetaPortfolio(BaseMetaPortfolio):
    risk: str = ""
    lookback_periods: str = ""
    rebalancing_periods: str = ""

    lookback_period_map = {"3M": 63, "6M": 126, "12M": 252}
    rebalancing_period_map = {"1W": "W", "1M": "M", "1Q": "Q"}

    class Parameters(BaseMetaPortfolio.Parameters):
        risk: Literal["Volatility", "MDD", "TuW"]
        lookback_periods: Literal["3M", "6M", "12M"]
        rebalancing_periods: Literal["1W", "1M", "1Q"]

    # Helper functions
    @staticmethod
    def daily_return_to_nav(daily_returns):
        def calculate_nav(daily_return):
            # 첫 값이 1로 시작하는 NaV 시리즈 생성
            nav_series = (1 + daily_return).cumprod()
            # 첫 값 1을 시리즈의 시작에 추가
            return nav_series

        return {
            alpha: calculate_nav(daily_returns[alpha]) for alpha in daily_returns.keys()
        }

    @staticmethod
    def calculate_previous_start_date(start_date, lookback_days):
        start = datetime.strptime(str(start_date), "%Y%m%d")
        previous_start = start - timedelta(days=lookback_days)
        return int(previous_start.strftime("%Y%m%d"))

    @staticmethod
    def retain_first_of_period(data: pd.Series, period: str) -> pd.Series:
        tmp = data.index[-2:-1].append(data.index[0:-1])
        mask = data.index.to_period(period) != tmp.to_period(period)
        return data[mask]

    @staticmethod
    def calculate_volatility(ret_dict, alpha_list, lookback_periods):
        return {
            alpha: ret_dict[alpha].rolling(window=lookback_periods).std()
            for alpha in alpha_list
        }

    @staticmethod
    def calculate_MDD(ret_dict, alpha_list, lookback_periods):
        def calculate_DD(series):
            nav = (1 + series).cumprod()
            dd = pd.Series(nav).cummax() - nav
            return dd.max()

        return {
            alpha: ret_dict[alpha]
            .rolling(window=lookback_periods)
            .apply(lambda x: calculate_DD(x))
            for alpha in alpha_list
        }

    @staticmethod
    def calculate_TuW(ret_dict, alpha_list, lookback_periods):
        def calculate_tuw(series):
            nav = (1 + series).cumprod()
            dd = pd.Series(nav).cummax() - nav
            return (dd > 0).astype(int).sum()

        return {
            alpha: ret_dict[alpha]
            .rolling(window=lookback_periods)
            .apply(lambda x: calculate_tuw(x))
            for alpha in alpha_list
        }

    @staticmethod
    def risk_parity_weights(volatilities):
        adjusted_volatilities = volatilities.replace(
            0, 1e-4
        )  # inf를 막기 위한 방어 로직

        inv_volatilities = 1 / adjusted_volatilities
        weights = inv_volatilities / inv_volatilities.sum()
        return weights

    @staticmethod
    def get_alphas(alpha_loader, alpha_list):
        alpha_dict = {
            alpha: alpha_loader.get_alpha(alpha)
            .replace(0, np.nan)
            .dropna(how="all", axis=1)
            .fillna(0)
            for alpha in alpha_list
        }
        ret_columns = set()
        for alpha in alpha_list:
            ret_columns.update(alpha_dict[alpha].columns)
        return alpha_dict, list(ret_columns)

    @staticmethod
    def get_summary(alpha_dict, close, universe):
        def backtest(alpha, close, universe):
            if universe == "kr_stock":
                bt = Simulator(
                    alpha.fillna(0),
                    close.reindex(alpha.index),
                    initial_cash=1e8,
                    buy_fee_tax=0,
                    sell_fee_tax=30,
                    slippage=10,
                )
            elif universe in [
                "us_etf",
                "us_stock",
                "us_factset_etf",
                "us_factset_stock",
            ]:
                bt = USStockBacktestor(
                    alpha.fillna(0),
                    close.reindex(alpha.index),
                    initial_cash=1e8,
                    buy_fee_tax=0,
                    sell_fee_tax=30,
                    slippage=10,
                )
            elif universe == "vn_stock":
                bt = VietnamBacktestor(
                    alpha.fillna(0),
                    close.reindex(alpha.index),
                    initial_cash=1e8,
                    buy_fee_tax=40,
                    sell_fee_tax=50,
                    slippage=10,
                )
            elif universe == "id_stock":
                bt = IndonesiaBacktestor(
                    alpha.fillna(0),
                    close.reindex(alpha.index),
                    initial_cash=1e8,
                    buy_fee_tax=45,
                    sell_fee_tax=55,
                    slippage=10,
                )
            else:
                raise ValueError(f"unsupported universe {universe}")
            bt.run()
            return bt.summary

        return {
            alpha: backtest(alpha_dict[alpha], close, universe)
            for alpha in alpha_dict.keys()
        }

    def get(self, start, end):
        self.lookback_periods = self.lookback_period_map.get(
            self.lookback_periods, self.lookback_periods
        )

        pre_start = self.calculate_previous_start_date(start, self.lookback_periods * 4)

        alpha_loader = self.alpha_loader(pre_start, end)
        alpha_dict, ret_columns = self.get_alphas(alpha_loader, self.alpha_list)

        model_info = self.get_model_info()
        cf = True
        universe = "kr_stock"

        if model_info["exchange"] == "us":
            if model_info["universe"] == "compustat":
                if model_info["instrument_type"] == "stock":
                    universe = "us_stock"
                elif model_info["instrument_type"] == "etf":
                    universe = "us_etf"
            else:
                cf = False
        elif model_info["exchange"] == "vnm":
            if model_info["instrument_type"] == "stock":
                universe = "vn_stock"
        elif model_info["exchange"] == "id":
            if model_info["instrument_type"] == "stock":
                universe = "id_stock"

        if cf:
            self.close = ContentFactory(universe, pre_start, end).get_df(
                "price_close", adj_div=True
            )
        else:
            self.close = ModelData.load(
                f"content.factset.api.price_volume.us-{model_info['instrument_type']}-price_close.1d"
            )
            self.close *= ModelData.load(
                f"content.factset.api.cax.us-{model_info['instrument_type']}-adjust_factor.1d"
            )
            self.close *= ModelData.load(
                f"content.factset.api.cax.us-{model_info['instrument_type']}-dividend_factor.1d"
            )
            universe = f"us_factset_{model_info['instrument_type']}"

        self.summary_dict = self.get_summary(alpha_dict, self.close, universe)
        self.ret_dict = {
            alpha: self.summary_dict[alpha].nav.pct_change().shift(1)
            for alpha in self.alpha_list
        }

        risk_calculation_method = {
            "Volatility": self.calculate_volatility,
            "MDD": self.calculate_MDD,
            "TuW": self.calculate_TuW,
        }

        self.risk_df = pd.DataFrame(
            risk_calculation_method[self.risk](
                self.ret_dict, self.alpha_list, self.lookback_periods
            )
        )

        period = self.rebalancing_period_map.get(self.rebalancing_periods, "M")
        parsed_risk = self.retain_first_of_period(self.risk_df, period)

        self.weights = parsed_risk.apply(self.risk_parity_weights, axis=1)
        weights = self.weights.reindex(self.risk_df.index).ffill()

        self.scaled_dict = dict()

        for alpha in self.alpha_list:
            self.scaled_dict[alpha] = (
                alpha_dict[alpha]
                .mul(weights[alpha].loc[alpha_dict[alpha].index], axis=0)
                .reindex(columns=ret_columns)
                .fillna(0)
            )

        combined_position = pd.DataFrame(
            index=self.risk_df.index, columns=ret_columns
        ).fillna(0)
        for alpha in self.alpha_list:
            combined_position += self.scaled_dict[alpha]
        return combined_position.shift(1).loc[str(start) : str(end)]

    @classmethod
    def submit(
        cls,
        model_name: str,
        staging: bool = False,
        outdir: Optional[str] = None,
        **kwargs,
    ):
        """
        Submits the portfolio model to the Finter platform.

        :param docker_submit: Whether to submit the model using Docker.
        :param outdir: if not null, submitted code and json file are saved.
        :return: The result of the submission if successful, None otherwise.
        """

        @contextmanager
        def nullcontext():
            yield outdir

        context = TemporaryDirectory() if outdir is None else nullcontext()

        with context as odir:
            assert odir is not None
            source = cls.get_submit_code()
            modeldir = Path(odir) / model_name
            os.makedirs(modeldir, exist_ok=True)
            with open(
                modeldir / cls._model_type.file_name, "w", encoding="utf-8"
            ) as fd:
                fd.write(source)
            model_info = cls.get_model_info()
            if "insample" in kwargs:
                insample = kwargs.pop("insample")

                if not re.match(r"^\d+ days$", insample):
                    raise ValueError("insample should be like '100 days'")

                model_info["insample"] = insample

            if kwargs:
                logger.warn(f"Unused parameters: {kwargs}")

            prepare_docker_submit_files(modeldir, gpu=None, image=None)

            return submit_model(
                model_info, str(modeldir), docker_submit=True, staging=staging
            )
