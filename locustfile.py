import json
import random
from locust import HttpUser, task, between

with open("scripts/queries.json", encoding="utf-8") as f:
    queries = json.load(f)

class IMDbUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def search_movie(self):
        query = random.choice(queries)
        self.client.get(f"/movies/?title={ query }")
