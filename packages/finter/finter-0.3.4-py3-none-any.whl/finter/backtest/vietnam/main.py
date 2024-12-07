import pandas as pd
import numpy as np
from numba import njit

from finter.backtest.base import BaseBacktestor, BacktestResult
from finter.backtest.core import (
    calculate_buy_sell_volumes,
    update_nav,
    update_valuation_and_cash,
)

# Todo
# - volcap
# - buy & hold frequency


class VietnamBacktestor(BaseBacktestor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._results = VietnamResult(self)

    def run(self, future_fee_tax = 5, auto_rebalance=True, debug=False):
        self.future_fee_tax = future_fee_tax / 10000
        for i in range(1, self.num_days):
            # Todo: use base price
            short = False
            if self.weight[i].sum() < 0: # todo : should be deleted
                short = True
            
            self.target_volume[i] = update_target_volume(
                self.weight[i],
                self.nav[i - 1, 0],
                self.price[i - 1],
                self.weight[i - 1],
                self.target_volume[i - 1],
                auto_rebalance,
                i == 1,
            )
            if i < 3:
                available_sell_volume = np.zeros_like(self.target_volume[i])
            else:
                available_sell_volume = (
                    self.actual_holding_volume[i - 3]
                    - self.actual_sell_volume[i - 2]
                    - self.actual_sell_volume[i - 1]
                )

            (
                self.target_buy_volume[i],
                self.target_sell_volume[i],
                self.actual_sell_volume[i],
            ) = calculate_buy_sell_volumes(
                self.target_volume[i],
                self.actual_holding_volume[i - 1],
                available_sell_volume=available_sell_volume if not short else None, # todo : should be deleted
                volume_capacity=self.volume_capacity[i],
            )

            (
                self.actual_sell_amount[i],
                self.available_buy_amount[i, 0],
                self.actual_buy_volume[i],
                self.actual_buy_amount[i],
            ) = execute_transactions(
                self.actual_sell_volume[i],
                self.buy_price[i],
                self.buy_fee_tax,
                self.sell_price[i],
                self.sell_fee_tax,
                self.cash[i - 1, 0],
                self.target_buy_volume[i],
                self.actual_holding_volume[i - 1],
                self.future_fee_tax,
            )

            self.actual_holding_volume[i], self.valuation[i], self.cash[i, 0] = (
                update_valuation_and_cash(
                    self.actual_holding_volume[i - 1],
                    self.actual_buy_volume[i],
                    self.actual_sell_volume[i],
                    self.price[i],
                    self.available_buy_amount[i, 0],
                    self.actual_buy_amount[i],
                )
            )

            self.nav[i, 0] = update_nav(self.cash[i, 0], self.valuation[i])

        if not debug:
            self.summary = self._summary
            self._clear_all_variables()
        else:
            self.summary = self._summary


@njit(cache=True)
def update_target_volume(
    weight: np.ndarray,
    prev_nav: np.float64,
    prev_price: np.ndarray,
    prev_weight: np.ndarray,
    target_volume_before: np.ndarray,
    auto_rebalance: bool,
    is_first_day: bool,
) -> np.ndarray:
    if auto_rebalance or (np.abs(weight - prev_weight) > 1e-10).any() or is_first_day:
        result = (np.nan_to_num((weight * prev_nav) / (prev_price * 100)) * 100).astype(
            target_volume_before.dtype
        )
        return result
    else:
        return target_volume_before


@njit(cache=True)
def execute_transactions(
    actual_sell_volume: np.ndarray,
    buy_price: np.ndarray,
    buy_fee_tax: np.float64,
    sell_price: np.ndarray,
    sell_fee_tax: np.float64,
    prev_cash: np.float64,
    target_buy_volume: np.ndarray,
    prev_actual_holding_volume: np.ndarray,
    future_fee_tax: np.float64,
) -> tuple:
    sell_spot_volume = np.minimum(actual_sell_volume, prev_actual_holding_volume)
    sell_spot_volume[sell_spot_volume < 0] = 0
    sell_future_volume = actual_sell_volume - sell_spot_volume
    
    actual_sell_amount = np.nan_to_num(
        sell_spot_volume * sell_price * (1 - sell_fee_tax) + sell_future_volume * sell_price * (1 - future_fee_tax)
    )
    available_buy_amount = prev_cash + actual_sell_amount.sum()

    buy_future_volume = np.where(
        prev_actual_holding_volume < 0,
        -1 * prev_actual_holding_volume,
        np.zeros_like(prev_actual_holding_volume)
    )
    buy_spot_volume = target_buy_volume - buy_future_volume
        
    target_buy_amount = np.nan_to_num(
        buy_spot_volume * buy_price * (1 + buy_fee_tax) + buy_future_volume * buy_price * (1 + future_fee_tax)
    )
    
    target_buy_amount_sum = target_buy_amount.sum()
    if target_buy_amount_sum > 0:
        available_buy_volume = (
            np.nan_to_num(
                (target_buy_amount / target_buy_amount_sum)
                * (available_buy_amount / (buy_price * (1 + buy_fee_tax) * 100))
            ).astype(np.int64)
            * 100
        )
        actual_buy_volume = np.minimum(available_buy_volume, target_buy_volume)

        actual_buy_amount = np.nan_to_num(
            actual_buy_volume * buy_price * (1 + buy_fee_tax)
        )
    else:
        actual_buy_volume = np.zeros_like(target_buy_volume)
        actual_buy_amount = np.zeros_like(target_buy_volume)
    return (
        actual_sell_amount,
        available_buy_amount,
        actual_buy_volume,
        actual_buy_amount,
    )

class VietnamResult(BacktestResult):
    @property
    def cost(self) -> pd.DataFrame:
        # 이전 시점의 보유 수량 계산
        prev_holding = np.roll(self.simulator.actual_holding_volume, 1, axis=0)
        prev_holding[0] = 0  # 첫날의 이전 포지션은 0으로 설정
        
        # 매도 비용 계산
        sell_spot_volume = np.minimum(
            self.simulator.actual_sell_volume,
            prev_holding
        )
        sell_spot_volume[sell_spot_volume < 0] = 0
        sell_future_volume = self.simulator.actual_sell_volume - sell_spot_volume
        
        sell_cost = np.nansum(
            (sell_spot_volume * self.simulator.sell_price * self.simulator.sell_fee_tax) +
            (sell_future_volume * self.simulator.sell_price * self.simulator.future_fee_tax),
            axis=1
        )
        
        # 매수 비용 계산
        buy_future_volume = np.minimum(np.abs(prev_holding), self.simulator.actual_buy_volume)
        buy_spot_volume = self.simulator.actual_buy_volume - buy_future_volume
        
        buy_cost = np.nansum(
            (buy_spot_volume * self.simulator.buy_price * self.simulator.buy_fee_tax) +
            (buy_future_volume * self.simulator.buy_price * self.simulator.future_fee_tax),
            axis=1
        )
        
        total_cost = buy_cost + sell_cost
        return pd.DataFrame(
            total_cost,
            index=self.simulator.dates,
            columns=["cost"],
        )
