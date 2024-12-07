import pandas as pd
from typing_extensions import Literal


def daily2period(
    data: pd.Series, period: Literal["W", "M", "Q"], keep_index=False
) -> pd.Series:
    tmp = data.index[-2:-1].append(data.index[0:-1])
    mask = data.index.to_period(period) != tmp.to_period(period)
    if keep_index:
        ffill_dates = 90
        if period == "W":
            ffill_dates = 7
        elif period == "M":
            ffill_dates = 30
        return data[mask].fillna(0).reindex(data.index).ffill(limit=ffill_dates)
    return data[mask]
