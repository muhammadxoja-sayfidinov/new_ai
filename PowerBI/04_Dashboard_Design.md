# 04 — Dashboard Dizayni (Layout & Visuals)

4 sahifali (page) interaktiv hisobot. Har bir sahifa 1280×720 (16:9) o'lchamda.

---

## Rang palitrasi (Theme)

| Element | Rang (HEX) | Foydalanish |
|---|---|---|
| Asosiy (Primary) | `#1B3A5B` (to'q ko'k) | Sarlavhalar, KPI matni |
| Akcent (Accent) | `#E8A33D` (oltin/amber) | Asosiy ustun/chiziq, highlight |
| Ijobiy | `#2E8B57` (yashil) | O'sish, target oshgan |
| Salbiy | `#C0392B` (qizil) | Pasayish, returns |
| Fon (Background) | `#F4F6F8` (och kulrang) | Sahifa foni |
| Kartochka foni | `#FFFFFF` (oq) | KPI kartalari |
| Matn | `#2C3E50` | Asosiy matn |

**Shrift:** Segoe UI (sarlavha 16–20pt bold, matn 10–12pt).
> Tayyor mavzu uchun: View → Themes → Browse for themes. Maven/Power BI'da `.json` theme ham qo'shsa bo'ladi.

---

## SAHIFA 1 — Executive Overview (Umumiy ko'rinish)

```
┌──────────────────────────────────────────────────────────────────┐
│  AdventureWorks — Executive Dashboard          [Logo]    [📅 slicer]│
├──────────┬──────────┬──────────┬──────────┬───────────────────────┤
│ Revenue  │ Profit   │  Orders  │ Return % │   <- KPI Cards (4 ta)  │
│ $24.9M   │ $10.5M   │  25.2K   │  2.17%   │   (vs Previous Month)  │
├──────────┴──────────┴──────────┴──────────┴───────────────────────┤
│                                          │                         │
│   Revenue Trend (oylik chiziqli)         │   Revenue by Category   │
│   + Revenue Target (target line)         │   (donut / bar)         │
│                                          │                         │
├──────────────────────────────────────────┼─────────────────────────┤
│   Revenue by Country (xarita / bar)      │   Top 10 Products       │
│                                          │   (bar chart)           │
└──────────────────────────────────────────┴─────────────────────────┘
```

