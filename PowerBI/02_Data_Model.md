# 02 — Data Model (Star Schema)

Bu model **yulduz sxemasi (star schema)** asosida qurilgan: markazda fakt jadvallar (AdventureWorks Sales Data, AdventureWorks Returns Data), atrofida o'lcham (dimension/lookup) jadvallar.

> **MUHIM:** Jadval nomlari CSV import qilinganda kelgan asl nomlarga **to'liq** mos saqlangan (`AdventureWorks ...`). DAX'da nomida bo'sh joy bo'lgani uchun bitta qo'shtirnoq ishlatiladi: `'AdventureWorks Sales Data'[OrderQuantity]`. Shu tariqa copy-paste to'g'ridan-to'g'ri ishlaydi.

---

## 1. Jadvallar (Tables)

### Fakt jadvallar (Fact tables)
| Jadval | Manba | Tavsif |
|---|---|---|
| **AdventureWorks Sales Data** | Sales Data 2020 + 2021 + 2022 | 3 ta CSV **Append** orqali bitta jadvalga birlashtiriladi (~56,000 qator) |
| **AdventureWorks Returns Data** | AdventureWorks Returns Data | Qaytarishlar (~1,809 qator) |

### O'lcham jadvallar (Dimension / Lookup tables)
| Jadval | Kalit (Key) | Tavsif |
|---|---|---|
| **AdventureWorks Calendar Lookup** | Date | Sana o'lchami (date dimension) |
| **AdventureWorks Customer Lookup** | CustomerKey | Mijoz ma'lumotlari |
| **AdventureWorks Product Lookup** | ProductKey | Mahsulotlar (narx, tannarx) |
| **AdventureWorks Product Subcategories Lookup** | ProductSubcategoryKey | Subkategoriya |
| **AdventureWorks Product Categories Lookup** | ProductCategoryKey | Kategoriya |
| **AdventureWorks Territory Lookup** | SalesTerritoryKey | Hudud/davlat/qit'a |

> `Product Category Sales (Unpivot Demo).csv` modelga **kiritilmaydi** — u faqat Power Query Unpivot mashqi uchun.

> **Eslatma (Sales Data nomi):** 3 ta sotuv faylini Append qilganda natija jadvalini **`AdventureWorks Sales Data`** deb nomlang (quyidagi barcha DAX shu nomga tayanadi). Agar boshqa nom qo'ysangiz, DAX'dagi `'AdventureWorks Sales Data'` ni o'sha nomga almashtiring.

---

## 2. Bog'lanishlar (Relationships)

Barchasi **One-to-Many (1:*)**, yo'nalishi **Single** (lookup → fact), filtr o'lchamdan faktga oqadi.

```
              ┌───────────────────────────────────────┐
              │  AdventureWorks Product Categories     │
              │       Lookup (ProductCategoryKey)      │
              └────────────────────┬───────────────────┘
                                   │ 1
                                   │ *
              ┌────────────────────┴───────────────────┐
              │ AdventureWorks Product Subcategories    │
              │     Lookup (ProductSubcategoryKey)      │
              └────────────────────┬───────────────────┘
                                   │ 1
                                   │ *
 ┌──────────────────┐    ┌─────────┴─────────┐    ┌──────────────────┐
 │ AdventureWorks   │1  *│  AdventureWorks   │1  *│  AdventureWorks  │
 │ Calendar Lookup  ├────┤  Product Lookup   ├────┤  Returns Data    │
 │     (Date)       │    │   (ProductKey)    │    │                  │
 └────────┬─────────┘    └─────────┬─────────┘    └────────┬─────────┘
          │1                       │1                       │*
          │                        │*                       │
          │*             ┌─────────┴─────────┐              │
          └──────────────┤  AdventureWorks   │              │
                         │    Sales Data     │              │
 ┌──────────────────┐    │                   │    ┌──────────────────┐
 │ AdventureWorks   │1  *│                   │    │  AdventureWorks  │1
 │ Customer Lookup  ├────┴─────────┬─────────┘    │ Territory Lookup │
 │  (CustomerKey)   │              │*             │ (SalesTerr.Key)  │
 └──────────────────┘              │              └────────┬─────────┘
                                   │   (Territory 1:* Sales Data)
                                   └───────────────────────┤
                                       (Territory 1:* Returns Data)
```

### Bog'lanishlar ro'yxati

