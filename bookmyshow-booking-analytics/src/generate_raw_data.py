"""
Real BookMyShow ka data public nahi milta, isliye yeh script ek
realistic (aur thoda gandha) booking dataset bana deti hai.
Agar tumhare paas apna CSV hai to isko skip karke seedha
data/raw/bookings_raw.csv me rakh do.
"""
import numpy as np
import pandas as pd

np.random.seed(42)
N = 10500  # 10K+ records

movies = {
    "Pathaan": 220, "Jawan": 250, "Animal": 240, "Dunki": 200,
    "Fighter": 230, "Kalki 2898 AD": 260, "Stree 2": 210,
    "Pushpa 2": 270, "Singham Again": 225, "Bhool Bhulaiyaa 3": 215,
}
cities = {
    "Mumbai": ["PVR Juhu", "INOX Nariman Point", "Cinepolis Andheri"],
    "Delhi": ["PVR Select City", "INOX Nehru Place", "Cinepolis DLF"],
    "Bangalore": ["PVR Orion", "INOX Garuda", "Cinepolis Nexus"],
    "Indore": ["PVR Treasure Island", "INOX C21 Mall", "Carnival Cinemas"],
    "Hyderabad": ["PVR Inorbit", "AMB Cinemas", "INOX GVK"],
    "Pune": ["PVR Phoenix", "INOX Amanora", "Cinepolis Seasons"],
}
shows = ["09:30 AM", "12:45 PM", "04:00 PM", "07:15 PM", "10:30 PM"]
pay = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Wallet"]
status = ["Confirmed"] * 88 + ["Cancelled"] * 12

rows = []
for i in range(N):
    m = np.random.choice(list(movies))
    c = np.random.choice(list(cities), p=[.22, .20, .18, .10, .16, .14])
    t = np.random.choice(cities[c])
    show_date = pd.Timestamp("2024-01-01") + pd.Timedelta(days=int(np.random.randint(0, 180)))
    booking_date = show_date - pd.Timedelta(days=int(np.random.randint(0, 6)))
    # evening shows zyada popular rakhe hain
    s = np.random.choice(shows, p=[.08, .17, .20, .35, .20])
    seats = int(np.random.choice([1, 2, 3, 4, 5, 6], p=[.12, .38, .2, .18, .08, .04]))
    price = movies[m] + int(np.random.choice([-20, 0, 0, 30, 60]))
    rows.append([f"BK{100000+i}", booking_date, f"user_{np.random.randint(1, 4000)}",
                 m, c, t, show_date, s, seats, price,
                 np.random.choice(pay), np.random.choice(status)])

df = pd.DataFrame(rows, columns=[
    "booking_id", "booking_date", "user_id", "movie_name", "city", "theatre_name",
    "show_date", "show_time", "seats_booked", "ticket_price", "payment_mode", "booking_status"])

# ---- ab data ko jaan bujh ke kharab karte hain ----
df["booking_date"] = df["booking_date"].dt.strftime("%d-%m-%Y")
df["show_date"] = df["show_date"].dt.strftime("%Y-%m-%d")
df["ticket_price"] = df["ticket_price"].astype(object)

# city me ajeeb spelling / spaces
idx = df.sample(400, random_state=1).index
df.loc[idx, "city"] = df.loc[idx, "city"].str.upper()
idx = df.sample(300, random_state=2).index
df.loc[idx, "city"] = " " + df.loc[idx, "city"].str.lower() + " "
idx = df.sample(150, random_state=3).index
df.loc[idx, "city"] = df.loc[idx, "city"].replace({"Bangalore": "Bengaluru"})

# price me Rs.
idx = df.sample(500, random_state=4).index
df.loc[idx, "ticket_price"] = "Rs. " + df.loc[idx, "ticket_price"].astype(str)

# missing values
df.loc[df.sample(120, random_state=5).index, "payment_mode"] = np.nan
df["seats_booked"] = df["seats_booked"].astype(float)
df.loc[df.sample(80, random_state=6).index, "seats_booked"] = np.nan
df.loc[df.sample(60, random_state=7).index, "seats_booked"] = -1
df.loc[df.sample(50, random_state=8).index, "movie_name"] = np.nan

# show time ka alag format (0930am)
idx = df.sample(350, random_state=9).index
df.loc[idx, "show_time"] = df.loc[idx, "show_time"].str.replace(" ", "").str.lower()

# duplicate rows
df = pd.concat([df, df.sample(200, random_state=10)], ignore_index=True)
df = df.sample(frac=1, random_state=11).reset_index(drop=True)

df.to_csv("data/raw/bookings_raw.csv", index=False)
print("raw data ready:", df.shape)
