

# <p style="text-align:center"> E&R India 100 Factsheet </p>


#### <p style="text-align:right"> by Tiric Ciprian </p>



## Description

_Exceptional & Rich India 100 Index [E&R India 100] has been created to improve the statistical and scientific design flaws of the market capitalization methodology used in the S&P BSE 100, which is widely regarded as the best single gauge of large-cap India equities. Unlike market capitalization methodology which is risk-increasing and return-reducing owing to its concentration, the E&R is designed to own 100 large-cap Indian equities, and deliver higher risk-weighted excess returns while maintaining low tracking error vs. the S&P BSE 100._

## Methodology

_The methodology is based on a modern science innovation, which uses Reversion-Divergence framework to dynamically score, weight and rebalance components in a group to deliver higher risk-weighted excess returns. The method removes the conflict between Efficient and Inefficient market thinking, statistically normal and non-normal behavior, or in simple terms the conflict between Value and Growth investing. The methodology is not Size biased, and obviates the need for concentration and running after winners but rather adopts a slower weight readjustment compared to the S&P BSE 100.
_

```sql bigvalue
select *
from metrics_india100
limit 1
```

```sql bigvalue2
select "S&P BSE 100"
from metrics_india100
limit 1
```


<BigValue 
  data={bigvalue} 
  value='E&R India 100'
comparison="S&P BSE 100"
sparkline="E&R India 100"
  comparisonTitle='vs S&P BSE 100'/>


<BigValue 
  data={bigvalue} 
  value='S&P BSE 100'
comparison="E&R India 100"
sparkline="E&R India 100"
  comparisonTitle='vs S&P BSE 100'/>





## Sctor breakdown  
```sql sec
select "Industry Sectors" as name, "Value P" as value
from sectors_india100
```

<ECharts config={
    {
        tooltip: {
            formatter: '{b}: {d}%'
        },
      series: [
        {
          type: 'pie',
          radius: ['50%', '90%'],
          data: [...sec],
          
        }
      ]
      }
    }
    
/>


## Symbol list info

```symbols
SELECT *
FROM symbols_india100
```
<DataTable data={symbols} search=true>
<Column id=Symbol />
<Column id=Name />
<Column id="Current Price" fmt=num />
<Column id="Portfolio Proportion(%)" fmt=num2 contentType=colorscale/>
<Column id="Benchmark Proportion(%)" fmt=num2 contentType=colorscale/>
<Column id=P&L(%) contentType=delta fmt=num2 totalAgg=weightedMean weightCol=sales/> 
</DataTable>

## Performance 

```historical
select *  from historical_india100
```

<LineChart 
    data={historical} 
    x=Date  
    y=Value 
    series=Group
    yMin = 0
    yfmt = num2
/>


## Metrics

```metrics
select *  from metrics_india100
```
<DataTable data={metrics} />



## Drawdown

```drawdown
select *  from drawdown_india100
```

<LineChart 
    data={drawdown} 
    x=Date 
    y=Value 
    series=Group
    yMax = 0
/>

```drawdownp
select *  from drawdownp_india100
```
<DataTable data={drawdownp}>
    <Column id="Start date" />
    <Column id="End date" align=center/>
    <Column id="Maximum (%)" contentType=delta fmt=num2 totalAgg=weightedMean weightCol=sales/> 
    <Column id=Days align=center contentType=colorscale scaleColor=blue/>
</DataTable>


```drawdownb
select *  from drawdownb_india100
```
<DataTable data={drawdownb}>
    <Column id="Start date" />
    <Column id="End date" align=center/>
    <Column id="Maximum (%)" contentType=delta fmt=num2 totalAgg=weightedMean weightCol=sales/> 
    <Column id=Days align=center contentType=colorscale scaleColor=blue/>
</DataTable>


## Top 10 Components

```symbolsp
SELECT *
FROM symbols_india100_p
```

<BarChart 
    data={symbolsp}
    x=Symbol
    x2="Benchmark Proportion(%)"
    y="Portfolio Proportion(%)"
    y2="Name"
/>

```symbolsb
SELECT *
FROM symbols_india100_b
```

<BarChart 
    data={symbolsb}
    x=Symbol
    y="Portfolio Proportion(%)"
    y2="Benchmark Proportion(%)"
/>


<BubbleChart 
    data={symbolsp}
    y="Portfolio Proportion(%)"
    x="Benchmark Proportion(%)"
    series=Symbol
    size=Symbol
/>


<BubbleChart 
    data={symbolsb}
    y="Portfolio Proportion(%)"
    x="Benchmark Proportion(%)"
    series=Symbol
    size=Symbol
/>


### Average Rolling 2YRS
```rolling
SELECT *
FROM rolling_india100
where Years == 2
```
<BarChart 
    data={rolling}
    x=Date
    y=Value
    series=Group
    type=grouped
/>

### Average Rolling 3YRS
```rolling2
SELECT *
FROM rolling_india100
where Years == 3
```
<BarChart 
    data={rolling2}
    x=Date
    y=Value
    series=Group
    type=grouped
/>


<FunnelChart 
    data={symbolsp}
    title="Top 10 Portfolio Components" 
    nameCol=Symbol
    valueCol="Portfolio Proportion(%)"
    showPercent=true
    connectGroup= "da"
/>

<FunnelChart 
    data={symbolsb}
    title="Top 10 Benchmark Components" 
    nameCol=Symbol
    valueCol="Benchmark Proportion(%)"
    showPercent=true
    connectGroup="da"
/>

