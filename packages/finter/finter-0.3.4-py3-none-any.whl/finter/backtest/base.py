import numpy as np
import pandas as pd
from finter.modeling.utils import daily2period
from typing_extensions import Literal

# Todo
# - volcap
# - buy & hold frequency


class BaseBacktestor:
    def __init__(
        self,
        position: pd.DataFrame,
        price: pd.DataFrame,
        initial_cash: np.float64,
        buy_fee_tax: np.float64,
        sell_fee_tax: np.float64,
        slippage: np.float64,
        volume: pd.DataFrame = None,
        volume_capacity_ratio: np.float64 = 0,
        resample_period: Literal[None, "W", "M", "Q"] = None,
    ) -> None:
        if resample_period:
            position = daily2period(position, resample_period, keep_index=True)

        non_zero_columns = position.columns[position.sum() != 0]
        self.weight, self.price, self.dates, self.common_columns = self.preprocess_data(
            position[non_zero_columns], price[non_zero_columns]
        )

        self.volume_capacity = self.preprocess_volume_capacity(
            volume, volume_capacity_ratio
        )

        self.initial_cash = initial_cash

        # Todo: matrix fee
        self.buy_fee_tax = buy_fee_tax / 10000
        self.sell_fee_tax = sell_fee_tax / 10000

        # Todo: matrix slipage
        self.slippage = slippage / 10000

        # Todo: user set buy price, sell price
        self.buy_price = self.price * (1 + self.slippage)
        self.sell_price = self.price * (1 - self.slippage)

        self.num_assets = self.weight.shape[1]
        self.num_days = self.weight.shape[0]

        self.initialize_variables()

        self.position = position

        self._results = BacktestResult(self)

    def preprocess_data(self, position: pd.DataFrame, price: pd.DataFrame) -> tuple:
        weight = position / 1e8
        common_columns = weight.columns.intersection(price.columns)

        weight = weight[common_columns]
        price = price[common_columns]

        first_position_index = weight.index[0]
        price_index_pos = price.index.get_loc(first_position_index)

        if price_index_pos == 0:
            price_index_pos = 1

        price = price.iloc[price_index_pos - 1 : price_index_pos + len(weight)]
        weight = weight.reindex(price.index)

        return weight.to_numpy(), price.to_numpy(), weight.index, common_columns

    def preprocess_volume_capacity(
        self, volume: pd.DataFrame, volume_capacity_ratio: np.float64
    ) -> np.ndarray:
        if volume is None or volume_capacity_ratio == 0:
            volume = pd.DataFrame(np.inf, index=self.dates, columns=self.common_columns)
            return volume.to_numpy()
        else:
            volume = volume.reindex(self.dates, columns=self.common_columns)
            return volume.fillna(0).to_numpy() * volume_capacity_ratio

    def initialize_variables(self) -> None:
        shape = (self.num_days, self.num_assets)

        self.actual_holding_volume = np.full(shape, np.nan, dtype=np.float64)
        self.target_volume = np.full(shape, np.nan, dtype=np.float64)
        self.target_buy_volume = np.full(shape, np.nan, dtype=np.float64)
        self.target_sell_volume = np.full(shape, np.nan, dtype=np.float64)
        self.actual_sell_volume = np.full(shape, np.nan, dtype=np.float64)
        self.actual_sell_amount = np.full(shape, np.nan, dtype=np.float64)
        self.available_buy_amount = np.full(
            (self.num_days, 1), np.nan, dtype=np.float64
        )
        self.target_buy_amount = np.full(shape, np.nan, dtype=np.float64)
        self.target_buy_amount_sum = np.full(
            (self.num_days, 1), np.nan, dtype=np.float64
        )
        self.available_buy_volume = np.full(shape, np.nan, dtype=np.float64)
        self.actual_buy_volume = np.full(shape, np.nan, dtype=np.float64)
        self.actual_buy_amount = np.full(shape, np.nan, dtype=np.float64)
        self.valuation = np.full(shape, np.nan, dtype=np.float64)
        self.cash = np.full((self.num_days, 1), np.nan, dtype=np.float64)
        self.nav = np.full((self.num_days, 1), np.nan, dtype=np.float64)

        self.actual_holding_volume[0] = 0
        self.cash[0] = self.initial_cash
        self.nav[0] = self.initial_cash

    def _clear_all_variables(self):
        for attr in list(self.__dict__.keys()):
            if attr not in ["summary", "_results", "position", "valuation"]:
                delattr(self, attr)

    def run(self):
        raise NotImplementedError(
            "The backtest method should be implemented by subclasses"
        )

    @property
    def result(self):
        try:
            self._results.summary
        except AttributeError:
            raise Warning("Deprecated attribute, use summary instead")
        return self._results

    @property
    def _summary(self):
        return self._results.summary

    def plot_single(self, single_asset):
        return self._results.plot_single(single_asset)


