# One-Page Dashboard Banane ka Tarika

## 1. Data load
Home -> Get Data -> MySQL database -> server `localhost`, database `bookmyshow_db`
-> `bookings`, `movies`, `theatres`, `cities` chaaro tables select karo.
(MySQL connector na ho to `data/cleaned/` ke CSV files bhi load kar sakte ho.)

## 2. Model view
- bookings[movie_id]   -> movies[movie_id]
- bookings[theatre_id] -> theatres[theatre_id]
- theatres[city_id]    -> cities[city_id]
Teeno many-to-one, single direction.

## 3. Layout (16:9 ek hi page)

| Jagah         | Visual                      | Fields                                   |
|---------------|-----------------------------|------------------------------------------|
| Top row       | 4 KPI cards                 | Total Bookings, Total Revenue, Avg Booking Value, Cancellation % |
| Left          | Bar chart                   | movies[movie_name] vs Total Revenue      |
| Middle        | Map / Bar chart             | cities[city_name] vs Total Revenue       |
| Right         | Column chart                | bookings[show_time] vs Total Bookings    |
| Bottom        | Line chart                  | DimDate[Month] vs Total Revenue          |
| Side panel    | Slicers                     | city_name, movie_name, show_slot, payment_mode |

## 4. Tips
- show_time ko sahi order me dikhane ke liye ek sort column bana lo (09:30 = 1, 12:45 = 2 ...).
- Sabhi visuals ke liye ek hi color theme rakho, bahut rang mat daalo.
- Dashboard ka screenshot `powerbi/dashboard_preview.png` naam se save karke GitHub me daal do.
- File ko `powerbi/BookMyShow_Dashboard.pbix` naam se save karo.
