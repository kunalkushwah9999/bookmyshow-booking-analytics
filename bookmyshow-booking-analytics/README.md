# BookMyShow Booking Analytics

Movie booking ke 10K+ records ko Python se clean kiya, MySQL me daala, SQL se analyze kiya
aur Power BI me ek page ka dashboard banaya. Maksad yeh samajhna tha ki kaunsi movie,
kaunsa city aur kaunsa show time sabse zyada bookings laata hai.

**Tech stack:** Python, pandas, NumPy, MySQL, SQL (joins, CTE, window functions), Power BI

> Note: BookMyShow ka asli data public nahi hai, isliye `src/generate_raw_data.py` se ek
> realistic dummy dataset banaya hai (10,700 rows, jaan bujh ke gandha). Numbers isi dummy
> data ke hain, asli BookMyShow ke nahi.

## Folder structure

```
bookmyshow-booking-analytics/
├── data/
│   ├── raw/                 # gandha data (bookings_raw.csv)
│   └── cleaned/             # clean tables (movies, cities, theatres, bookings)
├── src/
│   ├── generate_raw_data.py # dummy raw data banata hai
│   ├── clean_data.py        # pandas cleaning
│   └── load_to_mysql.py     # MySQL me load
├── sql/
│   ├── schema.sql           # tables + foreign keys
│   └── analysis_queries.sql # 9 analysis queries
├── powerbi/
│   ├── dax_measures.md
│   └── dashboard_guide.md
├── requirements.txt
└── .env.example
```

## Kaise chalayein

```bash
# 1. virtual environment
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt

# 2. data banao aur clean karo
python src/generate_raw_data.py
python src/clean_data.py

# 3. MySQL me tables banao (Workbench me sql/schema.sql run karo)
#    phir .env.example ko copy karke .env banao aur password daalo
python src/load_to_mysql.py

# 4. sql/analysis_queries.sql chalao, phir Power BI se connect karo
```

## Cleaning me kya kiya

- 200 duplicate bookings hataye (booking_id ke basis par)
- City names theek kiye: `MUMBAI`, ` delhi `, `Bengaluru` jaise variations ek standard naam me
- `Rs. 250` jaise price strings ko number banaya
- Alag alag date aur time formats ko ek format me kiya
- Negative / missing seats ko us movie ke median se bhara
- Missing payment mode ko `Unknown` rakha, bina movie name wali rows hata di
- Naye columns: `total_amount`, `show_slot` (Morning / Afternoon / Evening / Night)
- Data ko 4 tables me tod diya (movies, cities, theatres, bookings) taaki joins use ho sakein

## SQL me kya kiya

| Query | Kya nikala | Concept |
|-------|-----------|---------|
| Q1 | Overall KPIs | CASE WHEN, aggregation |
| Q2 | Movie wise revenue | JOIN, GROUP BY |
| Q3 | City wise revenue | 3 table JOIN |
| Q4 | Har city ki top 3 movies | CTE, RANK() |
| Q5 | Peak show timings | RANK() OVER |
| Q6 | Har movie ka best show time | CTE, RANK() PARTITION BY |
| Q7 | Monthly growth | LAG() |
| Q8 | Top 5 theatres | JOIN, LIMIT |
| Q9 | Payment mode share | window SUM |

## Dashboard

Ek page me KPI cards (bookings, revenue, avg value, cancellation %), movie / city / show time
ke charts aur city, movie, slot, payment mode ke slicers hain. DAX measures `powerbi/dax_measures.md`
me hain, aur banane ka tarika `powerbi/dashboard_guide.md` me.

## Findings (dummy data par)

- Pushpa 2 sabse zyada revenue wali movie rahi
- Mumbai revenue me sabse aage, uske baad Delhi aur Bangalore
- 07:15 PM ka show sabse busy raha, Evening slot me sabse zyada bookings
- Lagbhag 11% bookings cancel hui
