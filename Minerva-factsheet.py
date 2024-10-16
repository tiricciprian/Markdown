# %%
import pandas as pd
import glob
import time
import duckdb
import numpy as np
from statistics import mean


# %% FUNCTIONS
def calculate_annualized_return_for_rolling(start,end,column,df):

    first_value =df.iloc[start:end,column]
    last_value  =df.iloc[end,column]
    AR = (((last_value/first_value)**(12/12))-1)*100
    return round(AR,2)


def calculate_annualized_return_each_year(df,year):

    first_value =df[df['Date'].dt.year == year].iloc[0,2]
    last_value  =df[df['Date'].dt.year == year].iloc[-1,2]
    AR = (((last_value/first_value)**(12/len(df[df['Date'].dt.year == year])))-1)*100
    return round(AR,2)

def index_data(df):
    p=100/df.iloc[0,2:]
    df.iloc[:,2:]*=p
    return df

def calculate_annualized_return(nr_of_months,group):

    first_value =df[df['Group']==group].iloc[0,2]
    last_value  =df[df['Group']==group].iloc[nr_of_months,2]
    AR = (((last_value/first_value)**(12/nr_of_months))-1)*100
    return round(AR,2)

def calculate_return_full_year(df,year):
    first_value =df[df['Date'].dt.year == year-1].iloc[-1,2]
    last_value  =df[df['Date'].dt.year == year].iloc[-1,2]
    AR = ((last_value/first_value)-1)*100
    return round(AR,2)

def calculate_return_first_year(df,year):
    first_value =df[df['Date'].dt.year == year].iloc[0,2]
    last_value  =df[df['Date'].dt.year == year].iloc[-1,2]
    AR = ((last_value/first_value)-1)*100
    return round(AR,2)

def annualized_return_binge(df,value):
    list1 = []
    list1.append(100+df.iloc[0,2])
    for i in range(1, len(df)):
        list1.append(round(list1[i-1]*(1+df.iloc[i,2]/100),2))

    return_value = (list1[-1]/100-1)*100
    annualized_return_value = round(((list1[-1]/100)**(1/value)-1)*100,2)
    
    return annualized_return_value

def calculate_drawdown(df):
    df['Peak'] = df['Portfolio Return'].cummax()
    df['Drawdown'] = (df['Portfolio Return'] - df['Peak']) / df['Peak']
    return df

# %% CLEAN AND MANIPULATE DATA
groupname = 'Minerva-factsheet'
df = pd.read_csv('./minerva/Minerva-Monthly-12yrs.csv')
groups=df['Group'].unique()

periods=['1 Year', '2 Years', '3 Years', '5 Years', '10 Years','12 Years']
nr_months = [12,24,36,60,120,144]


df['Date'] =  pd.to_datetime(df['Date'])
df1 = df[df['Group']==groups[0]]

df2 = index_data(df1[df1['Date']>='1/1/2012'])
df3 = index_data(df1[df1['Date']>='1/1/2016'])
df4 = index_data(df1[df1['Date']>='1/1/2020'])
df5 = index_data(df1[df1['Date']>='1/1/2024'])

df6 = df[df['Group']==groups[2]]

df7 = index_data(df6[df6['Date']>='1/1/2012'])
df8 = index_data(df6[df6['Date']>='1/1/2016'])
df9 = index_data(df6[df6['Date']>='1/1/2020'])
df10 = index_data(df6[df6['Date']>='1/1/2024'])

portfolio_values = list(df1['Indexed Value'])
monthly_returns = [(portfolio_values[i+1] / portfolio_values[i]) - 1 for i in range(len(portfolio_values)-1)]
monthly_std_dev = np.std(monthly_returns)
annualized_std1 = round((monthly_std_dev * np.sqrt(12))*100,2)

benchmark_values = list(df6['Indexed Value'])
monthly_returns = [(benchmark_values[i+1] / benchmark_values[i]) - 1 for i in range(len(benchmark_values)-1)]
monthly_std_dev = np.std(monthly_returns)
annualized_std2 = round((monthly_std_dev * np.sqrt(12))*100,2)

df1['Returns'] = df1['Indexed Value'].pct_change()
df6['Returns'] = df6['Indexed Value'].pct_change()

