# <p style="text-align:center"> Minerva India Under-served™ </p>


## <p style="text-align:center"> Simulations </p>
---

<br>


#### **Description**


_This report simulates the fund's performance from various hypothetical starting points to provide deeper insight into its risk-adjusted performance. We employ a range of visualization techniques and metrics, including histograms, box plots, cartesian plots, distributions, and data tables for cluster and MPT (Modern Portfolio Theory) analysis._

_The fund simulations has delivered average positive annualized excess returns across the simulations. Another positive aspect was its marginally better outliers performance, as illustrated in the Information Ratio analytics. Even MPT statistics suggest a higher average Information Ratio and a relatively lower Maximum Drawdown. The only negative was the Cluster Analysis, where the fund simulations underperformed the S&P BSE Small Cap benchmark in terms of both return and risk._

<br>

## Average annualized excess returns histograms for various periods and groups  
```sql avg
select *
from full_averages
```

<BarChart 
    data={avg}
    y="Annualized Excess Return %"
    x="Group" 
    series="Group" 
/>


```sql avg_df
select *
from averages_df
```

<BarChart 
    data={avg_df}
    y="Annualized Excess Return %"
    x="Group" 
    series="Holding Yrs"
    type=grouped
/>


```sql full_data
select *
from full_data
```
## Cartesian plots for various statistical measures

<ScatterPlot 
    data={full_data}
    y="Annualized Excess Return %"
    x="Annualized Excess Volatility %"
    series="Group"
/>

<ScatterPlot 
    data={full_data}
    y="Annualized Excess Return %"
    x="Information Ratio"
    series="Group"
/>

<ScatterPlot 
    data={full_data}
    y="Information Ratio"
    x="Annualized Excess Volatility %"
    series="Group"
/>

<ScatterPlot 
    data={full_data}
    y="Alpha"
    x="Beta"
    series="Group"
/>

<ScatterPlot 
    data={full_data}
    y="Information Ratio"
    x="Tracking Error"
    series="Group"
/>

## Modern portfolio theory (MPT) statistics

```sql avg_table
select *
from avg_table
```
###### (**AR** - Annualized Excess Returns, **AV** - Annualized Excess Volatility, **TE** - Tracking Error, **IR** - Information Ratio)

<DataTable data={avg_table}>
<Column id=Group/>
<Column id='AR' contentType=colorscale scaleColor=blue/>
<Column id=AV/>
<Column id=IR fmt=num2/>
<Column id=TE/>
<Column id=Alpha fmt=num2/>
<Column id=Beta/>
</DataTable>