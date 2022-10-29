import csv
import pickle
from pathlib import Path


def exists(path):
    return Path(path).exists()

def read_csv(filename):
    with open(filename, "r", encoding="utf8") as fp:
        reader = csv.reader(fp)
        next(reader, None) # skip header
        for row in reader:
            yield row

def get_genres():
    return [
        ("name",), # header
        ("Action",),
        ("Adventure",),
        ("Animation",),
        ("Children",),
        ("Comedy",),
        ("Crime",),
        ("Documentary",),
        ("Drama",),
        ("Fantasy",),
        ("Film-Noir",),
        ("Horror",),
        ("IMAX",),
        ("Musical",),
        ("Mystery",),
        ("Romance",),
        ("Sci-Fi",),
        ("Thriller",),
        ("War",),
        ("Western",),
        ("(no genres listed)",),
    ]

def get_genome_tags():
    if exists("./data/processed/genome_tags.pickle") and exists("./data/processed/genome_tags_dict.pickle"):
        with open("./data/processed/genome_tags.pickle", "rb") as fp:
            genome_tags = pickle.load(fp)
        with open("./data/processed/genome_tags_dict.pickle", "rb") as fp:
            genome_tags_dict = pickle.load(fp)
    else:
        genome_tags_dict = {}
        genome_tags = [("id", "name")]
        for row in read_csv("./data/genome-tags.csv"):
            id = int(row[0])
            name = row[1]
            genome_tags_dict[name] = id
            genome_tags.append((id, name))
        
        with open("./data/processed/genome_tags.pickle", "wb") as fp:
            pickle.dump(genome_tags, fp)
        with open("./data/processed/genome_tags_dict.pickle", "wb") as fp:
            pickle.dump(genome_tags_dict, fp)

    return genome_tags, genome_tags_dict

def get_relates_to():

    if exists("./data/processed/relates_to.pickle"):
        with open("./data/processed/relates_to.pickle", "rb") as fp:
            relates_to = pickle.load(fp)
    else:
        relates_to = [("movieId", "tagId", "relevance")]
        for row in read_csv("./data/genome-scores.csv"):
            movieId = int(row[0])
            tagId = int(row[1])
            relevance = float(row[2])
            relates_to.append((movieId, tagId, relevance))

        with open("./data/processed/relates_to.pickle", "wb") as fp:
            pickle.dump(relates_to, fp)

    return relates_to

def get_movies_and_is_categorized_as():
    if exists("./data/processed/movies.pickle") and exists("./data/processed/is_categorized_as.pickle"):
        with open("./data/processed/movies.pickle", "rb") as fp:
            movies = pickle.load(fp)
        with open("./data/processed/is_categorized_as.pickle", "rb") as fp:
            is_categorized_as = pickle.load(fp) 
    else:
        movies = [("id", "name")]
        is_categorized_as = []

        for row in read_csv("./data/movies.csv"):
            id = int(row[0])
            name = row[1]
            genres = row[2].split("|")

            movies.append((id, name))

            for genre in genres:
                is_categorized_as.append((id, genre))
        
        with open("./data/processed/movies.pickle", "wb") as fp:
            pickle.dump(movies, fp)
        with open("./data/processed/is_categorized_as.pickle", "wb") as fp:
            pickle.dump(is_categorized_as, fp)

    return movies, is_categorized_as

def get_rates_and_users():
    if exists("./data/processed/rates.pickle") and exists("./data/processed/rates_users.pickle"):
        with open("./data/processed/rates.pickle", "rb") as fp:
            rates = pickle.load(fp)
        with open("./data/processed/rates_users.pickle", "rb") as fp:
            users = pickle.load(fp)
    else:
        rates = [("userId", "movieId", "rating")]
        users = set()

        for row in read_csv("./data/truncated/ratings.csv"):
            userId = int(row[0])
            movieId = int(row[1])
            rating = float(row[2])
    
            rates.append((userId, movieId, rating))
            users.add(userId)

        with open("./data/processed/rates.pickle", "wb") as fp:
            pickle.dump(rates, fp)
        with open("./data/processed/rates_users.pickle", "wb") as fp:
            pickle.dump(users, fp)

    return rates, users

def get_applies_and_users_and_genome_tags():
    genome_tags, genome_tags_dict = get_genome_tags()

    if exists("./data/processed/applies.pickle") and exists("./data/processed/applies_users.pickle"):
        with open("./data/processed/applies.pickle", "rb") as fp:
            applies = pickle.load(fp)
        with open("./data/processed/applies_users.pickle", "rb") as fp:
            users = pickle.load(fp)
    else:
        applies = [("userId", "movieId", "tagId")]
        users = set(())

        for row in read_csv("./data/truncated/tags.csv"):
            userId = int(row[0])
            movieId = int(row[1])
            tagId = int(genome_tags_dict.get(row[2], -1))

            if (tagId == -1):
                continue

            applies.append((userId, movieId, tagId))
            users.add(userId)

        with open("./data/processed/applies.pickle", "wb") as fp:
            pickle.dump(applies, fp)
        with open("./data/processed/applies_users.pickle", "wb") as fp:
            pickle.dump(users, fp)
    
    return applies, users, genome_tags

def get_users(applies_users, rates_users):
    users = [(user,) for user in applies_users.union(rates_users)]
    users.insert(0, ("id",))
    return users
