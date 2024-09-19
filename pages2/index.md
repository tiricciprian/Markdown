
<img src="header1.png" alt="header" width="300"/>
----

<br />
<br />

# <p style="text-align:center"> E&R ADR Factsheet </p>


#### <p style="text-align:right"> by Tiric Ciprian </p>



## Description

_Exceptional & Rich ADR 60 [E&R ADR 60] has been created to improve the statistical and scientific design flaws of the market
capitalization methodology used in the MCAP Weighted customized index of 153 ADRs. Unlike market capitalization
methodology which is risk-increasing and return-reducing owing to its concentration, the E&R is designed to own 60 ADRs,
and deliver higher risk-weighted excess returns while maintaining low tracking error vs. the MCAP Weighted 153 ADRs._

Data in this demo is from the local DuckDB file `test1.db`.


## Sctor breakdown  
```sql sec
select IndustrySectors as name, ValueP as value
from sectors
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

## Symbol,Name,Current Price,P&L(%),,

## Symbol list info

```symbols
SELECT *
FROM symbols
ORDER BY "E&R ADR 60 Proportion(%)" desc
```
<DataTable data={symbols} search=true>
<Column id=Symbol />
<Column id=Name />
<Column id="Current Price" />
<Column id="E&R ADR 60 Proportion(%)" contentType=colorscale/>
<Column id="MCAP Weighted 153 ADRs Proportion(%)" contentType=colorscale/>
<Column id=P&L(%) contentType=delta fmt=pct totalAgg=weightedMean weightCol=sales/> 
</DataTable>

## Performance 

```historical
select *  from historical
```

<LineChart 
    data={historical} 
    x=Date 
    y=Value 
    series=Group
    yMin = 90
    
/>


## Metrics

```metrics
select *  from metrics
```
<DataTable data={metrics} />



## Drawdown

```drawdown
select *  from drawdown
```

<LineChart 
    data={drawdown} 
    x=Date 
    y=Value 
    series=Group
    yMax = 0
/>

```drawdownp
select *  from drawdownp
```
<DataTable data={drawdownp} />

```drawdownb
select *  from drawdownb
```
<DataTable data={drawdownb} />


## Top 10 Components

```symbolsp
SELECT *
FROM symbols
ORDER BY "E&R ADR 60 Proportion(%)" desc
limit 10
```

<BarChart 
    data={symbolsp}
    x=Symbol
    y="E&R ADR 60 Proportion(%)"
    y2="MCAP Weighted 153 ADRs Proportion(%)"
/>

```symbolsb
SELECT *
FROM symbols
ORDER BY "MCAP Weighted 153 ADRs Proportion(%)" desc
limit 10
```

<BarChart 
    data={symbolsb}
    x=Symbol
    y2="E&R ADR 60 Proportion(%)"
    y="MCAP Weighted 153 ADRs Proportion(%)"
    colorPalette={'#488f96'}
/>

```rolling
SELECT *
FROM rolling
```
<BarChart 
    data={rolling}
    x=Date
    y=Value
    series=Group
/>
