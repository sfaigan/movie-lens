#!/bin/sh

cd data
curl -sS https://files.grouplens.org/datasets/movielens/ml-latest.zip > ml-latest.zip
unzip ml-latest.zip
mv ml-latest/* .
rm ml-latest.zip README.txt links.csv
rm ml-latest
head -n 1000 ratings.csv > truncated/ratings.csv
head -n 1000 tags.csv > truncated/tags.csv
head -n 1000 genome-scores.csv > truncated/genome-scores.csv
