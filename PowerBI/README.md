# AdventureWorks — Power BI Dashboard paketi

Bu papka AdventureWorks sotuv ma'lumotlari asosida professional Power BI dashboard
qurish uchun **to'liq tayyor paket** — tahlil, data model, DAX measure'lar, dizayn va
qadam-baqadam qurish qo'llanmasi.

> `.pbix` fayl ikkilik (binary) format bo'lib, Power BI Desktop'siz ishonchli generatsiya
> qilib bo'lmaydi. Shuning uchun bu yerda dashboardni **~20 daqiqada o'zingiz quradigan**
> hamma narsa (copy/paste DAX, model sxemasi, dizayn maketi) jamlangan.

## Fayllar

| Fayl | Tavsif |
|---|---|
| [`01_Data_Analysis.md`](01_Data_Analysis.md) | Ma'lumotlar tahlili, KPI'lar, insightlar (real raqamlar) |
| [`02_Data_Model.md`](02_Data_Model.md) | Star schema, bog'lanishlar, ETL, calculated columns |
| [`03_DAX_Measures.md`](03_DAX_Measures.md) | ~30 ta DAX measure (6 guruh) — copy/paste tayyor |
| [`04_Dashboard_Design.md`](04_Dashboard_Design.md) | 4 sahifa dizayn, rang palitrasi, vizual maketlar |
| [`05_Build_Guide.md`](05_Build_Guide.md) | Power BI Desktop'da 10 qadamli qurish qo'llanmasi |
| [`AdventureWorks_Theme.json`](AdventureWorks_Theme.json) | Tayyor Power BI mavzu — ranglar, shrift va vizual stillarni avtomatik qo'llaydi |

## Mavzuni (theme) qo'llash

1. Power BI Desktop'da **View → Themes → Browse for themes**.
2. `AdventureWorks_Theme.json` faylini tanlang.
3. Tamom — barcha vizual ranglari, oq kartochka foni, yumaloq burchaklar, soya va Segoe UI shriftlari avtomatik qo'llanadi.

## Tez boshlash

1. `05_Build_Guide.md` ni oching va qadamlarni bajaring.
2. DAX kodlarni `03_DAX_Measures.md` dan to'g'ridan-to'g'ri ko'chiring.
3. Vizuallarni `04_Dashboard_Design.md` maketi bo'yicha joylashtiring.
4. `01_Data_Analysis.md` dagi raqamlar bilan tekshiring.

## Asosiy ko'rsatkichlar (qisqacha)

- **Revenue:** $24.9M | **Profit:** $10.5M (42% margin)
- **Orders:** 25,164 | **Qty:** 84,174 | **Return Rate:** 2.17%
- **Davr:** 2020-01 → 2022-06 | **Mijozlar:** 18,148 | **Hududlar:** 10
- **Bikes** kategoriyasi daromadning **94.9%** ini beradi.
