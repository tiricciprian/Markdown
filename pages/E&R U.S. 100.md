
<img src="..static/header1.png" alt="header" width="300"/>
----

<br />
<br />

# <p style="text-align:center"> Exceptional & Rich © U.S. 500 Style Simulations </p>


#### <p style="text-align:right"> by Tiric Ciprian </p>




AlphaBlock's "open indexing" is a systematic, scientific, and replicable method, which is based on a mathematical innovation that allows for the construction of smart beta portfolios that are less concentrated, recover faster after a market fall and improve on the limitations of the current indexing methods.The Exceptional & Rich [E&R] Indices Sandbox is a codebase that executes the following three steps. First; downloads yahoo EOD [end of day] closing price data. Second; generates relative performance rankings [detailed in the codebase]. Third; creates portfolios using these rankings. The portfolios are not rebalanced and are held for 3 holding periods [1, 2, and 3 years].

The method tests the following statistical factors. Value - if ranking is equal or below 20 i.e. bottom quintile [V]. Core - if ranking is between 20 and 80 i.e. rest quintiles ignoring top and bottom quintile [C]. Growth - if ranking is equal or above 80 i.e. top quintile [G]. The following types of portfolios are generated: Value [V], Core [C], Growth[G], Value Growth i.e. top and bottom quintile [VG], All quintiles [VCG]. Based on this data the following files are created: Summary Table, Index Drawdown, Index Draw DownCurve plot, and Daily Return. If the input type is All (VCG) the code will generate an unequal weighted portfolio with value and growth having 40% each and core only 20%.

The 60 components of the ADR are screened for fundamental quality based on six parameters viz. sales growth, leverage, net profitability, free float, earnings growth and operating profitability. VCG group had the lowest average tracking error, the highest average information ratio and was the best Cartesian category that looked across various MPT statistics.

Though the behaviour of the 3N methodology is consistent across different regions and assets, the behaviour of respective styles (V, C, G, VG, VCG) may vary based on other factors like number of components, starting point of the simulation, macro economic conditions, fundamental factors etc. We use A.I. to monitor and anticipate these variations to enhance our strategy.



## Average annualized excess returns histograms for various factors  
```sql avg
select *
from full_averages
```

<BarChart 
    data={avg}
    y="Annualized Excess Return %"
    x="Statistical Factors" 
    series="Statistical Factors" 
/>


```sql avg_years
select *
from averages_years
```

<BarChart 
    data={avg_years}
    y="Annualized Excess Return %"
    series="Statistical Factors" 
    x="Holding Yrs"
    type=grouped
/>

```sql avg_rank
select *
from averages_rank
```

<BarChart 
    data={avg_rank}
    y="Annualized Excess Return %"
    series="Statistical Factors" 
    x="Rank"
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
    series="Statistical Factors"
/>

<AreaChart 
    data={full_data}
    y="Annualized Excess Return %"
    x="Statistical Factors"
    
/>