| # | Dan (1 tomon) | Ga (* tomon) | Maydon | Faollik |
|---|---|---|---|---|
| 1 | AdventureWorks Calendar Lookup[Date] | AdventureWorks Sales Data[OrderDate] | Date / OrderDate | **Active** |
| 2 | AdventureWorks Calendar Lookup[Date] | AdventureWorks Returns Data[ReturnDate] | Date / ReturnDate | Active |
| 3 | AdventureWorks Customer Lookup[CustomerKey] | AdventureWorks Sales Data[CustomerKey] | CustomerKey | Active |
| 4 | AdventureWorks Product Lookup[ProductKey] | AdventureWorks Sales Data[ProductKey] | ProductKey | Active |
| 5 | AdventureWorks Product Lookup[ProductKey] | AdventureWorks Returns Data[ProductKey] | ProductKey | Active |
| 6 | AdventureWorks Product Subcategories Lookup[ProductSubcategoryKey] | AdventureWorks Product Lookup[ProductSubcategoryKey] | — | Active |
| 7 | AdventureWorks Product Categories Lookup[ProductCategoryKey] | AdventureWorks Product Subcategories Lookup[ProductCategoryKey] | — | Active |
| 8 | AdventureWorks Territory Lookup[SalesTerritoryKey] | AdventureWorks Sales Data[TerritoryKey] | — | Active |
| 9 | AdventureWorks Territory Lookup[SalesTerritoryKey] | AdventureWorks Returns Data[TerritoryKey] | — | Active |

> Eslatma: AdventureWorks Sales Data[StockDate] uchun Calendar bilan ikkinchi bog'lanish kerak bo'lsa, u **inactive** bo'ladi va `USERELATIONSHIP` orqali ishlatiladi. Standart dashboard uchun shart emas.

---

## 3. Power Query tayyorgarligi (ETL)

### AdventureWorks Sales Data jadvali
1. 3 ta Sales CSV ni import qiling.
2. **Append Queries** → bitta jadvalga birlashtiring, nomini **`AdventureWorks Sales Data`** qo'ying.
3. `OrderDate`, `StockDate` → **Date** turiga o'tkazing.
4. Kalitlar (ProductKey, CustomerKey, TerritoryKey) → **Whole Number**.
5. `OrderQuantity` → **Whole Number**.

### AdventureWorks Calendar Lookup jadvali
- Tayyor CSV import qilinadi (`Date` ustuni) — nomi `AdventureWorks Calendar Lookup`.
- **Yoki** to'liqroq nazorat uchun DAX bilan yarating (4-bo'limga qarang) — tavsiya etiladi.

### AdventureWorks Product Lookup
- `ProductCost`, `ProductPrice` → **Decimal Number**.

### Boshqalar
- Lookup jadvallarni import qiling, kalit ustun turlarini to'g'rilang.

---

## 4. AdventureWorks Calendar Lookup jadvali (DAX bilan — tavsiya etiladi)

CSV o'rniga to'liq date dimension yarating. **Modeling → New Table**:

```dax
AdventureWorks Calendar Lookup =
VAR _min = MIN ( 'AdventureWorks Sales Data'[OrderDate] )
VAR _max = MAX ( 'AdventureWorks Sales Data'[OrderDate] )
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

> Agar tayyor CSV (`AdventureWorks Calendar Lookup`) ishlatsangiz, bu DAX jadvalini yaratmang — aks holda nom to'qnashadi. Bittasini tanlang.

So'ng **Modeling → Mark as Date Table** → `Date` ustunini tanlang.

> `Month` ustunini to'g'ri tartiblash uchun: `Month` ustunini tanlab → **Sort by Column** → `Month Number`.

---

## 5. Calculated Columns (hisoblangan ustunlar)

### AdventureWorks Product Lookup jadvalida
```dax
-- Narx oralig'i bo'yicha guruhlash
Price Point =
SWITCH ( TRUE (),
    'AdventureWorks Product Lookup'[ProductPrice] > 500, "High",
    'AdventureWorks Product Lookup'[ProductPrice] > 100, "Mid-Range",
    "Low"
)
```

### AdventureWorks Customer Lookup jadvalida
```dax
-- To'liq ism
Full Name = 'AdventureWorks Customer Lookup'[FirstName] & " " & 'AdventureWorks Customer Lookup'[LastName]
```
```dax
-- Yosh
Customer Age = DATEDIFF ( 'AdventureWorks Customer Lookup'[BirthDate], TODAY (), YEAR )
```
```dax
-- Daromad darajasi
Income Level =
SWITCH ( TRUE (),
    'AdventureWorks Customer Lookup'[AnnualIncome] >= 150000, "Very High",
    'AdventureWorks Customer Lookup'[AnnualIncome] >= 100000, "High",
    'AdventureWorks Customer Lookup'[AnnualIncome] >= 50000,  "Average",
    "Low"
)
```
```dax
-- Mijoz nechta bola bilan (ota-ona/oilaviy holat)
Parent Status = IF ( 'AdventureWorks Customer Lookup'[TotalChildren] > 0, "Parent", "Not Parent" )
```

> Measure'lar (SUM, time-intelligence va h.k.) keyingi faylda — `03_DAX_Measures.md`.
