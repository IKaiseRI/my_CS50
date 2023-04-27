select movies.title from movies
join stars on movies.id = stars.movie_id
join people on people.id = stars.person_id where name like "Johnny Depp" and movies.title
in (select movies.title from movies join stars on movies.id = stars.movie_id join people on people.id = stars.person_id where name like "Helena Bonham Carter");