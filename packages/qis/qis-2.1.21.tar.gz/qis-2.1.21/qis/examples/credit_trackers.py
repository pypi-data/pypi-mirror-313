
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import qis as qis
from bbg_fetch import fetch_field_timeseries_per_tickers


tickers = {'CICMCE5B Index': 'ITRAXX Main 5Y',
           'CICMCE1B Index': 'ITRAXX Main 10Y',
           'CICMCX5B Index': 'ITRAXX Xover 5Y',
           'CICMCI5B Index': 'CDX NA IG 5Y',
           'CICMCI1B Index': 'CDX NA IG 10Y',
           'CICMCH5B Index': 'CDX NA HY 5Y',
           'CICMCG05 Index': 'UK CDS 5Y',
           'CICMCK05 Index': 'South Korea CDS 5Y',
           'CICMCJ05 Index': 'Japan CDS 5Y',
           'CICMCU05 Index': 'US CDS 5Y',
           'CICMCE05 Index': 'Germany CDS 5Y'
           }

tickers = {'UISYMH5S Index': 'UBS_CDX_HY',
           'CICMCH5B Index': 'CITI_CDX_HY',
           'UISYMI5S Index': 'UBS_IG_5Y',
           'CICMCI5B Index': 'CITI_IG_5Y'}

prices = fetch_field_timeseries_per_tickers(tickers=tickers, freq='B', field='PX_LAST').ffill()
print(prices)
benchmark_prices = fetch_field_timeseries_per_tickers(tickers={'LGDRTRUU Index': 'Agg IG'}, freq='B', field='PX_LAST').ffill()

time_period = qis.TimePeriod('01Jan2008', pd.Timestamp.today())
kwargs = qis.fetch_default_report_kwargs(time_period=time_period)

fig = qis.generate_multi_asset_factsheet(prices=prices,
                                         benchmark_prices=benchmark_prices,
                                         time_period=time_period,
                                         **kwargs)
qis.save_figs_to_pdf(figs=[fig],
                     file_name=f"credit_trackers_report", orientation='landscape',
                     local_path=qis.local_path.get_output_path())
