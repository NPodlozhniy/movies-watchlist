# movies-watchlist
The simple bot to share your favourite movies with friends

## Getting started

The appropriate way to run the app is in a docker container, so to have the docker installed is the only prerequisite for the app

### Installation

You can just copy the repo without installing any additional packages

```bash
$ git clone https://github.com/NPodlozhniy/movies-watchlist.git
$ cd movies-watchlist
```

### Usage

Even if you don't have Python installed this option will work well for you

The only thing you should do is to set an environment variable - the token of your bot
``` bash
export TOKEN=<YOUR TOKEN>  (use 'set' instead of 'export' for Windows)
```

Then you can build the app with just one command
``` bash
docker-compose up -d
```

_Important Note: If the command doesn't work, try to drop the dash and use just `docker compose ...`_

Since you have run the command and all the necessary containers are set further you can start and stop your app simply using
``` bash
docker-compose stop
docker-compose start
```
Also you can easily access the logs using 
``` bash
docker-compose logs backend
```

### Addition

You can manage database manually using pleasant web interface - [Apache Superset](https://hub.docker.com/r/apache/superset)

#### Log In

Thanks to container has been already run you don't need to write any code!
Just navigate to `localhost:8080` and login using `admin` as username and password [screen #1](https://github.com/NPodlozhniy/movies-watchlist/blob/master/screenshots/con1.JPG)

#### Connect Database

Then you need to connect the database, navigate to the plus sign in the top right corner according this [screen #2](https://github.com/NPodlozhniy/movies-watchlist/blob/master/screenshots/con3.JPG) and select PostgreSQL

Insert your parameters: [screen #3](https://github.com/NPodlozhniy/movies-watchlist/blob/master/screenshots/con2.JPG)
 - HOST you need execute `docker inspect app` and find the IPv4 address used by the container with `"Name": "database"` in the output
 - PORT sholud be `5432`
 - DATABASE NAME `movies`
 - USERNAME `postgres` (default user)
 - PASSWORD `qwerty` (is you haven't changed it during the setup)

Adjust how the database will interact with SQL Lab at least mark the following checkboxes
 - [x] Allow CREATE TABLE AS
 - [x] Allow DML

#### Write scripts

Navigate to SQL Lab and write and run your queries or DML statements here [screen #4](https://github.com/NPodlozhniy/movies-watchlist/blob/master/screenshots/con4.JPG)