df1 = df1.reset_index(drop=True)
df6 = df6.reset_index(drop=True)

tracking_errors = df1['Returns'] - df6['Returns']
avg_tracking_error = round(tracking_errors.abs().mean()*100,2)

active_risk = tracking_errors.std()
information_ratio = round(tracking_errors.mean() / active_risk,2)

if (groupname=='Minerva-factsheet'):
    text1 = '2012'
    index1 = 2012
else:
    text1 = '2014'
    index1 = 2014
column_names1 = ['Nr./Name',groups[0],groups[2]]
df_metrics=pd.DataFrame(columns = column_names1)
df_metrics = df_metrics._append({'Nr./Name':'Performance (%) since January '+text1,groups[0]:round(df2.iloc[-1,2]-100,2),groups[2]:round(df7.iloc[-1,2]-100,2)},ignore_index = True)
df_metrics = df_metrics._append({'Nr./Name':'Performance (%) since January 2016',groups[0]:round(df3.iloc[-1,2]-100,2),groups[2]:round(df8.iloc[-1,2]-100,2)},ignore_index = True)
df_metrics = df_metrics._append({'Nr./Name':'Performance (%) since January 2020',groups[0]:round(df4.iloc[-1,2]-100,2),groups[2]:round(df9.iloc[-1,2]-100,2)},ignore_index = True)
df_metrics = df_metrics._append({'Nr./Name':'Performance (%) since January 2024',groups[0]:round(df5.iloc[-1,2]-100,2),groups[2]:round(df10.iloc[-1,2]-100,2)},ignore_index = True)
df_metrics = df_metrics._append({'Nr./Name':'Current Portfolio Value (Invested in March '+text1+')',groups[0]:round(df1.iloc[-1,2],2),groups[2]:round(df6.iloc[-1,2],2)},ignore_index = True)
df_metrics = df_metrics._append({'Nr./Name':'Annualized (%) Return (Since March '+text1+')',groups[0]:calculate_annualized_return(len(df1)-1,groups[0]),groups[2]:calculate_annualized_return(len(df1)-1,groups[2])},ignore_index = True)
df_metrics = df_metrics._append({'Nr./Name':'Annualized Std. Deviation (%)',groups[0]:annualized_std1,groups[2]:annualized_std2},ignore_index = True)
df_metrics = df_metrics._append({'Nr./Name':'Average Tracking Error (%)',groups[0]:avg_tracking_error,groups[2]:'-'},ignore_index = True)
df_metrics = df_metrics._append({'Nr./Name':'Average Information Ratio (%)',groups[0]:information_ratio,groups[2]:'-'},ignore_index = True)

df_metrics.to_csv("./minerva/factsheet_data/metrics.csv",index=False)


##### BINGE Years

column_names = ['Group','Period','Return %']
df3=pd.DataFrame(columns = column_names)

for group in groups:
    df3= df3._append({'Group':group,'Period':str(index1-1),'Return %':calculate_return_first_year(df[df['Group']==group],index1-1)},ignore_index = True)

for group in groups:
    for i in range (index1,2025):
        df3= df3._append({'Group':group,'Period':str(i),'Return %':calculate_return_full_year(df[df['Group']==group],i)},ignore_index = True)

column_names = ['Group','Annualized Return %']
df3_averages=pd.DataFrame(columns = column_names)
for group in groups:
    df3_averages=df3_averages._append({'Group':group, 'Annualized Return %':annualized_return_binge(df3[df3['Group']==group],12.98)},ignore_index=True)

df3_binge = df3[(df3.Period!='2014')&(df3.Period!='2017')&(df3.Period!='2021')&(df3.Period!='2023')]
column_names = ['Group','Annualized Return %']
df4_averages=pd.DataFrame(columns = column_names)
for group in groups:
    df4_averages=df4_averages._append({'Group':group, 'Annualized Return %':annualized_return_binge(df3_binge[df3_binge['Group']==group],8.98)},ignore_index=True)

df3_averages.to_csv("./minerva/factsheet_data/binge1.csv",index=False)
df4_averages.to_csv("./minerva/factsheet_data/binge2.csv",index=False)


##### BINGE table

