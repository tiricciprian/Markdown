# %%
import pandas as pd
import glob
import time
import duckdb
# %%
con = duckdb.connect('test1.db')

# %%
rolling_df = pd.read_csv('./india100/rolling.csv')

# %%
rolling_df['Date'] = pd.to_datetime(rolling_df['Date'], format='%Y')



# %%
symbols_df = pd.read_csv('./india100/symbols-data.csv')

#%%
#%%
symbols_df.Symbol = symbols_df.Symbol.astype(str)
#%%
symbols_p = symbols_df.sort_values(symbols_df.columns[4],ascending=False)[:10]
symbols_b = symbols_df.sort_values(symbols_df.columns[5],ascending=False)[:10]

#%%
con.sql("CREATE TABLE rolling_india100 AS FROM rolling_df")


# %%
con.sql("CREATE TABLE symbols_india100 AS FROM symbols_df")
con.sql("CREATE TABLE symbols_india100_p AS FROM symbols_p")
con.sql("CREATE TABLE symbols_india100_b AS FROM symbols_b")
con.sql("CREATE TABLE drawdownp_india100 AS FROM read_csv_auto('./india100/drawdown-p.csv')")
con.sql("CREATE TABLE drawdownb_india100 AS FROM read_csv_auto('./india100/drawdown-b.csv')")
con.sql("CREATE TABLE historical_india100 AS FROM read_csv_auto('./india100/historical.csv')")
con.sql("CREATE TABLE drawdown_india100 AS FROM read_csv_auto('./india100/drawdown.csv')")
con.sql("CREATE TABLE sectors_india100 AS FROM read_csv_auto('./india100/sector-portfolio.csv')")
con.sql("CREATE TABLE metrics_india100 AS FROM read_csv_auto('./india100/metrics.csv')")


# %%
con.sql("CREATE TABLE rolling_us100 AS FROM read_csv_auto('./us100/rolling.csv')")
con.sql("CREATE TABLE drawdownp_us100 AS FROM read_csv_auto('./us100/drawdown-p.csv')")
con.sql("CREATE TABLE drawdownb_us100 AS FROM read_csv_auto('./us100/drawdown-b.csv')")
con.sql("CREATE TABLE historical_us100 AS FROM read_csv_auto('./us100/historical.csv')")
con.sql("CREATE TABLE drawdown_us100 AS FROM read_csv_auto('./us100/drawdown.csv')")
con.sql("CREATE TABLE symbols_us100 AS FROM read_csv_auto('./us100/symbols-data.csv')")
con.sql("CREATE TABLE sectors_us100 AS FROM read_csv_auto('./us100/sector-portfolio.csv')")
con.sql("CREATE TABLE metrics_us100 AS FROM read_csv_auto('./us100/metrics.csv')")


# %%
con.table('rolling_india100').show()
#%%
con.table('sectors_india100').show()
#%%
con.table('DROP TABLE rolling')


# %%
con.close()

# %%
