# 05 — Qurish Qo'llanmasi (Power BI Desktop'da qadam-baqadam)

> Maqsad: quyidagi qadamlar bilan ~20 daqiqada to'liq dashboard tayyor bo'ladi.
> Kerak: **Power BI Desktop** (bepul, Microsoft Store yoki powerbi.microsoft.com).

---

## QADAM 1 — Ma'lumotlarni yuklash (Get Data)

1. **Home → Get Data → Text/CSV**.
2. Quyidagilarni import qiling:
   - 3 ta `Sales Data 20XX.csv`
   - `Returns Data.csv`
   - `Customer Lookup.csv`
   - `Product Lookup.csv`
   - `Product Subcategories Lookup.csv`
   - `Product Categories Lookup.csv`
   - `Territory Lookup.csv`
   - (`Calendar Lookup.csv` — ixtiyoriy, biz DAX bilan yaratamiz)
3. Har birini **Transform Data** (Power Query'ga kirish) bilan oching.

---

## QADAM 2 — Power Query tozalash (Transform)

1. **Sales jadvallarini birlashtirish:**
   - `Home → Append Queries → Append Queries as New`.
   - 3  ta sales jadvalini tanlang → natijani **Sales** deb nomlang.
   - Eski 3 ta query'ni **Enable load** dan o'chiring (yuklamaslik uchun).
2. **Ma'lumot turlarini to'g'rilang:**
   - `OrderDate`, `StockDate`, `ReturnDate` → Date.
   - Barcha `...Key` ustunlar → Whole Number.
   - `ProductCost`, `ProductPrice` → Decimal Number.
   - `OrderQuantity`, `ReturnQuantity` → Whole Number.
3. Jadval nomlarini soddalashtiring: `Customers`, `Products`, `Product Subcategories`, `Product Categories`, `Territories`, `Returns`.
4. **Close & Apply**.

---

## QADAM 3 — Calendar jadvali (DAX)

1. **Modeling → New Table** → `02_Data_Model.md` dagi `Calendar` kodini joylashtiring.
2. `Calendar` tanlangan holda **Table tools → Mark as Date Table → Date**.
3. `Month` ustunini **Sort by Column → Month Number** qiling (`Quarter`, `Weekday` uchun ham mos raqamli ustun bilan).

---

## QADAM 4 — Bog'lanishlar (Model view)

1. Chap paneldan **Model view** ga o'ting.
2. `02_Data_Model.md` dagi 9 ta bog'lanishni tekshiring/yarating (drag & drop).
3. Har biri **1:* , Single direction** ekanligiga ishonch hosil qiling:
   - Calendar[Date] → Sales[OrderDate] **(active)**
   - Calendar[Date] → Returns[ReturnDate]
   - Customers → Sales, Products → Sales, Products → Returns
   - Subcategories → Products, Categories → Subcategories
   - Territories → Sales, Territories → Returns

---

## QADAM 5 — Calculated Columns

`02_Data_Model.md` dagi ustunlarni qo'shing:
- **Products:** `Price Point`
- **Customers:** `Full Name`, `Customer Age`, `Income Level`, `Parent Status`

(Har biri: tegishli jadval → **New Column** → kodni joylashtiring.)

---

## QADAM 6 — Measures

1. **Home → Enter Data** → bo'sh jadval → nomi `_Measures` → Load.
2. `_Measures` tanlangan holda **New Measure** bilan `03_DAX_Measures.md` dagi barcha measure'larni qo'shing.
3. Har birini formatlang (Currency / Percentage / Whole Number — faylda ko'rsatilgan).

> Maslahat: avval Core (1-guruh), keyin Returns, keyin Time Intelligence tartibida qo'shing — chunki keyingilar oldingilariga tayanadi.

---

## QADAM 7 — Vizuallar (Report view)

`04_Dashboard_Design.md` maketiga amal qiling:
1. **Sahifalar yarating:** Overview, Product Detail, Customer Detail, Geography (pastdagi `+` tugma, nom o'zgartirish: double-click).
2. **KPI Cards:** Card visual → measure'ni tashlang.
3. **Line chart:** X = `Month Year`, Y = `Total Revenue` + `Revenue Target`.
4. **Donut/Bar:** Category/Country breakdown.
5. **Map:** Filled Map → Location = `Country`, Color saturation = `Total Revenue`.
6. **Table/Matrix:** Top products/customers + conditional formatting.
7. **Slicers:** `Year`, `Category`, `Continent` qo'shing.

---

## QADAM 8 — Dizayn va sayqal (Polish)

1. **View → Themes** → mos mavzu tanlang (yoki `04_Dashboard_Design.md` ranglarini qo'llang).
2. Sarlavhalar, sahifa fonini sozlang.
3. **Display units:** Cards va o'qlarda → Millions (`$24.9M`).
4. **Sync slicers** (View → Sync slicers) — `Year` ni barcha sahifalarda.
5. **Page navigation buttons** (Insert → Buttons → Navigator).
6. **Drill-through** sahifasi (Product Detail) o'rnating.

---

## QADAM 9 — Tekshirish (Validation)

Quyidagi raqamlar `01_Data_Analysis.md` bilan mos kelishi kerak (filtr yo'q holatda):

| Tekshiruv | Kutilgan |
|---|---|
| Total Revenue | ~$24.9M |
| Total Profit | ~$10.5M |
| Profit Margin | ~42% |
| Total Orders | ~25,164 |
| Return Rate | ~2.17% |
| Bikes ulushi | ~94.9% |

Agar mos kelsa — model to'g'ri qurilgan! ✅

---

## QADAM 10 — Saqlash va ulashish

1. **File → Save as** → `AdventureWorks_Dashboard.pbix`.
2. Nashr qilish: **Home → Publish → Power BI Service** (workspace tanlang).
3. Service'da dashboard pin qilish, ulashish (share) yoki PDF/PowerPoint eksport.

---

### Foydali qisqa yo'llar (shortcuts)
- `Ctrl + C / V` — vizualni nusxalash (formatni saqlaydi).
- `F4` — format painter rejimi.
- Vizualni tanlab **Format → General → "Edit interactions"** — cross-filter xatti-harakatini boshqarish.
