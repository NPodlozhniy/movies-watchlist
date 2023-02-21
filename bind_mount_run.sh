docker build -t moviebot . 
	&& docker rm tgbot
	 & docker run -d -v $pwd/movies/:/home/app/movies -e TOKEN=$TOKEN --name tgbot moviebot