df4_averages.rename(columns = {'Annualized Return %':'Annualized Return % Adjusted'}, inplace = True)
df3_averages['Annualized Return % Adjusted']= df4_averages['Annualized Return % Adjusted']
df3_averages.rename(columns = {'Group':'Nr./Group'}, inplace = True)

df3_averages.to_csv("./minerva/factsheet_data/binge_table.csv",index=False)

##### Performance

df.rename(columns = {'Indexed Value':'Portfolio Return'}, inplace = True)
df['Date'] =  pd.to_datetime(df['Date'])
source = df
source.to_csv("./minerva/factsheet_data/performance.csv",index=False)

##### 12Yrs

column_names = ['Group','Period','Annualized Return %']
df2=pd.DataFrame(columns = column_names)
for group in groups:
    for i in range (0,len(periods)):
        df2 = df2._append({'Group':group,'Period':periods[i],'Annualized Return %':calculate_annualized_return(nr_months[i],group)},ignore_index = True)

df2.to_csv("./minerva/factsheet_data/12yrs.csv",index=False)

##### Drawdown

df0 = df[df['Group']==groups[0]]
df0['Peak'] = df0['Portfolio Return'].cummax()
df0['Drawdown'] = (df0['Portfolio Return'] - df0['Peak']) / df0['Peak']

df1 = df[df['Group']==groups[1]]
df1['Peak'] = df1['Portfolio Return'].cummax()
df1['Drawdown'] = (df1['Portfolio Return'] - df1['Peak']) / df1['Peak']

df2 = df[df['Group']==groups[2]]
df2['Peak'] = df2['Portfolio Return'].cummax()
df2['Drawdown'] = (df2['Portfolio Return'] - df2['Peak']) / df2['Peak']

df3 = df[df['Group']==groups[3]]
df3['Peak'] = df3['Portfolio Return'].cummax()
df3['Drawdown'] = (df3['Portfolio Return'] - df3['Peak']) / df3['Peak']

df4 = df[df['Group']==groups[4]]
df4['Peak'] = df4['Portfolio Return'].cummax()
df4['Drawdown'] = (df4['Portfolio Return'] - df4['Peak']) / df4['Peak']

df5 = pd.concat([df0,df1, df2,df3,df4], axis=0)
df5.to_csv("./minerva/factsheet_data/drawdown.csv",index=False)

#### Rolling 2-3 years

df_roll1 = df[df['Group']==groups[0]]
df_roll2 = df[df['Group']==groups[2]]

df_roll1['2-Year Returns'] = df_roll1['Portfolio Return'].pct_change(24) * 100
df_roll1['3-Year Returns'] = df_roll1['Portfolio Return'].pct_change(36) * 100

df_roll2['2-Year Returns'] = df_roll2['Portfolio Return'].pct_change(24) * 100
df_roll2['3-Year Returns'] = df_roll2['Portfolio Return'].pct_change(36) * 100

df_roll = pd.concat([df_roll1,df_roll2],axis=0)

column_names = ['Group','Period','Annualized Return %','Years']
df_roll1_avg=pd.DataFrame(columns = column_names)
for i in range (2013,2025):
    df_roll1_avg=df_roll1_avg._append({'Group':groups[0],'Period':str(i),'Annualized Return %':df_roll1[df_roll1['Date'].dt.year == i].iloc[:,3].mean(),'Years':str(2)},ignore_index = True)
    df_roll1_avg=df_roll1_avg._append({'Group':groups[0],'Period':str(i),'Annualized Return %':df_roll1[df_roll1['Date'].dt.year == i].iloc[:,4].mean(),'Years':str(3)},ignore_index = True)

column_names = ['Group','Period','Annualized Return %','Years']
df_roll2_avg=pd.DataFrame(columns = column_names)
for i in range (2013,2025):
    df_roll2_avg=df_roll2_avg._append({'Group':groups[2],'Period':str(i),'Annualized Return %':df_roll2[df_roll2['Date'].dt.year == i].iloc[:,3].mean(),'Years':str(2)},ignore_index = True)
    df_roll2_avg=df_roll2_avg._append({'Group':groups[2],'Period':str(i),'Annualized Return %':df_roll2[df_roll2['Date'].dt.year == i].iloc[:,4].mean(),'Years':str(3)},ignore_index = True)

