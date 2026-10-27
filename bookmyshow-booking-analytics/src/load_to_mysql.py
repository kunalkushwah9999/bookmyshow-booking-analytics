"""
Cleaned CSV files ko MySQL me load karta hai.
Pehle sql/schema.sql chala ke tables bana lena.
"""
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

user = os.getenv("DB_USER")
pwd = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "3306")
db = os.getenv("DB_NAME", "bookmyshow_db")

engine = create_engine(f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}")

# parent tables pehle, fact table last me (foreign key ki wajah se)
tables = ["cities", "movies", "theatres", "bookings"]

with engine.begin() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    for t in reversed(tables):
        conn.execute(text(f"TRUNCATE TABLE {t}"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

for t in tables:
    df = pd.read_csv(f"data/cleaned/{t}.csv")
    df.to_sql(t, engine, if_exists="append", index=False, chunksize=2000)
    print(f"{t}: {len(df)} rows loaded")

print("done")
