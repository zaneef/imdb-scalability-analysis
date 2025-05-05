import csv
import traceback
from sqlalchemy.orm import Session
from . import models, database

def load_movies():
    db: Session = database.SessionLocal()

    movie_data = {}
    try:
        with open('data/title.basics.tsv', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                if row.get('titleType') != 'movie':
                    continue
                movie_data[row['tconst']] = {
                    'id': row['tconst'],
                    'title': row['primaryTitle'],
                    'year': int(row['startYear']) if row['startYear'].isdigit() else None,
                    'duration': int(row['runtimeMinutes']) if row['runtimeMinutes'].isdigit() else None,
                }
    except Exception:
        print('Error reading title.basics.tsv')
        traceback.print_exc()

    ratings = {}
    try:
        with open('data/title.ratings.tsv', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                ratings[row['tconst']] = {
                    'rating': float(row['averageRating']),
                    'num_votes': int(row['numVotes'])
                }
    except Exception:
        print('Error reading title.ratings.tsv')
        traceback.print_exc()

    people = {}
    try:
        with open('data/name.basics.tsv', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                people[row['nconst']] = row['primaryName']
    except Exception:
        print('Error reading name.basics.tsv')
        traceback.print_exc()

    cast_by_title = {}
    try:
        with open('data/title.principals.tsv', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                title_id = row['tconst']
                person_id = row['nconst']
                role = row['category']

                if title_id not in cast_by_title:
                    cast_by_title[title_id] = {
                        'directors': set(),
                        'actors': set()
                    }

                person_name = people.get(person_id, '')
                if role == 'director':
                    cast_by_title[title_id]['directors'].add(person_name)
                elif role in {'actor', 'actress'}:
                    cast_by_title[title_id]['actors'].add(person_name)
    except Exception:
        print('Error reading title.principals.tsv')
        traceback.print_exc()

    print(f"Retrieved {len(movie_data)} movies...")

    try:
        for title_id, movie in movie_data.items():
            if title_id not in ratings or title_id not in cast_by_title:
                continue

            movie_entry = models.Movie(
                id=title_id,
                title=movie.get('title', ''),
                year=movie.get('year') or 0,
                duration=movie.get('duration') or 0,
                rating=ratings[title_id].get('rating'),
                num_votes=ratings[title_id].get('num_votes'),
                directors=', '.join(cast_by_title[title_id].get('directors', [])),
                actors=', '.join(cast_by_title[title_id].get('actors', [])),
            )
            db.merge(movie_entry)
        db.commit()
    except Exception:
        print('Error inserting movies into the database')
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=database.engine)
    load_movies()