source = pd.concat([df_roll1_avg[df_roll1_avg['Years']=='2'],df_roll2_avg[df_roll2_avg['Years']=='2']],axis=0)
source=source.dropna()
source.to_csv("./minerva/factsheet_data/rolling1.csv",index=False)

source = pd.concat([df_roll1_avg[df_roll1_avg['Years']=='3'],df_roll2_avg[df_roll2_avg['Years']=='3']],axis=0)
source=source.dropna()
source.to_csv("./minerva/factsheet_data/rolling2.csv",index=False)

df1 = df[df['Group']==groups[0]]
df2 = df[df['Group']==groups[1]]
df3 = df[df['Group']==groups[2]]
df4 = df[df['Group']==groups[3]]
df5 = df[df['Group']==groups[4]]


if (groupname=='Minerva-factsheet'):
    start_dates = ['2012-01-01','2014-01-01','2016-01-01','2018-01-01','2020-01-01','2021-01-01','2022-01-01','2023-01-01']
    
else:    
    start_dates = ['2014-01-01','2016-01-01','2018-01-01','2019-01-01','2020-01-01','2021-01-01','2022-01-01','2023-01-01']

for i in range (0,len(start_dates)-1,2):
    source1 = pd.concat([index_data(df1[df1['Date']>=start_dates[i]]),index_data(df2[df2['Date']>=start_dates[i]]),
              index_data(df3[df3['Date']>=start_dates[i]]),index_data(df4[df4['Date']>=start_dates[i]]),
              index_data(df5[df5['Date']>=start_dates[i]])],axis=0)
    source1.to_csv("./minerva/factsheet_data/startdate"+str(i)+".csv",index=False)

    source2 = pd.concat([index_data(df1[df1['Date']>=start_dates[i+1]]),index_data(df2[df2['Date']>=start_dates[i+1]]),
              index_data(df3[df3['Date']>=start_dates[i+1]]),index_data(df4[df4['Date']>=start_dates[i+1]]),
              index_data(df5[df5['Date']>=start_dates[i+1]])],axis=0)
    source2.to_csv("./minerva/factsheet_data/startdate"+str(i+1)+".csv",index=False)

symbols_df = pd.read_csv('./minerva/symbols-data.csv')

symbols_df.Symbol = symbols_df.Symbol.astype(str)
symbols_p = symbols_df.sort_values(symbols_df.columns[2],ascending=False)[:10]
symbols_b = symbols_df.sort_values(symbols_df.columns[3],ascending=False)[:10]


################## Connect and populate database ############################

# %%
con = duckdb.connect('test2.db')

con.sql("CREATE TABLE symbols_p AS FROM symbols_p")
con.sql("CREATE TABLE symbols_b AS FROM symbols_b")
con.sql("CREATE TABLE sectors_minerva AS FROM read_csv_auto('./minerva/factsheet_data/sector-portfolio.csv')")
con.sql("CREATE TABLE performance AS FROM read_csv_auto('./minerva/factsheet_data/performance.csv')")
con.sql("CREATE TABLE yrs12 AS FROM read_csv_auto('./minerva/factsheet_data/12yrs.csv')")
con.sql("CREATE TABLE drawdown AS FROM read_csv_auto('./minerva/factsheet_data/drawdown.csv')")
con.sql("CREATE TABLE metrics AS FROM read_csv_auto('./minerva/factsheet_data/metrics.csv')")
con.sql("CREATE TABLE binge1 AS FROM read_csv_auto('./minerva/factsheet_data/binge1.csv')")
con.sql("CREATE TABLE binge2 AS FROM read_csv_auto('./minerva/factsheet_data/binge2.csv')")
con.sql("CREATE TABLE startdate0 AS FROM read_csv_auto('./minerva/factsheet_data/startdate0.csv')")
con.sql("CREATE TABLE startdate1 AS FROM read_csv_auto('./minerva/factsheet_data/startdate1.csv')")
con.sql("CREATE TABLE startdate2 AS FROM read_csv_auto('./minerva/factsheet_data/startdate2.csv')")
con.sql("CREATE TABLE startdate3 AS FROM read_csv_auto('./minerva/factsheet_data/startdate3.csv')")
con.sql("CREATE TABLE startdate4 AS FROM read_csv_auto('./minerva/factsheet_data/startdate4.csv')")
con.sql("CREATE TABLE startdate5 AS FROM read_csv_auto('./minerva/factsheet_data/startdate5.csv')")
con.sql("CREATE TABLE startdate6 AS FROM read_csv_auto('./minerva/factsheet_data/startdate6.csv')")
con.sql("CREATE TABLE startdate7 AS FROM read_csv_auto('./minerva/factsheet_data/startdate7.csv')")

