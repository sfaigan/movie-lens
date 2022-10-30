SET client_encoding TO 'UTF8';

WITH movieids_genres AS (
		SELECT movies.id, is_categorized_as.genreName as genre FROM movies
			LEFT JOIN is_categorized_as ON movies.id=is_categorized_as.movieId
	), avg_ratings AS (
 		SELECT genre, avg(rates.rating) as avg_rating FROM movieids_genres
 			LEFT JOIN rates ON movieids_genres.id=rates.movieId
 			GROUP BY genre
 	), avg_tag_relevances AS (
 		SELECT genre, avg(relates_to.relevance) as avg_tag_relevance FROM movieids_genres
			INNER JOIN applies ON movieids_genres.id=applies.movieId 
			LEFT JOIN relates_to ON movieids_genres.id=relates_to.movieId AND applies.tagId=relates_to.tagId
			GROUP BY genre
 	)

SELECT avg_ratings.genre as genre, avg_rating, avg_tag_relevance FROM avg_ratings
	INNER JOIN avg_tag_relevances ON avg_ratings.genre=avg_tag_relevances.genre
