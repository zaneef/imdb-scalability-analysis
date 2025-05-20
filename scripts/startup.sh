set -e

echo "Downloading IMDb data..."
mkdir -p data
cd data
wget -q https://datasets.imdbws.com/title.basics.tsv.gz
wget -q https://datasets.imdbws.com/title.ratings.tsv.gz
wget -q https://datasets.imdbws.com/title.principals.tsv.gz
wget -q https://datasets.imdbws.com/name.basics.tsv.gz

# gunzip -f *.tsv.gz
cd ..

echo "Checking if database is already populated..."
export PGPASSWORD="$POSTGRES_PASSWORD"
exists=$(psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c "SELECT COUNT(*) FROM movies;" 2>/dev/null || echo "error")
exists=$(echo "$exists" | xargs)

echo "Found $exists rows in 'movies' table."

if echo "$exists" | grep -Eq '^[0-9]+$' && [ "$exists" -gt 100 ]; then
  echo "✅ Database already populated. Skipping import."
else
  echo "Populating database..."
  python -m app.populate_db
fi

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

echo "Checking if database is already populated..."
export PGPASSWORD="$POSTGRES_PASSWORD"
exists=$(psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c "SELECT COUNT(*) FROM movies;" 2>/dev/null || echo "error")
exists=$(echo "$exists" | xargs)

echo "Found $exists rows in 'movies' table."

if echo "$exists" | grep -Eq '^[0-9]+$' && [ "$exists" -gt 100 ]; then
  echo "Database already populated. Skipping import."
else
  echo "Populating database..."
  python -m app.populate_db
fi

echo "Starting API server..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
