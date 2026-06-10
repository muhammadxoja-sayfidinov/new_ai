# 03 — DAX Measures (to'liq to'plam)

Barcha measure'larni **`_Measures`** nomli alohida jadvalda saqlash tavsiya etiladi
(`Home → Enter Data` → bo'sh jadval yarating, nomini `_Measures` qo'ying).

Har bir measure'ni **Modeling → New Measure** orqali qo'shing va format/birlikni sozlang.

> **MUHIM:** Jadval nomlari CSV import qilinganda kelgan asl nomlarga to'liq mos (`AdventureWorks ...`). Nomida bo'sh joy bor jadval bitta qo'shtirnoq bilan yoziladi: `'AdventureWorks Sales Data'[OrderQuantity]`. Quyidagilarni to'g'ridan-to'g'ri copy-paste qilsangiz ishlaydi.

---

## 1-guruh: Asosiy ko'rsatkichlar (Core Measures)

```dax
Total Revenue =
SUMX ( 'AdventureWorks Sales Data', 'AdventureWorks Sales Data'[OrderQuantity] * RELATED ( 'AdventureWorks Product Lookup'[ProductPrice] ) )
```

```dax
Total Cost =
SUMX ( 'AdventureWorks Sales Data', 'AdventureWorks Sales Data'[OrderQuantity] * RELATED ( 'AdventureWorks Product Lookup'[ProductCost] ) )
```

```dax
Total Profit = [Total Revenue] - [Total Cost]
```

```dax
Profit Margin = DIVIDE ( [Total Profit], [Total Revenue] )
```
*Format: Percentage.*

```dax
Quantity Sold = SUM ( 'AdventureWorks Sales Data'[OrderQuantity] )
```

```dax
Total Orders = DISTINCTCOUNT ( 'AdventureWorks Sales Data'[OrderNumber] )
```

```dax
Total Customers = DISTINCTCOUNT ( 'AdventureWorks Sales Data'[CustomerKey] )
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
Total Returns = SUM ( 'AdventureWorks Returns Data'[ReturnQuantity] )
```

```dax
Return Rate = DIVIDE ( [Total Returns], [Quantity Sold] )
```
*Format: Percentage.*

```dax
-- Qaytarilgan daromad (yo'qotilgan revenue)
Returned Revenue =
SUMX ( 'AdventureWorks Returns Data', 'AdventureWorks Returns Data'[ReturnQuantity] * RELATED ( 'AdventureWorks Product Lookup'[ProductPrice] ) )
```

---

## 3-guruh: Time Intelligence (vaqt bo'yicha tahlil)

> `AdventureWorks Calendar Lookup` jadvali "Mark as Date Table" qilingan bo'lishi shart.

```dax
Revenue YTD = TOTALYTD ( [Total Revenue], 'AdventureWorks Calendar Lookup'[Date] )
```

```dax
Revenue PY = CALCULATE ( [Total Revenue], SAMEPERIODLASTYEAR ( 'AdventureWorks Calendar Lookup'[Date] ) )
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
    DATESINPERIOD ( 'AdventureWorks Calendar Lookup'[Date], MAX ( 'AdventureWorks Calendar Lookup'[Date] ), -10, DAY )
)
```

```dax
-- Yig'iluvchi (running) jami
Revenue Running Total =
CALCULATE (
    [Total Revenue],
    FILTER (
        ALLSELECTED ( 'AdventureWorks Calendar Lookup'[Date] ),
        'AdventureWorks Calendar Lookup'[Date] <= MAX ( 'AdventureWorks Calendar Lookup'[Date] )
    )
)
```

---

## 4-guruh: Oldingi oy va Maqsadlar (Targets — KPI vizuallar uchun)

```dax
Previous Month Revenue =
CALCULATE ( [Total Revenue], PREVIOUSMONTH ( 'AdventureWorks Calendar Lookup'[Date] ) )
```

```dax
Previous Month Orders =
CALCULATE ( [Total Orders], PREVIOUSMONTH ( 'AdventureWorks Calendar Lookup'[Date] ) )
```

```dax
Previous Month Profit =
CALCULATE ( [Total Profit], PREVIOUSMONTH ( 'AdventureWorks Calendar Lookup'[Date] ) )
```

```dax
Previous Month Returns =
CALCULATE ( [Total Returns], PREVIOUSMONTH ( 'AdventureWorks Calendar Lookup'[Date] ) )
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
    HASONEVALUE ( 'AdventureWorks Product Lookup'[ProductName] ),
    RANKX ( ALL ( 'AdventureWorks Product Lookup'[ProductName] ), [Total Revenue],, DESC )
)
```

```dax
-- Mijozlarni daromad bo'yicha tartiblash
Customer Rank =
IF (
    HASONEVALUE ( 'AdventureWorks Customer Lookup'[Full Name] ),
    RANKX ( ALL ( 'AdventureWorks Customer Lookup'[Full Name] ), [Total Revenue],, DESC )
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
