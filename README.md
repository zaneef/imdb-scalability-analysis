# README.md

## 🎬 IMDb Scalability Analysis Web App
This project is part of the "Software Performance and Scalability" course and is designed to:
- Build a FastAPI-based web application to search movie information from the IMDb dataset.
- Simulate realistic traffic based on rating frequency.
- Test and analyze the system's scalability using queueing theory and tools.

---

## 📁 Project Structure
```
.
├── app/                  # Application logic
│   ├── main.py           # FastAPI entry point
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic response models
│   ├── crud.py           # Database queries
│   ├── database.py       # DB connection setup
│   └── populate_db.py    # Script to import IMDb TSV files into the DB
│
├── data/                 # Data files
│   ├── imdb_data.zip     # Contains all TSV files compressed
│   └── [*.tsv]           # TSV files extracted manually
│
├── requirements.txt      # Python dependencies
├── template_env          # Template for environment variables
├── .env                  # (To be created from template_env)
└── README.md             # This file
```

---

## ⚙️ Setup Instructions

### 1. 🧱 Clone the repository
```bash
git clone https://github.com/zaneef/imdb-scalability-analysis.git
cd imdb-scalability-analysis
```

### 2. 🗃️ Unzip IMDb data
Inside the `data/` directory, you will find a compressed file `imdb_data.zip`.
Extract its contents to the same directory.

### 3. 🐘 Start PostgreSQL with Docker
```bash
docker run --name imdb-postgres \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=imdb \
  -p 5432:5432 -d postgres
```
You may customize the credentials and database name.

### 4. 📝 Configure Environment
Rename the provided `template_env` to `.env`:
```bash
cp template_env .env
```
Then edit `.env` and fill in the required values as defined above:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin
POSTGRES_DB=imdb
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 5. 🐍 Create and activate Python virtual environment
```bash
python -m venv venv
./venv/Scripts/activate     # On Windows
source venv/bin/activate   # On Unix/macOS
```

### 6. 📦 Install dependencies
```bash
pip install -r requirements.txt
```

### 7. 🧩 Populate the database
Make sure the `.tsv` files are extracted in `data/`, then run:
```bash
python -m app.populate_db
```
This script will read from the TSV files and load a subset of the IMDb dataset into the PostgreSQL database.

### 8. 🚀 Run the web application
```bash
uvicorn app.main:app --reload
```
Visit:
- Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Example Query: `/movies/?title=matrix`

---

## 📄 License
MIT License

---