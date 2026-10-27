-- BookMyShow Booking Analytics : table structure
-- MySQL Workbench ya VS Code (MySQL extension) me chala do

CREATE DATABASE IF NOT EXISTS bookmyshow_db;
USE bookmyshow_db;

DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS theatres;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS cities;

CREATE TABLE cities (
    city_id    INT PRIMARY KEY,
    city_name  VARCHAR(50) NOT NULL
);

CREATE TABLE movies (
    movie_id    INT PRIMARY KEY,
    movie_name  VARCHAR(100) NOT NULL
);

CREATE TABLE theatres (
    theatre_id    INT PRIMARY KEY,
    theatre_name  VARCHAR(100) NOT NULL,
    city_id       INT NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

CREATE TABLE bookings (
    booking_id      VARCHAR(20) PRIMARY KEY,
    movie_id        INT NOT NULL,
    theatre_id      INT NOT NULL,
    user_id         VARCHAR(20),
    booking_date    DATE,
    show_date       DATE,
    show_time       VARCHAR(10),
    show_slot       VARCHAR(15),
    seats_booked    INT,
    ticket_price    DECIMAL(8,2),
    total_amount    DECIMAL(10,2),
    payment_mode    VARCHAR(20),
    booking_status  VARCHAR(15),
    FOREIGN KEY (movie_id)   REFERENCES movies(movie_id),
    FOREIGN KEY (theatre_id) REFERENCES theatres(theatre_id)
);

CREATE INDEX idx_bookings_movie   ON bookings(movie_id);
CREATE INDEX idx_bookings_theatre ON bookings(theatre_id);
