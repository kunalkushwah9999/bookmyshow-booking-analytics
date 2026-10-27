# DAX Measures

Power BI me data load karne ke baad `bookings` table me yeh measures bana lena
(Modeling -> New Measure). Relationships: `bookings` -> `movies`, `bookings` -> `theatres` -> `cities`.

```DAX
Total Bookings =
CALCULATE ( COUNTROWS ( bookings ), bookings[booking_status] = "Confirmed" )

Total Revenue =
CALCULATE ( SUM ( bookings[total_amount] ), bookings[booking_status] = "Confirmed" )

Total Seats Sold =
CALCULATE ( SUM ( bookings[seats_booked] ), bookings[booking_status] = "Confirmed" )

Avg Booking Value =
DIVIDE ( [Total Revenue], [Total Bookings] )

Cancellation % =
DIVIDE (
    CALCULATE ( COUNTROWS ( bookings ), bookings[booking_status] = "Cancelled" ),
    COUNTROWS ( bookings )
)

Revenue Share % =
DIVIDE ( [Total Revenue], CALCULATE ( [Total Revenue], ALL ( movies ) ) )

Top Movie =
VAR t = TOPN ( 1, ALL ( movies[movie_name] ), [Total Revenue] )
RETURN MAXX ( t, movies[movie_name] )

Revenue Last Month =
CALCULATE ( [Total Revenue], DATEADD ( DimDate[Date], -1, MONTH ) )

MoM Growth % =
DIVIDE ( [Total Revenue] - [Revenue Last Month], [Revenue Last Month] )
```

`Revenue Last Month` ke liye ek date table chahiye:

```DAX
DimDate = CALENDAR ( DATE ( 2024, 1, 1 ), DATE ( 2024, 12, 31 ) )
```
Phir `DimDate[Date]` ko `bookings[show_date]` se jod do.
