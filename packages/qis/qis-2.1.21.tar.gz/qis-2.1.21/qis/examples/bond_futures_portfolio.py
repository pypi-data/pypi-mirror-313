import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
import qis as qis

import quant_strats.local_path as lp

output_path = lp.OUTPUT_PATH
local_path = lp.LOCAL_PATH
# quant_strats
from quant_strats import (compute_strategy_portfolio_data_with_costs,
                          compute_multi_strategy_data_from_blocks,
                          compute_marginal_perfs_for_strategy)
from quant_strats.data.universes.futures.bbg_futures import Universes
from quant_strats.data.set.assets_bbg import AssetsBBG
from quant_strats.research_strategies.futures.cross_trend.csft_strategies import (CSTF_RB_TRACKER,
                                                                                  CSTF_EXACT_TRACKER,
                                                                                  CSTF_RB_AC_TRACKER)
from quant_strats.research_strategies.futures.trackers.run_trackers_backtest import (CSTF_GOLDMAN_TRACKER_AC,
                                                                                     GOLDMAN_UNIVERSE)

strategy_universe = Universes.BBG_FUTURES_INVESTABLE.load_universe_data(local_path=local_path)
prices = strategy_universe.get_prices(freq='B')[['UXY1 Comdty', 'US1 Comdty', 'WN1 Comdty']].ffill().dropna()
prices = prices[prices.columns[::-1]]
qis.plot_prices_with_dd(prices=prices)

portfolio_data = qis.backtest_model_portfolio(prices=prices,
                                              weights=np.array([-1.0, 2.0, -1.0]),
                                              rebalance_freq='ME',
                                              ticker='Butterly'
                                              )

time_period = qis.TimePeriod('31Dec2015', None)
figs = qis.generate_strategy_factsheet(portfolio_data=portfolio_data,
                                       benchmark_prices=prices.iloc[:, -1],
                                       is_grouped=False,
                                       add_current_position_var_risk_sheet=False,
                                       add_weights_turnover_sheet=False,
                                       add_grouped_exposures=False,
                                       add_grouped_cum_pnl=False,
                                       time_period=time_period,
                                       **qis.fetch_default_report_kwargs(time_period=time_period,
                                                                         add_rates_data=False))

qis.save_figs_to_pdf(figs=figs, file_name=f"butterfly", orientation='landscape',
                     local_path=output_path)

plt.show()