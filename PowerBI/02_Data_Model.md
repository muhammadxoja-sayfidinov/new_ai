# 02 — Data Model (Star Schema)

Bu model **yulduz sxemasi (star schema)** asosida qurilgan: markazda fakt jadvallar (Sales, Returns), atrofida o'lcham (dimension/lookup) jadvallar.

---

## 1. Jadvallar (Tables)

### Fakt jadvallar (Fact tables)
| Jadval | Manba | Tavsif |
|---|---|---|
| **Sales** | Sales Data 2020 + 2021 + 2022 | 3 ta CSV **Append** orqali bitta jadvalga birlashtiriladi (~56,000 qator) |
| **Returns** | Returns Data | Qaytarishlar (~1,809 qator) |

### O'lcham jadvallar (Dimension / Lookup tables)
| Jadval | Kalit (Key) | Tavsif |
|---|---|---|
| **Calendar** | Date | Sana o'lchami (date dimension) |
| **Customers** | CustomerKey | Mijoz ma'lumotlari |
| **Products** | ProductKey | Mahsulotlar (narx, tannarx) |
| **Product Subcategories** | ProductSubcategoryKey | Subkategoriya |
| **Product Categories** | ProductCategoryKey | Kategoriya |
| **Territories** | SalesTerritoryKey | Hudud/davlat/qit'a |

> `Product Category Sales (Unpivot Demo).csv` modelga **kiritilmaydi** — u faqat Power Query Unpivot mashqi uchun.

---

## 2. Bog'lanishlar (Relationships)

Barchasi **One-to-Many (1:*)**, yo'nalishi **Single** (lookup → fact), filtr o'lchamdan faktga oqadi.

```
                    ┌─────────────────────┐
                    │ Product Categories  │
                    │ (ProductCategoryKey)│
                    └──────────┬──────────┘
                               │ 1
                               │ *
                    ┌──────────┴───────────┐
                    │ Product Subcategories│
                    │(ProductSubcategoryKey)│
                    └──────────┬───────────┘
                               │ 1
                               │ *
   ┌───────────┐      ┌────────┴────────┐      ┌──────────────┐
   │ Calendar  │1   * │    PRODUCTS     │ 1  * │   Returns    │
   │  (Date)   ├──────┤  (ProductKey)   ├──────┤              │
   └─────┬─────┘      └────────┬────────┘      └──────┬───────┘
         │1                    │1                     │*
         │                     │*                     │
         │*            ┌───────┴────────┐             │
         └─────────────┤     SALES      │             │
                       │                │             │
         ┌─────────────┤                │             │
         │*            └───────┬────────┘             │
   ┌─────┴──────┐              │*                ┌─────┴──────┐
   │ Customers  │1             │                 │Territories │1
   │(CustomerKey)├─────────────┘                 │(...Key)    │
   └────────────┘         (Territories 1:* Sales)└─────┬──────┘
                                                       │ 1:* Returns
```

### Bog'lanishlar ro'yxati

| # | Dan (1 tomon) | Ga (* tomon) | Maydon | Faollik |
|---|---|---|---|---|
| 1 | Calendar[Date] | Sales[OrderDate] | Date / OrderDate | **Active** |
| 2 | Calendar[Date] | Returns[ReturnDate] | Date / ReturnDate | Active |
| 3 | Customers[CustomerKey] | Sales[CustomerKey] | CustomerKey | Active |
| 4 | Products[ProductKey] | Sales[ProductKey] | ProductKey | Active |
| 5 | Products[ProductKey] | Returns[ProductKey] | ProductKey | Active |
| 6 | Product Subcategories[ProductSubcategoryKey] | Products[ProductSubcategoryKey] | — | Active |
| 7 | Product Categories[ProductCategoryKey] | Product Subcategories[ProductCategoryKey] | — | Active |
| 8 | Territories[SalesTerritoryKey] | Sales[TerritoryKey] | — | Active |
| 9 | Territories[SalesTerritoryKey] | Returns[TerritoryKey] | — | Active |

> Eslatma: Sales[StockDate] uchun Calendar bilan ikkinchi bog'lanish kerak bo'lsa, u **inactive** bo'ladi va `USERELATIONSHIP` orqali ishlatiladi. Standart dashboard uchun shart emas.

---

## 3. Power Query tayyorgarligi (ETL)

### Sales jadvali
1. 3 ta Sales CSV ni import qiling.
2. **Append Queries** → bitta `Sales` jadvali.
3. `OrderDate`, `StockDate` → **Date** turiga o'tkazing.
4. Kalitlar (ProductKey, CustomerKey, TerritoryKey) → **Whole Number**.
5. `OrderQuantity` → **Whole Number**.

### Calendar jadvali
- Tayyor CSV import qilinadi (`Date` ustuni).
- **Yoki** to'liqroq nazorat uchun DAX bilan yarating (4-bo'limga qarang) — tavsiya etiladi.

### Products
- `ProductCost`, `ProductPrice` → **Decimal Number**.

### Boshqalar
- Lookup jadvallarni import qiling, kalit ustun turlarini to'g'rilang.

---

## 4. Calendar jadvali (DAX bilan — tavsiya etiladi)

CSV o'rniga to'liq date dimension yarating. **Modeling → New Table**:

```dax
Calendar =
VAR _min = MIN ( Sales[OrderDate] )
VAR _max = MAX ( Sales[OrderDate] )
RETURN
ADDCOLUMNS (
    CALENDAR ( DATE ( YEAR(_min), 1, 1 ), DATE ( YEAR(_max), 12, 31 ) ),
    "Year",           YEAR ( [Date] ),
    "Month Number",   MONTH ( [Date] ),
    "Month",          FORMAT ( [Date], "mmm" ),
    "Month Year",     FORMAT ( [Date], "mmm yyyy" ),
    "Quarter",        "Q" & FORMAT ( [Date], "Q" ),
    "Weekday Number", WEEKDAY ( [Date] ),
    "Weekday",        FORMAT ( [Date], "ddd" ),
    "Start of Month", STARTOFMONTH ( [Date] ),
    "Is Weekend",     IF ( WEEKDAY ( [Date], 2 ) > 5, "Weekend", "Weekday" )
)
```

So'ng **Modeling → Mark as Date Table** → `Date` ustunini tanlang.

> `Month` ustunini to'g'ri tartiblash uchun: `Month` ustunini tanlab → **Sort by Column** → `Month Number`.

---

## 5. Calculated Columns (hisoblangan ustunlar)

### Products jadvalida
```dax
-- Narx oralig'i bo'yicha guruhlash
Price Point =
SWITCH ( TRUE (),
    Products[ProductPrice] > 500, "High",
    Products[ProductPrice] > 100, "Mid-Range",
    "Low"
)
```

### Customers jadvalida
```dax
-- To'liq ism
Full Name = Customers[FirstName] & " " & Customers[LastName]
```
```dax
-- Yosh
Customer Age = DATEDIFF ( Customers[BirthDate], TODAY (), YEAR )
```
```dax
-- Daromad darajasi
Income Level =
SWITCH ( TRUE (),
    Customers[AnnualIncome] >= 150000, "Very High",
    Customers[AnnualIncome] >= 100000, "High",
    Customers[AnnualIncome] >= 50000,  "Average",
    "Low"
)
```
```dax
-- Mijoz nechta bola bilan (ota-ona/oilaviy holat)
Parent Status = IF ( Customers[TotalChildren] > 0, "Parent", "Not Parent" )
```

> Measure'lar (SUM, time-intelligence va h.k.) keyingi faylda — `03_DAX_Measures.md`.
