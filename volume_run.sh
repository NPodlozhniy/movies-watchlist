docker build -t moviebot . 
	&& docker rm tgbot 
	 & docker run -d -v movies:/home/app/movies -e TOKEN=$TOKEN --name tgbot moviebot 
	&& docker exec -it tgbot bash -c "cat ./app/movies/movies_list.csv" 
	|| docker cp movies/movies_list.csv tgbot:home/app/movies/movies_list.csv