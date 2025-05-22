import random
import csv
import json
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

cur = conn.cursor()

cur.execute("SELECT title, num_votes FROM movies WHERE num_votes > 0")
rows = cur.fetchall()

titles = [row[0] for row in rows]
weights = [row[1] for row in rows]

queries = random.choices(titles, weights=weights, k=10_000)

with open("scripts/queries.json", "w", encoding="utf-8") as f:
    json.dump(queries, f, ensure_ascii=False, indent=2)
with open("scripts/queries.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows([q] for q in queries)

cur.close()
conn.close()
