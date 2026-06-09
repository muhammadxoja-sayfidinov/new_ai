# 03 — DAX Measures (to'liq to'plam)

Barcha measure'larni **`_Measures`** nomli alohida jadvalda saqlash tavsiya etiladi
(`Home → Enter Data` → bo'sh jadval yarating, nomini `_Measures` qo'ying).

Har bir measure'ni **Modeling → New Measure** orqali qo'shing va format/birlikni sozlang.

---

## 1-guruh: Asosiy ko'rsatkichlar (Core Measures)

```dax
Total Revenue =
SUMX ( Sales, Sales[OrderQuantity] * RELATED ( Products[ProductPrice] ) )
```

```dax
Total Cost =
SUMX ( Sales, Sales[OrderQuantity] * RELATED ( Products[ProductCost] ) )
```

```dax
Total Profit = [Total Revenue] - [Total Cost]
```

```dax
Profit Margin = DIVIDE ( [Total Profit], [Total Revenue] )
```
*Format: Percentage.*

```dax
Quantity Sold = SUM ( Sales[OrderQuantity] )
```

```dax
Total Orders = DISTINCTCOUNT ( Sales[OrderNumber] )
```

```dax
Total Customers = DISTINCTCOUNT ( Sales[CustomerKey] )
```

```dax
Average Order Value = DIVIDE ( [Total Revenue], [Total Orders] )
```
*Format: Currency.*

```dax
Revenue per Customer = DIVIDE ( [Total Revenue], [Total Customers] )
```

---

## 2-guruh: Qaytarishlar (Returns)

```dax
Total Returns = SUM ( Returns[ReturnQuantity] )
```

```dax
Return Rate = DIVIDE ( [Total Returns], [Quantity Sold] )
```
*Format: Percentage.*

```dax
-- Qaytarilgan daromad (yo'qotilgan revenue)
Returned Revenue =
SUMX ( Returns, Returns[ReturnQuantity] * RELATED ( Products[ProductPrice] ) )
```

---

## 3-guruh: Time Intelligence (vaqt bo'yicha tahlil)

> `Calendar` jadvali "Mark as Date Table" qilingan bo'lishi shart.

```dax
Revenue YTD = TOTALYTD ( [Total Revenue], 'Calendar'[Date] )
```

```dax
Revenue PY = CALCULATE ( [Total Revenue], SAMEPERIODLASTYEAR ( 'Calendar'[Date] ) )
```

```dax
Revenue YoY = [Total Revenue] - [Revenue PY]
```

```dax
Revenue YoY % = DIVIDE ( [Revenue YoY], [Revenue PY] )
```
*Format: Percentage.*

```dax
-- 10 kunlik harakatlanuvchi o'rtacha (rolling average)
Revenue 10-Day Rolling =
CALCULATE (
    [Total Revenue],
    DATESINPERIOD ( 'Calendar'[Date], MAX ( 'Calendar'[Date] ), -10, DAY )
)
```

```dax
-- Yig'iluvchi (running) jami
Revenue Running Total =
CALCULATE (
    [Total Revenue],
    FILTER (
        ALLSELECTED ( 'Calendar'[Date] ),
        'Calendar'[Date] <= MAX ( 'Calendar'[Date] )
    )
)
```

---

## 4-guruh: Oldingi oy va Maqsadlar (Targets — KPI vizuallar uchun)

```dax
Previous Month Revenue =
CALCULATE ( [Total Revenue], PREVIOUSMONTH ( 'Calendar'[Date] ) )
```

```dax
Previous Month Orders =
CALCULATE ( [Total Orders], PREVIOUSMONTH ( 'Calendar'[Date] ) )
```

```dax
Previous Month Profit =
CALCULATE ( [Total Profit], PREVIOUSMONTH ( 'Calendar'[Date] ) )
```

```dax
Previous Month Returns =
CALCULATE ( [Total Returns], PREVIOUSMONTH ( 'Calendar'[Date] ) )
```

```dax
-- Maqsad: o'tgan oydan 10% yuqori (KPI card "Target" sifatida)
Revenue Target = [Previous Month Revenue] * 1.1
```

```dax
Order Target = [Previous Month Orders] * 1.1
```

```dax
Profit Target = [Previous Month Profit] * 1.1
```

---

## 5-guruh: Reyting va Top N (Ranking)

```dax
-- Mahsulotlarni daromad bo'yicha tartiblash
Product Rank =
IF (
    HASONEVALUE ( Products[ProductName] ),
    RANKX ( ALL ( Products[ProductName] ), [Total Revenue],, DESC )
)
```

```dax
-- Mijozlarni daromad bo'yicha tartiblash
Customer Rank =
IF (
    HASONEVALUE ( Customers[Full Name] ),
    RANKX ( ALL ( Customers[Full Name] ), [Total Revenue],, DESC )
)
```

---

## 6-guruh: Dinamik sarlavhalar va format (Dynamic titles)

```dax
-- Vizual sarlavhasi uchun (masalan: "Top 10 Products by Revenue")
Revenue Headline =
VAR _rev = [Total Revenue]
RETURN
"Total Revenue: " &
SWITCH ( TRUE (),
    _rev >= 1e6, FORMAT ( _rev / 1e6, "$#,##0.0" ) & "M",
    _rev >= 1e3, FORMAT ( _rev / 1e3, "$#,##0.0" ) & "K",
    FORMAT ( _rev, "$#,##0" )
)
```

```dax
-- KPI rangi uchun yordamchi (target'dan oshgan/qolgan)
Revenue vs Target % = DIVIDE ( [Total Revenue] - [Revenue Target], [Revenue Target] )
```

---

## Measure'lar formatlash bo'yicha eslatma

| Measure turi | Format |
|---|---|
| Revenue, Cost, Profit, AOV | Currency `$#,##0` |
| Margin, Return Rate, YoY % | Percentage `0.0%` |
| Quantity, Orders, Customers | Whole Number `#,##0` |
| Rank | Whole Number |

Har bir measure tanlanganda **Measure tools → Format** dan to'g'rilang.
