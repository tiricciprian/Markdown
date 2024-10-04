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
con = duckdb.connect('test2.db')

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
# %%
