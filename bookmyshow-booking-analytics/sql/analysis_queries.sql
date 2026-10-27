-- BookMyShow Booking Analytics : analysis queries
-- Jahan revenue nikala hai wahan sirf 'Confirmed' bookings li hain,
-- kyunki cancelled booking ka paisa wapas ho jata hai.

USE bookmyshow_db;

-- Q1. Total bookings, revenue aur seats (overall KPI)
SELECT
    COUNT(*)                                       AS total_bookings,
    SUM(CASE WHEN booking_status = 'Confirmed' THEN total_amount ELSE 0 END) AS total_revenue,
    SUM(CASE WHEN booking_status = 'Confirmed' THEN seats_booked ELSE 0 END) AS total_seats,
    ROUND(100 * SUM(booking_status = 'Cancelled') / COUNT(*), 2)             AS cancellation_pct
FROM bookings;


-- Q2. Movie wise revenue (JOIN + GROUP BY)
SELECT
    m.movie_name,
    COUNT(*)            AS bookings,
    SUM(b.seats_booked) AS seats_sold,
    SUM(b.total_amount) AS revenue
FROM bookings b
JOIN movies m ON m.movie_id = b.movie_id
WHERE b.booking_status = 'Confirmed'
GROUP BY m.movie_name
ORDER BY revenue DESC;


-- Q3. City wise revenue (teen table ka join)
SELECT
    c.city_name,
    COUNT(*)            AS bookings,
    SUM(b.total_amount) AS revenue,
    ROUND(AVG(b.total_amount), 2) AS avg_booking_value
FROM bookings b
JOIN theatres t ON t.theatre_id = b.theatre_id
JOIN cities   c ON c.city_id    = t.city_id
WHERE b.booking_status = 'Confirmed'
GROUP BY c.city_name
ORDER BY revenue DESC;


-- Q4. Har city ki top 3 movies (CTE + RANK window function)
WITH city_movie_revenue AS (
    SELECT
        c.city_name,
        m.movie_name,
        SUM(b.total_amount) AS revenue
    FROM bookings b
    JOIN movies   m ON m.movie_id   = b.movie_id
    JOIN theatres t ON t.theatre_id = b.theatre_id
    JOIN cities   c ON c.city_id    = t.city_id
    WHERE b.booking_status = 'Confirmed'
    GROUP BY c.city_name, m.movie_name
),
ranked AS (
    SELECT
        city_name,
        movie_name,
        revenue,
        RANK() OVER (PARTITION BY city_name ORDER BY revenue DESC) AS rnk
    FROM city_movie_revenue
)
SELECT city_name, rnk, movie_name, revenue
FROM ranked
WHERE rnk <= 3
ORDER BY city_name, rnk;


-- Q5. Peak show timings (kis time pe sabse zyada bookings)
SELECT
    show_time,
    show_slot,
    COUNT(*)            AS bookings,
    SUM(seats_booked)   AS seats_sold,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS popularity_rank
FROM bookings
WHERE booking_status = 'Confirmed'
GROUP BY show_time, show_slot
ORDER BY popularity_rank;


-- Q6. Har movie ka sabse popular show time (CTE + RANK)
WITH movie_time AS (
    SELECT
        m.movie_name,
        b.show_time,
        COUNT(*) AS bookings
    FROM bookings b
    JOIN movies m ON m.movie_id = b.movie_id
    WHERE b.booking_status = 'Confirmed'
    GROUP BY m.movie_name, b.show_time
)
SELECT movie_name, show_time AS peak_show_time, bookings
FROM (
    SELECT *, RANK() OVER (PARTITION BY movie_name ORDER BY bookings DESC) AS rnk
    FROM movie_time
) x
WHERE rnk = 1
ORDER BY bookings DESC;


-- Q7. Monthly revenue trend + pichhle mahine se growth (LAG)
WITH monthly AS (
    SELECT
        DATE_FORMAT(show_date, '%Y-%m') AS month,
        SUM(total_amount)               AS revenue
    FROM bookings
    WHERE booking_status = 'Confirmed'
    GROUP BY DATE_FORMAT(show_date, '%Y-%m')
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_month,
    ROUND(100 * (revenue - LAG(revenue) OVER (ORDER BY month))
          / LAG(revenue) OVER (ORDER BY month), 2) AS growth_pct
FROM monthly
ORDER BY month;


-- Q8. Top 5 theatres by revenue
SELECT
    t.theatre_name,
    c.city_name,
    SUM(b.total_amount) AS revenue
FROM bookings b
JOIN theatres t ON t.theatre_id = b.theatre_id
JOIN cities   c ON c.city_id    = t.city_id
WHERE b.booking_status = 'Confirmed'
GROUP BY t.theatre_name, c.city_name
ORDER BY revenue DESC
LIMIT 5;


-- Q9. Payment mode ka share
SELECT
    payment_mode,
    COUNT(*) AS bookings,
    ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS share_pct
FROM bookings
GROUP BY payment_mode
ORDER BY bookings DESC;
