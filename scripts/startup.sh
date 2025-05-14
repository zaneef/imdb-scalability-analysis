set -e

echo "Downloading IMDb data..."
mkdir -p data
cd data
# wget -q https://datasets.imdbws.com/title.basics.tsv.gz
# wget -q https://datasets.imdbws.com/title.ratings.tsv.gz
# wget -q https://datasets.imdbws.com/title.principals.tsv.gz
# wget -q https://datasets.imdbws.com/name.basics.tsv.gz

# gunzip -f *.tsv.gz
cd ..

if [ ! -f /app/.db_populated ]; then
  echo "Populating database (this could a while)..."
  python -m app.populate_db
  touch /app/.db_populated
else
  echo "Database already populated. Skipping."
fi

echo "Starting API server..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000