import numpy as np
from finter.framework_model.content import Loader
from finter.settings import logger

class FactorLoader(Loader):
    def __init__(self, cm_name):
        self.__CM_NAME = cm_name
        self.__FREQ = cm_name.split(".")[-1]
        self.gvkeyiid_factor = [
            "z_score",
            "kz_index",
            "eq_dur",
            "ival_me",
            "debt_mev", 
            'pstk_mev',
            'debtlt_mev',
            'debtst_mev',
            'be_mev',
            'at_mev',
            'cash_mev',
            'bev_mev',
            'ppen_mev',
            'gp_mev',
            'ebitda_mev',
            'ebit_mev',
            'sale_mev',
            'ocf_mev',
            'cop_mev',
            'be_me',
            'at_me',
            'cash_me',
            'gp_me',
            'ebitda_me',
            'ebit_me',
            'ope_me',
            'ni_me',
            'sale_me',
            'ocf_me',
            'nix_me',
            'cop_me',
            'rd_me',
            'div_me',
            'debt_me',
            'netdebt_me',
            'aliq_mat'
        ]

    def get_df(
        self,
        start: int,
        end: int,
        fill_nan=True,
        quantit_universe=True,
        *args,
        **kwargs
    ):
        raw = self._load_cache(
            self.__CM_NAME,
            start,
            end,
            freq=self.__FREQ,
            fill_nan=fill_nan,
            *args,
            **kwargs,
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
            factor_name = self.__CM_NAME.split("-")[-1].replace(".1d", "")
            
            if factor_name not in self.gvkeyiid_factor:
                univ.columns = [col[:6] for col in univ.columns]
                univ = univ.T.groupby(univ.columns).any().T
            else:
                logger.info(f"{factor_name} cm column is gvkeyiid")
            raw *= univ
            raw = raw.replace(0, np.nan)

        return raw
