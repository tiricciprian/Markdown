
# <p style="text-align:center"> Minerva India Under-served™ </p>


## <p style="text-align:center"> Performance Factsheet </p>
---

<br>


## **Description**

>Minerva India Under-served focuses on the overlooked segment of the Indian equity market, targeting shares that
are institutionally under-owned and undervalued despite clear financial records and structural transparency. The
strategy emphasizes investment in high-conviction holdings that, while free from speculative excess, are typically
neglected by institutional investors. This approach seeks to exploit market inefficiencies caused by overly broad
generalizations about this sector.
>
>The fund has been highly successful, delivering a 906% return from its inception in April 2011 through February
2024, which equates to an annualized gain of over 18.5%. During the same period, the broader Indian market
indices, including the Nifty 50, S&P BSE 500, S&P BSE MidCap, and S&P BSE Smallcap, have significantly
underperformed compared to Minerva, with returns ranging from 11.35% to 13.99% annually. Adjusting for the
fund's top four performing years, it still managed an impressive 9.96% annualized return, far outpacing the
respective indices which ranged from losses to modest gains.
>
>The performance factsheet offers a detailed view of the fund's strategy and outcomes, including sector allocation,
performance metrics over various periods, a comparison of the top 10 holdings against benchmark constituents,
and analysis of the fund's drawdowns and rolling performance. The strategic focus on mispriced idiosyncrasies
within the Indian market has clearly differentiated Minerva from typical market benchmarks and conventional
investment approaches, demonstrating the effectiveness of targeting under-served market segments.

### **Sector breakdown**
```sql sec
select *
from minerva.sec
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

### **Performance** 

```performance
select *  from minerva.performance
```

<LineChart 
    data={performance} 
    x=Date  
    y='Portfolio Return' 
    series=Group
    yMin = 0
    yfmt = num2
/>


### **Metrics**

```metrics
select *  from minerva.metrics
```
<DataTable data={metrics} />

### **Top 10 Components**

```symbolsp
SELECT *
FROM minerva.symbols_p
```

```symbolsb
SELECT *
FROM minerva.symbols_b
```

<FunnelChart 
    data={symbolsp}
    title="Top 10 Portfolio Components" 
    nameCol=Symbol
    valueCol="India Under-served Proportion(%)"
    showPercent=true
    connectGroup= "da"
/>
<FunnelChart 
    data={symbolsb}
    title="Top 10 Benchmark Components" 
    nameCol=Symbol
    valueCol="S&P BSE 500 Proportion(%)"
    showPercent=true
    connectGroup= "da"
/>

### **Average Annualized Returns**

```yrs12
SELECT *
FROM minerva.yrs12
```
<BarChart 
    data={yrs12}
    x=Period
    y='Annualized Return %'
    series=Group
    type=grouped
/>

### **Drawdown Analysis**


```drawdown
SELECT *
FROM minerva.drawdown
```

<LineChart 
    data={drawdown} 
    x=Date  
    y='Drawdown' 
    series=Group
    yfmt = num3
/>

### **Binge years**

```binge1
SELECT *
FROM minerva.binge1
```
<BarChart 
    title="Historical Annualized Returns"
    data={binge1}
    x=Group
    y='Annualized Return %'
    series=Group
/>

```binge2
SELECT *
FROM minerva.binge2
```
<BarChart
    title="Historical Annualized Returns without 2014, 2017, 2021, 2023"
    data={binge2}
    x=Group
    y='Annualized Return %'
    series=Group
/>

### **Starting Point Analysis**

```startdate0
SELECT *
FROM minerva.startdate0
```
<LineChart 
    data={startdate0}
    x=Date  
    y='Portfolio Return' 
    series=Group
    yfmt = num2
/>

```startdate1
SELECT *
FROM minerva.startdate1
```
<LineChart 
    data={startdate1}
    x=Date  
    y='Portfolio Return' 
    series=Group
    yfmt = num2
/>

```startdate2
SELECT *
FROM minerva.startdate2
```
<LineChart 
    data={startdate2}
    x=Date  
    y='Portfolio Return' 
    series=Group
    yfmt = num2
/>

```startdate3
SELECT *
FROM minerva.startdate3
```
<LineChart 
    data={startdate3}
    x=Date  
    y='Portfolio Return' 
    series=Group
    yfmt = num2
/>


```startdate4
SELECT *
FROM minerva.startdate4
```
<LineChart 
    data={startdate4}
    x=Date  
    y='Portfolio Return' 
    series=Group
    yfmt = num2
/>

```startdate5
SELECT *
FROM minerva.startdate5
```
<LineChart 
    data={startdate5}
    x=Date  
    y='Portfolio Return' 
    series=Group
    yfmt = num2
/>

```startdate6
SELECT *
FROM minerva.startdate6
```
<LineChart 
    data={startdate6}
    x=Date  
    y='Portfolio Return' 
    series=Group
    yfmt = num2
/>

```startdate7
SELECT *
FROM minerva.startdate7
```
<LineChart 
    data={startdate7}
    x=Date  
    y='Portfolio Return' 
    series=Group
    yfmt = num2
/>