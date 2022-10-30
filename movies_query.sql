SET client_encoding TO 'UTF8';

WITH avg_ratings AS (
 		SELECT movies.name as movie, avg(rates.rating) as avg_rating FROM movies
 			LEFT JOIN rates ON movies.id=rates.movieId
 			GROUP BY movie
 	), avg_tag_relevances AS (
 		SELECT movies.name as movie, avg(relates_to.relevance) as avg_tag_relevance FROM movies
			INNER JOIN applies ON movies.id=applies.movieId 
			LEFT JOIN relates_to ON movies.id=relates_to.movieId AND applies.tagId=relates_to.tagId
			GROUP BY movie
 	)

SELECT avg_ratings.movie, avg_rating, avg_tag_relevance FROM avg_ratings
	INNER JOIN avg_tag_relevances ON avg_ratings.movie=avg_tag_relevances.movie
