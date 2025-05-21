# IMDb Scalability Analysis Web App

## 📚 Project Overview
This project was developed for the "Software Performance and Scalability" course and demonstrates the design, deployment, and performance analysis of a scalable web application. The system loads and serves movie data from the IMDb dataset through a FastAPI backend, a PostgreSQL database, and a Redis cache to improve performance under high concurrency.

---

## 🏗️ Project Structure
```
imdb-scalability-analysis/
├── app/                          # FastAPI backend
│   ├── main.py                   # Entry point
│   ├── models.py                 # SQLAlchemy models
│   ├── schemas.py                # Pydantic schemas for API
│   ├── crud.py                   # Database access logic
│   ├── database.py               # DB engine and session setup
│   ├── populate_db.py            # Loads IMDb TSV into DB
|   └── redis_client.py           # Redis client
│
├── data/                         # TSV files (downloaded at runtime)
│   ├── title.basics.tsv
│   ├── title.ratings.tsv
│   ├── title.principals.tsv
│   └── name.basics.tsv
│
├── scripts/                      # Startup and automation scripts
│   └── startup.sh                # Startup script for Docker container
│
├── jmeter/                       # Load test project for Step 3
│   ├── movies.jmx                # JMeter test plan
│   └── queries.csv               # 10k query dataset
│
|── jmt/
|   |── project_raw.jmva          # JMT model without Redis cache 
|   |── project_warmup.jmva       # JMT model with Redis cache
|   └── images/                   # images used in the report
|
├── Dockerfile                   # Dockerfile for the webapp container
├── docker-compose.yml           # Compose file to run app + db containers
├── requirements.txt             # Python dependencies
├── .env.template                # Environment variable template
├── .dockerignore                # Excludes sensitive files from build
├── generate_queries.py          # Script to create weighted random queries
└── README.md                    # This file
```

---

## ⚙️ How to Run the Project

### 1. Copy and Edit the Environment File
```bash
cp .env.template .env
```
You may edit the `.env` file if needed (not required with Docker defaults).

### 2. Build and Launch the System
```bash
docker-compose up --build
```
This will:
- Download IMDb TSV datasets
- Extract and load them into PostgreSQL
- Start a Redis container
- Launch the API server on http://localhost:8000
- Warm up the Redis cache with the 5000 most-rated movies
---

## 🔍 API Overview
Visit the Swagger documentation at:
```
http://localhost:8000/docs
```
Example usage:
```
GET /movies/?title=Matrix
```
Returns a JSON with title, year, rating, directors, and actors.

---

## 📄 License
MIT License

---

## 🙌 Credits
Developed as part of "Software Performance and Scalability" coursework at Ca' Foscari University.

---