#%%
con.close()

#%%
con = duckdb.connect('test1.db')

# %%
full_averages = pd.read_csv('./minerva/simulations_data/full_averages.csv')
averages_df = pd.read_csv('./minerva/simulations_data/averages_df.csv')
full_data = pd.read_csv('./minerva/simulations_data/full_data.csv')
averages_table = pd.read_csv('./minerva/simulations_data/averages_table.csv')

# %%
con.sql("CREATE TABLE full_averages AS FROM full_averages")
con.sql("CREATE TABLE averages_df AS FROM averages_df")
con.sql("CREATE TABLE full_data AS FROM full_data")
con.sql("CREATE TABLE avg_table AS FROM averages_table")
# %%
con.close()

######################## RISK DATA PREPROCESSING ####################

# %%
import pandas as pd

# Load your CSV file
data = pd.read_csv('./minerva/Minerva-Monthly-12yrs.csv')

# Filter data for 'India Under-served' as the portfolio and 'S&P BSE 500' as the benchmark
portfolio_data = data[data['Group'] == 'India Under-served'].copy()
benchmark_data = data[data['Group'] == 'S&P BSE 500'].copy()

# Ensure that Date columns are in datetime format for both datasets
portfolio_data['Date'] = pd.to_datetime(portfolio_data['Date'], format='%m/%d/%Y')
benchmark_data['Date'] = pd.to_datetime(benchmark_data['Date'], format='%m/%d/%Y')

# Merge both dataframes on 'Date' to align the portfolio and benchmark data
merged_data = pd.merge(portfolio_data[['Date', 'Indexed Value']], benchmark_data[['Date', 'Indexed Value']], on='Date', suffixes=('_portfolio', '_benchmark'))

# Calculate monthly returns for both portfolio and benchmark
merged_data['Portfolio_Returns'] = merged_data['Indexed Value_portfolio'].pct_change()
merged_data['Benchmark_Returns'] = merged_data['Indexed Value_benchmark'].pct_change()

# Drop the first row as it will contain NaN values due to percentage change calculation
merged_data.dropna(inplace=True)

# Set a small threshold to avoid division by near-zero downside deviations
downside_deviation_threshold = 0.005  # Small positive number

# Define a function to calculate rolling beta, information ratio, tracking error, Sharpe ratio, and Sortino ratio
def calculate_rolling_stats_with_threshold(data, window, rolling_period):
    # Rolling standard deviation for portfolio returns
    rolling_std_portfolio = data['Portfolio_Returns'].rolling(window=window).std()

    # Rolling standard deviation for benchmark returns
    rolling_std_benchmark = data['Benchmark_Returns'].rolling(window=window).std()

    # Rolling covariance between portfolio and benchmark
    rolling_cov = data['Portfolio_Returns'].rolling(window=window).cov(data['Benchmark_Returns'])

    # Rolling variance for benchmark returns
    rolling_var_benchmark = data['Benchmark_Returns'].rolling(window=window).var()

    # Rolling Sharpe Ratio (mean return / standard deviation)
    rolling_sharpe = data['Portfolio_Returns'].rolling(window=window).mean() / rolling_std_portfolio

    # Rolling Sortino Ratio (mean return / downside risk)
    downside_returns = data['Portfolio_Returns'].copy()
    downside_returns[downside_returns > 0] = 0  # Only consider negative returns
    rolling_downside_std = downside_returns.rolling(window=window).std()

    # Apply threshold to downside deviation
    rolling_downside_std = rolling_downside_std.apply(lambda x: max(x, downside_deviation_threshold))

    rolling_sortino = data['Portfolio_Returns'].rolling(window=window).mean() / rolling_downside_std

    # Rolling Tracking Error (standard deviation of the difference between portfolio and benchmark returns)
    rolling_tracking_error = (data['Portfolio_Returns'] - data['Benchmark_Returns']).rolling(window=window).std()

    # Rolling Information Ratio (excess return / tracking error)
    rolling_excess_return = data['Portfolio_Returns'].rolling(window=window).mean() - data['Benchmark_Returns'].rolling(window=window).mean()
    rolling_information_ratio = rolling_excess_return / rolling_tracking_error

    # Rolling Beta (covariance / variance of benchmark)
    rolling_beta = rolling_cov / rolling_var_benchmark

    return pd.DataFrame({
        'Date': data['Date'],
        'Rolling_Period': rolling_period,
        'Rolling_Sharpe': rolling_sharpe,
        'Rolling_Sortino': rolling_sortino,
        'Rolling_Tracking_Error': rolling_tracking_error,
        'Rolling_Information_Ratio': rolling_information_ratio,
        'Rolling_Beta': rolling_beta
    })

