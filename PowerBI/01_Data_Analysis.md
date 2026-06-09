# 01 — Ma'lumotlar Tahlili (Data Analysis)

> AdventureWorks (velosiped va aksessuarlar sotuvchi kompaniya) ma'lumotlari.
> Davr: **2020-01-01 → 2022-06-30** (2.5 yil). Barcha raqamlar real CSV fayllardan hisoblangan.

---

## 1. Asosiy KPI'lar (umumiy ko'rsatkichlar)

| Ko'rsatkich | Qiymat | Izoh |
|---|---|---|
| **Total Revenue** | **$24.9M** | Umumiy daromad (Price × Qty) |
| **Total Cost** | $14.5M | Tannarx (Cost × Qty) |
| **Total Profit** | **$10.5M** | Sof foyda |
| **Profit Margin** | **42.0%** | Foyda marjasi — juda yuqori |
| **Quantity Sold** | 84,174 dona | Sotilgan mahsulot soni |
| **Total Orders** | 25,164 ta | Buyurtmalar (unique OrderNumber) |
| **Total Returns** | 1,828 dona | Qaytarilgan mahsulot |
| **Return Rate** | 2.17% | Qaytarish darajasi — sog'lom (norma <5%) |
| **Avg Order Value** | ~$990 | O'rtacha buyurtma qiymati |

---

## 2. Yillar bo'yicha trend

| Yil | Revenue | Sotilgan dona | Izoh |
|---|---|---|---|
| 2020 | $6.40M | 2,630 | Faqat yirik (bike) buyurtmalar — startup bosqichi |
| 2021 | $9.32M | 36,230 | **+45.6% o'sish**, aksessuar/clothing qo'shildi |
| 2022* | $9.19M | 45,314 | *Faqat 6 oy (Yan–Iyun). Yillik proyeksiya ~$18M+ |

**Insight:** 2022 yil atigi yarmi bo'lsa-da 2021 yilning deyarli barobarini bergan — kuchli o'sish tendensiyasi. Dashboard'da YoY (yildan-yilga) taqqoslashni ko'rsatish kerak.

---

## 3. Mahsulot kategoriyalari bo'yicha

| Kategoriya | Revenue | Ulush | Izoh |
|---|---|---|---|
| **Bikes** | $23.6M | **94.9%** | Daromadning asosiy manbai |
| Accessories | $0.91M | 3.6% | Ko'p dona, kichik chek |
| Clothing | $0.37M | 1.5% | Eng kichik ulush |

**Insight:** Daromad deyarli to'liq velosipedlarga bog'liq (yuqori chek, kam dona). Aksessuarlar esa dona bo'yicha ko'p sotiladi (cross-sell imkoniyati) lekin daromadga ta'siri kichik. Bu **konsentratsiya riski** — dashboardda kategoriya bo'yicha breakdown muhim.

---

## 4. Geografiya (davlatlar) bo'yicha

| Davlat | Revenue | Continent |
|---|---|---|
| United States | $7.94M | North America |
| Australia | $7.42M | Pacific |
| United Kingdom | $2.90M | Europe |
| Germany | $2.52M | Europe |
| France | $2.36M | Europe |
| Canada | $1.77M | North America |

10 ta hudud, 6 ta davlat, 3 ta qit'a (North America, Europe, Pacific). AQSh 5 ta regionga bo'lingan.

**Insight:** AQSh va Avstraliya birgalikda daromadning ~60% ini beradi. Yevropa bozori (UK+DE+FR) o'sish uchun salohiyatli.

---

## 5. Mijozlar (Customers)

- **18,148** noyob mijoz (Customer Lookup).
- Demografik atributlar mavjud: Gender, Marital Status, AnnualIncome, TotalChildren, EducationLevel, Occupation, HomeOwner, BirthDate (→ Age).
- Bu segmentatsiya uchun boy imkoniyat: daromad/yosh/kasb bo'yicha mijoz profilini ko'rsatish mumkin.

---

## 6. Qaytarishlar (Returns)

- 1,810 qator, jami 1,828 dona qaytarilgan.
- Return Rate = 2.17% — sog'lom darajada.
- ProductKey va TerritoryKey bilan bog'lanadi → qaysi mahsulot/hudud ko'p qaytaradi tahlil qilish mumkin.

---

## 7. Tavsiya etilgan dashboard fokuslari

1. **Executive Overview** — KPI kartalari + Revenue trend + YoY.
2. **Product Detail** — kategoriya/subkategoriya/mahsulot bo'yicha drill-down, eng yaxshi/yomon sotuvchilar, return rate.
3. **Customer Detail** — mijoz segmentlari, top mijozlar, AOV.
4. **Map / Geography** — davlat bo'yicha daromad xaritasi.

> Eslatma: `Product Category Sales (Unpivot Demo).csv` — bu Power Query'da Unpivot mashqi uchun namuna fayl; asosiy modelga kiritilmaydi.
