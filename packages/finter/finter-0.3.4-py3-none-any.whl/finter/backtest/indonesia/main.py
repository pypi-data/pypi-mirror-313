import numpy as np
from numba import njit

from finter.backtest.base import BaseBacktestor
from finter.backtest.core import (
    calculate_buy_sell_volumes,
    execute_transactions,
    update_nav,
    update_valuation_and_cash,
)

# Todo
# - volcap
# - buy & hold frequency


class IndonesiaBacktestor(BaseBacktestor):
    def run(self, auto_rebalance=True, debug=False):
        for i in range(1, self.num_days):
            # Todo: use base price
            self.target_volume[i] = update_target_volume(
                self.weight[i],
                self.nav[i - 1, 0],
                self.price[i - 1],
                self.weight[i - 1],
                self.target_volume[i - 1],
                auto_rebalance,
                i == 1,
            )

            (
                self.target_buy_volume[i],
                self.target_sell_volume[i],
                self.actual_sell_volume[i],
            ) = calculate_buy_sell_volumes(
                self.target_volume[i],
                self.actual_holding_volume[i - 1],
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
            )

            (self.actual_holding_volume[i], self.valuation[i], self.cash[i, 0]) = (
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
