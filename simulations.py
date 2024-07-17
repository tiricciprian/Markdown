# %%
import pandas as pd
import glob
import time
import duckdb
# %%
con = duckdb.connect('test1.db')

# %%
full_averages = pd.read_csv('./simulations_data/full_averages.csv')
averages_years = pd.read_csv('./simulations_data/averages_years.csv')
averages_rank = pd.read_csv('./simulations_data/averages_rank.csv')
full_data = pd.read_csv('./simulations_data/full_data.csv')



# %%
con.sql("CREATE TABLE full_averages AS FROM full_averages")
con.sql("CREATE TABLE averages_years AS FROM averages_years")
con.sql("CREATE TABLE averages_rank AS FROM averages_rank")
con.sql("CREATE TABLE full_data AS FROM full_data")
# %%
con.close()

# %%
