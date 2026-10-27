"""
Raw CSV ko clean karke data/cleaned/ me 4 tables bana deta hai:
movies, cities, theatres, bookings
"""
import numpy as np
import pandas as pd

RAW = "data/raw/bookings_raw.csv"
OUT = "data/cleaned/"

df = pd.read_csv(RAW)
print("raw shape:", df.shape)

# 1. duplicate hatao (booking_id unique hona chahiye)
before = len(df)
df = df.drop_duplicates(subset="booking_id", keep="first")
print("duplicates removed:", before - len(df))

# 2. text columns saaf karo
df["city"] = df["city"].str.strip().str.title()
df["city"] = df["city"].replace({"Bengaluru": "Bangalore"})
df["movie_name"] = df["movie_name"].str.strip()
df["theatre_name"] = df["theatre_name"].str.strip()

# 3. ticket price se "Rs." hatao aur number banao
df["ticket_price"] = (
    df["ticket_price"].astype(str)
    .str.replace("Rs.", "", regex=False)
    .str.strip()
)
df["ticket_price"] = pd.to_numeric(df["ticket_price"], errors="coerce")

# 4. dates ko sahi format me
df["booking_date"] = pd.to_datetime(df["booking_date"], format="%d-%m-%Y", errors="coerce")
df["show_date"] = pd.to_datetime(df["show_date"], format="%Y-%m-%d", errors="coerce")

# 5. show time ek hi format me (09:30 AM)
df["show_time"] = df["show_time"].str.upper().str.replace(" ", "", regex=False)
df["show_time"] = pd.to_datetime(df["show_time"], format="%I:%M%p", errors="coerce").dt.strftime("%I:%M %p")

# 6. missing / galat values
df["payment_mode"] = df["payment_mode"].fillna("Unknown")
df.loc[df["seats_booked"] <= 0, "seats_booked"] = np.nan
# seats missing hai to us movie ka median daal diya
df["seats_booked"] = df.groupby("movie_name")["seats_booked"].transform(lambda x: x.fillna(x.median()))
df["seats_booked"] = df["seats_booked"].fillna(df["seats_booked"].median()).astype(int)

# movie_name nahi hai to us row ka koi use nahi
df = df.dropna(subset=["movie_name", "ticket_price", "show_date", "show_time"])

# 7. naye columns
df["total_amount"] = df["seats_booked"] * df["ticket_price"]
hour = pd.to_datetime(df["show_time"], format="%I:%M %p").dt.hour
df["show_slot"] = np.select(
    [hour < 12, hour < 16, hour < 20],
    ["Morning", "Afternoon", "Evening"],
    default="Night",
)

# 8. dimension tables (taaki SQL me joins use ho sake)
movies = pd.DataFrame({"movie_name": sorted(df["movie_name"].unique())})
movies["movie_id"] = movies.index + 1

cities = pd.DataFrame({"city_name": sorted(df["city"].unique())})
cities["city_id"] = cities.index + 1

theatres = df[["theatre_name", "city"]].drop_duplicates().reset_index(drop=True)
theatres["theatre_id"] = theatres.index + 1
theatres = theatres.merge(cities, left_on="city", right_on="city_name")
theatre_lookup = theatres[["theatre_id", "theatre_name", "city"]]
theatres = theatres[["theatre_id", "theatre_name", "city_id"]]

# fact table: names ki jagah ids
bookings = df.merge(movies, on="movie_name").merge(theatre_lookup, on=["theatre_name", "city"])
bookings = bookings[[
    "booking_id", "movie_id", "theatre_id", "user_id", "booking_date", "show_date",
    "show_time", "show_slot", "seats_booked", "ticket_price", "total_amount",
    "payment_mode", "booking_status",
]]

movies.to_csv(OUT + "movies.csv", index=False)
cities.to_csv(OUT + "cities.csv", index=False)
theatres.to_csv(OUT + "theatres.csv", index=False)
bookings.to_csv(OUT + "bookings.csv", index=False)

print("clean bookings:", bookings.shape)
print("movies:", len(movies), "| cities:", len(cities), "| theatres:", len(theatres))
