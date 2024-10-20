# <p style="text-align:center"> Minerva India Under-served™ </p>


## <p style="text-align:center"> Risk Metrics </p>
---

<br>


## **Description**

<br>

>The India Under-served Fund, a portfolio focused on companies serving underrepresented sectors and regions in India, is evaluated here against the S&P BSE 500, a broad benchmark of India’s leading companies. By analyzing key risk and performance metrics, we can assess how well the India Under-served Fund manages risk, delivers returns, and compares to the benchmark over different time horizons.
>
>In this analysis, we use rolling 12, 24, and 36-month windows to compute various financial metrics. These rolling windows help us understand how the fund's performance has evolved over time, allowing for a more dynamic comparison. Below are the key metrics used:

<br>


### **Sharpe Ratio**

<br>

 The Sharpe Ratio measures the excess return (above the risk-free rate) generated by the portfolio per unit of risk (volatility). It provides insight into how efficiently the fund converts risk into returns.


##### A higher Sharpe ratio indicates better risk-adjusted returns. A negative Sharpe ratio suggests underperformance relative to the risk-free rate.

<br>

```sql sharpe
select *
from minerva.sharpe
```

<LineChart
    data={sharpe}
    x="Date"
    y="Value"
    series="Rolling_Period"
    yAxisTitle='Sharpe Ratio'
    yFmt=num2
/>


### **Sortino Ratio**

<br>

##### Similar to the Sharpe Ratio, the Sortino Ratio also evaluates risk-adjusted returns but focuses only on downside risk. It measures how well the portfolio performs relative to negative volatility or downside deviation. 

##### In this analysis, a threshold of 0.005 was applied to the downside deviation (the denominator of the Sortino ratio) to prevent artificially high ratios when the downside deviation is extremely small or near zero. This adjustment ensures that the ratio reflects a more realistic risk-adjusted performance by setting a minimum level of downside risk, even in periods where few or no negative returns occur.

##### A higher Sortino ratio means the portfolio is generating better returns for the amount of negative risk (losses) incurred.

<br>

```sql sortino
select *
from minerva.sortino
```

<LineChart
    data={sortino}
    x="Date"
    y="Value"
    series="Rolling_Period"
    yAxisTitle='Sortino Ratio'
    yFmt=num2
/>


### **Information Ratio**

<br>

##### The Information Ratio measures the excess return of the portfolio over the benchmark, relative to the amount of tracking error. It tells us how much value the fund manager is adding, given the additional risk taken.

##### A higher Information Ratio indicates that the fund is outperforming the benchmark relative to the amount of risk taken in deviating from it.

<br>

```sql information_ratio
select *
from minerva.information_ratio
```

<LineChart
    data={information_ratio}
    x="Date"
    y="Value"
    series="Rolling_Period"
    yAxisTitle='Information Ratio'
    yFmt=num2
/>


### **Tracking Error**

<br>

#####  Tracking Error represents the standard deviation of the difference between the portfolio's returns and the benchmark's returns. It quantifies how closely the portfolio tracks the benchmark’s performance.

##### A lower tracking error suggests that the fund closely follows the benchmark, while a higher tracking error indicates greater deviation from the benchmark.

<br>

```sql tracking_error
select *
from minerva.tracking_error
```

<LineChart
    data={tracking_error}
    x="Date"
    y="Value"
    series="Rolling_Period"
    yAxisTitle='Tracking Error'
    yFmt=num2
/>

### **Beta**

<br>

##### Beta measures the sensitivity of the portfolio’s returns to the benchmark. It shows the degree to which the portfolio moves in relation to the benchmark.

##### A beta of 1 indicates that the portfolio moves in tandem with the benchmark. A beta above 1 means the portfolio is more volatile than the benchmark, while a beta below 1 indicates less volatility.

<br>

```sql beta
select *
from minerva.beta
```

<LineChart 
    data={beta}
    x="Date"
    y="Value"
    series="Rolling_Period"
    yAxisTitle='Beta'
    yFmt=num2
/>