# Calculate rolling statistics for 12, 24, and 36 months and concatenate results
rolling_12_months = calculate_rolling_stats_with_threshold(merged_data, 12, '12 Months')
rolling_24_months = calculate_rolling_stats_with_threshold(merged_data, 24, '24 Months')
rolling_36_months = calculate_rolling_stats_with_threshold(merged_data, 36, '36 Months')

# Concatenate results for all rolling periods
combined_results = pd.concat([rolling_12_months, rolling_24_months, rolling_36_months]).dropna()

# Separate data frames for each statistic
sharpe_df = combined_results[['Date', 'Rolling_Period', 'Rolling_Sharpe']].rename(columns={'Rolling_Sharpe': 'Value'})
sortino_df = combined_results[['Date', 'Rolling_Period', 'Rolling_Sortino']].rename(columns={'Rolling_Sortino': 'Value'})
tracking_error_df = combined_results[['Date', 'Rolling_Period', 'Rolling_Tracking_Error']].rename(columns={'Rolling_Tracking_Error': 'Value'})
information_ratio_df = combined_results[['Date', 'Rolling_Period', 'Rolling_Information_Ratio']].rename(columns={'Rolling_Information_Ratio': 'Value'})
beta_df = combined_results[['Date', 'Rolling_Period', 'Rolling_Beta']].rename(columns={'Rolling_Beta': 'Value'})


# Drop NaNs and display the first valid rows for each rolling window, keeping the date
rolling_12_months_valid = rolling_12_months.dropna()
rolling_24_months_valid = rolling_24_months.dropna()
rolling_36_months_valid = rolling_36_months.dropna()

# %%
con = duckdb.connect('test2.db')

# %%
con.sql("CREATE TABLE rolling12 AS FROM rolling_12_months_valid")
con.sql("CREATE TABLE rolling24 AS FROM rolling_24_months_valid")
con.sql("CREATE TABLE rolling36 AS FROM rolling_36_months_valid")
# %%
con.close()

# %%
con = duckdb.connect('test2.db')

# %%
con.sql("CREATE TABLE sharpe AS FROM sharpe_df")
con.sql("CREATE TABLE sortino_with_threshold AS FROM sortino_df")
con.sql("CREATE TABLE information_ratio AS FROM information_ratio_df")
con.sql("CREATE TABLE tracking_error AS FROM tracking_error_df")
con.sql("CREATE TABLE beta AS FROM beta_df")

# %%
con.close()



################# FIND HIGH SORTINO #############
# %%
# Find the row with the high Sortino ratio
high_sortino = sortino_df[sortino_df['Value'] > 15]
print("High Sortino Ratio found:")
print(high_sortino)

# Investigate the portfolio returns and downside deviation for the specific date
date_of_high_sortino = high_sortino.iloc[0]['Date']

# Get portfolio returns and downside deviations leading up to that date
lookback_window = 12  # Assuming 12 months rolling period for the high Sortino ratio
relevant_data = merged_data[merged_data['Date'] <= date_of_high_sortino].tail(lookback_window)

# Calculate downside deviation manually for this period
downside_returns = relevant_data['Portfolio_Returns'].copy()
downside_returns[downside_returns > 0] = 0  # Only consider negative returns
downside_deviation = downside_returns.std()

print(f"Downside deviation for the period ending {date_of_high_sortino}: {downside_deviation}")
print("Relevant portfolio returns:")
print(relevant_data[['Date', 'Portfolio_Returns']])
# %%
