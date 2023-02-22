echo Start Building... 
	&& docker network rm app
	 & docker network create app 
	&& cd database 
	&& docker build -t database . 
	&& docker run --rm -d --net app -e POSTGRES_PASSWORD=qwerty -e POSTGRES_DB=movies -p 5432:5432 --name database -v movies:/var/lib/postgresql/data database 
	&& echo Database is ready. Records Available 
	&& docker exec database psql -U postgres --dbname movies -c "SELECT * FROM movies_table;" 
	&& cd ../backend 
	&& docker build -t moviebot . 
	&& docker rm tgbot
	 & docker run -d --net app -e TOKEN=$TOKEN -e HOST=database -e PASSWORD=qwerty --name tgbot moviebot 
	&& echo Application is launched 
	&& docker run --rm -d --net app -p 8080:8088 --name superset apache/superset 
	&& docker exec -it superset superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password admin 
	&& docker exec -it superset superset db upgrade 
	&& docker exec -it superset superset init 
	&& echo Database web interface works on localhost:8080 
	&& cd ..