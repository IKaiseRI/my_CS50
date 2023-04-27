select distinct(people.name) from people join directors on people.id = directors.person_id join movies on directors.movie_id = movies.id join ratings on ratings.movie_id = movies.id where rating >= 9;