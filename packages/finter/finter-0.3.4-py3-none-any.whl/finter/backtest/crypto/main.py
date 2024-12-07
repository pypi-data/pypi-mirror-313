import numpy as np
from numba import njit

from finter.backtest.base import BaseBacktestor
from finter.backtest.core import (
    calculate_buy_sell_volumes,
    update_nav,
    update_valuation_and_cash,
    update_target_volume,
)


class CryptoBacktestor(BaseBacktestor):
    def run(self, auto_rebalance=True, debug=False):
        for i in range(1, self.num_days):
            # Todo: use base price
            self.target_volume[i] = update_target_volume(
                self.weight[i],
                self.nav[i - 1, 0],
                self.price[i - 1],
                self.weight[i - 1],
                self.target_volume[i - 1],
                auto_rebalance=auto_rebalance,
                is_first_day=i == 1,
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
def execute_transactions(
    actual_sell_volume: np.ndarray,
    buy_price: np.ndarray,
    buy_fee_tax: np.float64,
    sell_price: np.ndarray,
    sell_fee_tax: np.float64,
    prev_cash: np.float64,
    target_buy_volume: np.ndarray,
) -> tuple:
    actual_sell_amount = np.nan_to_num(
        actual_sell_volume * sell_price * (1 - sell_fee_tax)
    )
    available_buy_amount = prev_cash + actual_sell_amount.sum()
    target_buy_amount = np.nan_to_num(target_buy_volume * buy_price * (1 + buy_fee_tax))
    target_buy_amount_sum = target_buy_amount.sum()
    if target_buy_amount_sum > 0:
        available_buy_volume = np.nan_to_num(
            (target_buy_amount / target_buy_amount_sum)
            * (available_buy_amount / (buy_price * (1 + buy_fee_tax)))
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
