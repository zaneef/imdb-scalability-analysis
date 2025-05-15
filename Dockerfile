FROM python:3.11-slim

WORKDIR /app

COPY app/ app/
COPY requirements.txt .
COPY .env.template .env
COPY scripts/ scripts/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN apt-get update && apt-get install -y wget unzip postgresql-client && apt-get clean

CMD ["bash", "scripts/startup.sh"]