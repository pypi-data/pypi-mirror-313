from dataclasses import dataclass
from datetime import datetime
from typing import List

import pandas as pd

from hydreservoir.columns_constant import INFLOW, OUTFLOW, TIMESERIES


@dataclass
class Dataset:
    timeseries: List[datetime]
    inflow: List[float]
    outflow: List[float]

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(
            {TIMESERIES: self.timeseries, INFLOW: self.inflow, OUTFLOW: self.outflow}
        )
        df[TIMESERIES] = pd.to_datetime(df[TIMESERIES])

        return df

    @classmethod
    def from_wb_df_to_dataset(cls, df: pd.DataFrame):
        return cls(
            timeseries=df[TIMESERIES].tolist(),
            inflow=df[INFLOW].tolist(),
            outflow=df[OUTFLOW].tolist(),
        )