**Vizuallar:**
1. **KPI Cards (4 ta)** — `Total Revenue`, `Total Profit`, `Total Orders`, `Return Rate`. Har birida "vs Previous Month" trend (KPI visual yoki Card + kichik matn).
2. **Line chart** — X: `'AdventureWorks Calendar Lookup'[Month Year]`, Y: `Total Revenue`, ikkinchi qator: `Revenue Target`.
3. **Donut/Bar** — `Total Revenue` by `'AdventureWorks Product Categories Lookup'[CategoryName]`.
4. **Map yoki Bar** — `Total Revenue` by `'AdventureWorks Territory Lookup'[Country]`.
5. **Bar chart** — Top 10 `'AdventureWorks Product Lookup'[ProductName]` by `Total Revenue` (Top N filter).
6. **Slicer** — `'AdventureWorks Calendar Lookup'[Year]` (yuqori o'ng burchak).

---

## SAHIFA 2 — Product Detail (Mahsulot tahlili)

```
┌──────────────────────────────────────────────────────────────────┐
│  Product Detail        [Category slicer] [Subcategory slicer]      │
├───────────────────────┬──────────────────────────────────────────┤
│  Selected Product KPI  │   Orders vs Target (gauge / KPI)         │
│  Revenue / Profit /    │   Monthly trend (line)                   │
│  Return Rate cards     │                                          │
├───────────────────────┴──────────────────────────────────────────┤
│   Product list (table): Name | Revenue | Qty | Return Rate | Rank │
│   (drill: Category → Subcategory → Product)                       │
└──────────────────────────────────────────────────────────────────┘
```

**Vizuallar:**
1. **Slicers** — `CategoryName`, `SubcategoryName`.
2. **Matrix/Table** — ustunlar: Product, `Total Revenue`, `Quantity Sold`, `Return Rate`, `Product Rank`. Conditional formatting (return rate qizil gradient).
3. **Line chart** — tanlangan mahsulot oylik `Total Revenue` + `Revenue Target`.
4. **Gauge** — `Total Orders` vs `Order Target`.
5. **Decomposition Tree** (ixtiyoriy) — Revenue → Category → Subcategory → Product.

---

## SAHIFA 3 — Customer Detail (Mijozlar tahlili)

```
┌──────────────────────────────────────────────────────────────────┐
│  Customer Detail          [Income slicer] [Occupation slicer]      │
├──────────┬──────────┬──────────────────────────────────────────────┤
│ Total    │ Revenue/ │   Revenue by Income Level (bar)              │
│ Customers│ Customer │   Customers by Occupation (bar)              │
├──────────┴──────────┴──────────────────────────────────────────────┤
│   Top 100 Customers (table): Full Name | Orders | Revenue | Rank   │
│   + Unique customer trend (line by month)                          │
└──────────────────────────────────────────────────────────────────┘
```

**Vizuallar:**
1. **Cards** — `Total Customers`, `Revenue per Customer`, `Average Order Value`.
2. **Bar** — `Total Revenue` by `Income Level`.
3. **Bar** — `Total Customers` by `Occupation`.
4. **Donut** — by `Parent Status` yoki `Gender`.
5. **Table** — Top 100 mijoz: `Full Name`, `Total Orders`, `Total Revenue`, `Customer Rank`.
6. **Line** — oylik `Total Customers` trendi.

---

## SAHIFA 4 — Map / Geography (Geografiya)

```
┌──────────────────────────────────────────────────────────────────┐
│  Regional Performance        [Continent slicer]                    │
├────────────────────────────────────┬──────────────────────────────┤
│                                     │   Revenue by Country (bar)   │
│   Filled Map: Revenue by Country    ├──────────────────────────────┤
│   (rang intensivligi = revenue)     │   Return Rate by Country     │
│                                     │   (bar)                      │
└────────────────────────────────────┴──────────────────────────────┘
```

**Vizuallar:**
1. **Filled/Bubble Map** — Location: `Country`, size/color: `Total Revenue`.
2. **Bar** — `Total Revenue` by `Country` (saralangan).
3. **Bar** — `Return Rate` by `Country`.
4. **Slicer** — `Continent`.

---

## Interaktivlik (UX)

- **Cross-filtering:** barcha vizuallar bir-birini filtrlaydi (default yoqilgan).
- **Drill-through:** Product sahifasiga drill-through o'rnating (`'AdventureWorks Sales Data'[ProductKey]` yoki CategoryName bo'yicha).
- **Tooltips:** maxsus tooltip sahifasi — kursor ostida mini revenue trend ko'rsatish.
- **Bookmarks:** "Reset filters" tugmasi uchun bookmark.
- **Buttons:** sahifalar orasida navigatsiya (Page Navigator).
- **Slicer sync:** `Year` slicer'ini barcha sahifalarda sinxronlash (View → Sync slicers).

---

## Dizayn tamoyillari (Best Practices)

1. **Z-pattern:** eng muhim KPI yuqori-chapda, detallar pastda.
2. **Oq bo'sh joy (white space)** — vizuallarni siqib tashlamang.
3. **Ranglar maqsadli** — yashil=yaxshi, qizil=yomon, akcent rang faqat asosiy metrikaga.
4. **Maksimum 6–8 vizual** bir sahifada (kognitiv yuk).
5. **Number formatting** — $24.9M ko'rinishida (display units: Millions).
6. **Izchil sarlavhalar** va shrift o'lchami.
