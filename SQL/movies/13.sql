select distinct(name) from people
join stars on people.id = stars.person_id
join movies on stars.movie_id = movies.id
where movies.title in
(select distinct(movies.title) from movies
join stars on movies.id = stars.movie_id
join people on stars.person_id = people.id
where people.name like "Kevin Bacon" and people.birth = 1958)
and people.name not like "Kevin Bacon";