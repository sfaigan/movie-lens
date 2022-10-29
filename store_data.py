from psycopg2 import connect as _connect, sql
from psycopg2.extras import execute_values
import multiprocessing
from datetime import datetime
from process_data import *
from string_iterator_io import StringIteratorIO

def recreate_db():
    conn = None
    try:
        conn = _connect(database="postgres", user="postgres", password="postgres")
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("DROP DATABASE IF EXISTS movielens")
            cur.execute("CREATE DATABASE movielens")
    finally:
        if conn:
            conn.close()

def connect():
    conn = _connect(database="movielens", user="postgres", password="postgres")
    conn.set_session(autocommit=True)
    return conn

def create_tables(cursor):
    with open("schema.sql", "r") as fp:
        cursor.execute(fp.read())

def insert(table, values, cur):
    str_io = StringIteratorIO(("^".join(map(str, row)) + "\n" for row in values))
    cur.copy_from(str_io, table, sep="^", size=8192)

def init_db(recreate=False):
    print("Processing data...")

    pool = multiprocessing.Pool()

    relates_to_result = pool.apply_async(get_relates_to)
    movies_result = pool.apply_async(get_movies_and_is_categorized_as)
    rates_result = pool.apply_async(get_rates_and_users)
    applies_result = pool.apply_async(get_applies_and_users_and_genome_tags)

    # Tables
    genres = get_genres()
    relates_to = relates_to_result.get()
    movies, is_categorized_as = movies_result.get()
    rates, rates_users = rates_result.get()
    applies, applies_users, tags = applies_result.get()
    users = get_users(applies_users, rates_users)

    pool.close()

    # Initialize database
    if recreate:
        print("Recreating database...")
        recreate_db()

    try:
        conn = connect()
        with conn.cursor() as cur:

            print("Creating tables...")
            create_tables(cur)

            print("Populating users table...")
            insert("users", users[0], users[1:], cur)

            print("Populating movies table...")
            insert("movies", movies[0], movies[1:], cur)

            print("Populating tags table...")
            insert("tags", tags[0], tags[1:], cur)

            print("Populating genres table...")
            insert("genres", genres[0], genres[1:], cur)

            print("Populating applies table...")
            insert("applies", applies[0], applies[1:], cur)

            print("Populating rates table...")
            insert("rates", rates[0], rates[1:], cur)

            print("Populating relates_to table...")
            insert("relates_to", relates_to[0], relates_to[1:], cur)

            print("Populating is_categorized_as table...")
            insert("is_categorized_as", is_categorized_as[0], is_categorized_as[1:], cur)

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    start = datetime.now()
    init_db(True)
    end = datetime.now()
    print("Time taken: {}".format(end - start))