class BacktestResult:
    def __init__(self, simulator: BaseBacktestor) -> None:
        self.simulator = simulator

    @property
    def nav(self) -> pd.DataFrame:
        return pd.DataFrame(
            self.simulator.nav, index=self.simulator.dates, columns=["nav"]
        )

    @property
    def cash(self) -> pd.DataFrame:
        return pd.DataFrame(
            self.simulator.cash, index=self.simulator.dates, columns=["cash"]
        )

    @property
    def valuation(self) -> pd.DataFrame:
        return pd.DataFrame(
            self.simulator.valuation.sum(axis=1),
            index=self.simulator.dates,
            columns=["valuation"],
        )

    @property
    def cost(self) -> pd.DataFrame:
        cost = np.nansum(
            (
                self.simulator.actual_buy_volume
                * self.simulator.buy_price
                * self.simulator.buy_fee_tax
            )
            + (
                self.simulator.actual_sell_volume
                * self.simulator.sell_price
                * self.simulator.sell_fee_tax
            ),
            axis=1,
        )
        return pd.DataFrame(
            cost,
            index=self.simulator.dates,
            columns=["cost"],
        )

    @property
    def slippage(self) -> pd.DataFrame:
        slippage = np.nansum(
            (
                self.simulator.actual_buy_volume
                * self.simulator.buy_price
                * (self.simulator.slippage / (1 + self.simulator.slippage))
            )
            + (
                self.simulator.actual_sell_volume
                * self.simulator.sell_price
                * (self.simulator.slippage / (1 - self.simulator.slippage))
            ),
            axis=1,
        )
        return pd.DataFrame(
            slippage,
            index=self.simulator.dates,
            columns=["slippage"],
        )

    @property
    def summary(self) -> pd.DataFrame:
        pnl = self.nav.diff().fillna(0) - self.cost.values
        pnl.columns = ("pnl",)

        result = pd.concat(
            [
                self.nav,
                self.cash,
                self.valuation,
                self.cost,
                self.slippage,
                pnl,
            ],
            axis=1,
        )
        return result

    @property
    def average_buy_price(self) -> pd.DataFrame:
        shape = (self.simulator.num_days, self.simulator.num_assets)

        self.cummulative_buy_amount = np.full(shape, np.nan, dtype=np.float64)
        self.__average_buy_price = np.full(shape, np.nan, dtype=np.float64)

        self.cummulative_buy_amount[0] = 0
        self.__average_buy_price[0] = 0

        for i in range(1, self.simulator.num_days):
            self.cummulative_buy_amount[i] = (
                self.cummulative_buy_amount[i - 1]
                + (
                    self.simulator.actual_buy_volume[i]
                    * np.nan_to_num(self.simulator.buy_price[i])
                )
                - (
                    self.simulator.actual_sell_volume[i]
                    * self.__average_buy_price[i - 1]
                )
            )

            self.__average_buy_price[i] = np.nan_to_num(
                self.cummulative_buy_amount[i] / self.simulator.actual_holding_volume[i]
            )

        return pd.DataFrame(
            self.__average_buy_price,
            index=self.simulator.dates,
            columns=self.simulator.common_columns,
        )

    @property
    def realized_pnl(self) -> pd.DataFrame:
        return (
            np.nan_to_num(self.simulator.sell_price) - self.average_buy_price.shift()
        ) * self.simulator.actual_sell_volume

    @property
    def unrealized_pnl(self) -> pd.DataFrame:
        return (
            np.nan_to_num(self.simulator.price) - self.average_buy_price
        ) * self.simulator.actual_holding_volume

    def plot_single(self, single_asset):
        import plotly.graph_objs as go
        from plotly.subplots import make_subplots

        assert (
            single_asset in self.simulator.position.columns
        ), f"{single_asset} should be in position"
        assert self.simulator.valuation.size != 0, "Valuation can not empty"

        non_zero_position = self.simulator.position.loc[
            :, self.simulator.position.sum() != 0
        ]
        if self.simulator.position.shape == self.simulator.valuation.shape:
            valuation_df = pd.DataFrame(
                self.simulator.valuation,
                index=self.simulator.position.index,
                columns=self.simulator.position.columns,
            )
        elif non_zero_position.shape == self.simulator.valuation.shape:
            valuation_df = pd.DataFrame(
                self.simulator.valuation,
                index=non_zero_position.index,
                columns=non_zero_position.columns,
            )
        else:
            try:
                non_zero_position = non_zero_position.loc[self.simulator.summary.index,]
                non_zero_valuation = self.simulator.valuation[
                    :, np.nansum(self.simulator.valuation, axis=0) != 0
                ]

                valuation_df = pd.DataFrame(
                    non_zero_valuation,
                    index=non_zero_position.index,
                    columns=non_zero_position.columns,
                )
            except Exception as e:
                print(e)
                assert (
                    False
                ), f"position and valuation shape is different.\nposition {self.simulator.position.shape}; valuation {self.simulator.valuation.shape}"

        valuation_single = valuation_df[single_asset]

        position_single = non_zero_position[single_asset].fillna(0)
        position_previous = position_single.shift(1)
        position_next = position_single.shift(-1)

        # valuation_percent 계산
        # valuation의 차이로 계산해서 기말에 사고, 기초에 파는 효과로 나옴
        # 조건 정의 (각각 별도의 Series 사용)
        position_end = position_single != position_next
        entry = (position_previous <= 0) & (position_single > 0)
        short = (position_previous >= 0) & (position_single < 0)
        add = (
            (position_single > position_previous)
            & (position_single != 0)
            & ~entry
            & ~short
            & ~position_end
        )
        reduce = (
            (position_single < position_previous)
            & (position_single != 0)
            & ~entry
            & ~short
            & ~position_end
        )

        signal = np.where(
            entry,
            2,
            np.where(
                add,
                1,
                np.where(reduce, -1, np.where(short, -2, np.where(position_end, 3, 0))),
            ),
        )

        pnl_df = pd.DataFrame(valuation_single)
        pnl_df["signal_start"] = signal
        pnl_df["pnl_percent_start"] = (
            pnl_df[signal != 0][single_asset].pct_change() * 100
        ).shift(-1)
        pnl_df["pnl_start"] = pnl_df[(signal != 0)][single_asset].diff().shift(-1)

        pnl_df["signal_end"] = signal
        pnl_df["signal_end"] = pnl_df[signal != 0]["signal_end"].shift(1)
        pnl_df["pnl_percent_end"] = (
            pnl_df[(signal != 0)][single_asset].pct_change() * 100
        )

        pnl_df["pnl_start"] = np.where(
            pnl_df["pnl_percent_start"].abs() == 100, 0, pnl_df["pnl_start"]
        )
        pnl_df["pnl_start"] = np.where(
            pnl_df[single_asset] < 0, -pnl_df["pnl_start"], pnl_df["pnl_start"]
        )
        pnl_df["pnl_start"] = np.where(
            (pnl_df["signal_start"] == 3), np.nan, pnl_df["pnl_start"]
        )
        pnl_df["pnl_percent_start"] = np.where(
            pnl_df["pnl_percent_start"].abs() == 100, 0, pnl_df["pnl_percent_start"]
        )
        pnl_df["pnl_percent_end"] = np.where(
            pnl_df["pnl_percent_end"].abs() == 100, 0, pnl_df["pnl_percent_end"]
        )

        pnl_df["ffill_signal"] = pnl_df.signal_start.replace(0, np.nan).fillna(
            method="ffill"
        )
        pnl_df["ffill_pnl_percent"] = pnl_df.pnl_percent_start.fillna(method="ffill")

        fig = make_subplots(
            rows=3,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=("Position", "Valuation(Trading)", "Profit And Loss"),
        )

        # 선 그래프
        valuation_line = go.Scatter(
            x=valuation_single.index,
            y=valuation_single.values,
            mode="lines",
            name="Valuation",
        )

        pnl_line = go.Scatter(
            x=pnl_df["pnl_start"].index,
            y=pnl_df["pnl_start"].fillna(method="ffill"),
            mode="lines",
            name="PNL",
        )
        pnl_cumsum_line = go.Scatter(
            x=pnl_df["pnl_start"].index,
            y=pnl_df["pnl_start"].fillna(0).cumsum(),
            mode="lines",
            name="PNL_cumsum",
        )

        # 진입 포인트 (빨간색 세모)
        trace_entry = go.Scatter(
            x=pnl_df[pnl_df.signal_start == 2].index,
            y=pnl_df[pnl_df.signal_start == 2]["pnl_percent_start"],
            mode="markers",
            marker=dict(symbol="triangle-up", color="red", size=10),
            name="Long",
        )

        trace_entry2 = go.Scatter(
            x=pnl_df[pnl_df.signal_end == 2].index,
            y=pnl_df[pnl_df.signal_end == 2]["pnl_percent_end"],
            mode="markers",
            marker=dict(symbol="triangle-up", color="red", size=10),
            name="Long",
        )

        line_entry = go.Scatter(
            x=pnl_df.index,
            y=np.where(
                pnl_df["ffill_signal"] == 2, pnl_df["ffill_pnl_percent"], np.nan
            ),
            mode="lines",
            name="Long",
            line=dict(color="red"),
        )

        # 추매 포인트 (빨간색 세모)
        trace_add = go.Scatter(
            x=pnl_df[pnl_df.signal_start == 1].index,
            y=pnl_df[pnl_df.signal_start == 1]["pnl_percent_start"],
            mode="markers",
            marker=dict(symbol="triangle-up", color="red", size=5),
            name="Add",
        )

        trace_add2 = go.Scatter(
            x=pnl_df[pnl_df.signal_end == 1].index,
            y=pnl_df[pnl_df.signal_end == 1]["pnl_percent_end"],
            mode="markers",
            marker=dict(symbol="triangle-up", color="red", size=5),
            name="Add",
        )

        line_add = go.Scatter(
            x=pnl_df.index,
            y=np.where(
                pnl_df["ffill_signal"] == 1, pnl_df["ffill_pnl_percent"], np.nan
            ),
            mode="lines",
            name="Add",
            line=dict(color="rgba(255, 0, 0, 0.2)"),
        )

        # 매도 포인트 (파란색 세모)
        trace_short = go.Scatter(
            x=pnl_df[pnl_df.signal_start == -2].index,
            y=pnl_df[pnl_df.signal_start == -2]["pnl_percent_start"],
            mode="markers",
            marker=dict(symbol="triangle-down", color="blue", size=10),
            name="Short",
        )

        trace_short2 = go.Scatter(
            x=pnl_df[pnl_df.signal_end == -2].index,
            y=pnl_df[pnl_df.signal_end == -2]["pnl_percent_end"],
            mode="markers",
            marker=dict(symbol="triangle-down", color="blue", size=10),
            name="Short",
        )

        line_short = go.Scatter(
            x=pnl_df.index,
            y=np.where(
                pnl_df["ffill_signal"] == -2, pnl_df["ffill_pnl_percent"], np.nan
            ),
            mode="lines",
            name="Short",
            line=dict(color="blue"),
        )

        # 매도 포인트 (파란색 세모)
        trace_down = go.Scatter(
            x=pnl_df[pnl_df.signal_start == -1].index,
            y=pnl_df[pnl_df.signal_start == -1]["pnl_percent_start"],
            mode="markers",
            marker=dict(symbol="triangle-down", color="blue", size=5),
            name="Reduce",
        )

        trace_down2 = go.Scatter(
            x=pnl_df[pnl_df.signal_end == -1].index,
            y=pnl_df[pnl_df.signal_end == -1]["pnl_percent_end"],
            mode="markers",
            marker=dict(symbol="triangle-down", color="blue", size=5),
            name="Reduce",
        )

        line_down = go.Scatter(
            x=pnl_df.index,
            y=np.where(
                pnl_df["ffill_signal"] == -1, pnl_df["ffill_pnl_percent"], np.nan
            ),
            mode="lines",
            name="Reduce",
            line=dict(color="rgba(0, 0, 255, 0.2)"),
        )

        fig.add_trace(trace_entry, row=1, col=1)
        fig.add_trace(trace_entry2, row=1, col=1)
        fig.add_trace(trace_add, row=1, col=1)
        fig.add_trace(trace_add2, row=1, col=1)
        fig.add_trace(trace_down, row=1, col=1)
        fig.add_trace(trace_down2, row=1, col=1)
        fig.add_trace(trace_short, row=1, col=1)
        fig.add_trace(trace_short2, row=1, col=1)

        fig.add_trace(line_entry, row=1, col=1)
        fig.add_trace(line_add, row=1, col=1)
        fig.add_trace(line_down, row=1, col=1)
        fig.add_trace(line_short, row=1, col=1)

        fig.add_trace(valuation_line, row=2, col=1)

        fig.add_trace(pnl_line, row=3, col=1)
        fig.add_trace(pnl_cumsum_line, row=3, col=1)

        # 레이아웃 설정
        fig.update_layout(height=600, hovermode="x unified")

        # 그래프 그리기
        fig.show()
