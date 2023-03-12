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

## DBMS Web App

You can manage database manually using pleasant web interface - [Apache Superset](https://hub.docker.com/r/apache/superset)

### Log In

Thanks to container has been already run you don't need to write any code!
Just navigate to `localhost:8080` and login using `admin` as username and password [screen #1](https://github.com/NPodlozhniy/movies-watchlist/blob/master/screenshots/con1.JPG)

### Connect Database

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

### Write scripts

Navigate to SQL Lab and write and run your queries or DML statements here [screen #4](https://github.com/NPodlozhniy/movies-watchlist/blob/master/screenshots/con4.JPG)

## Deploy to Heroku

As soon as Heroku as a platform doesn't have the right capabilities to use docker-compose (sometimes you can use [heroku.yml](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml) but it's pretty poor in terms of functionality compared to docker-compose) the easiest way to deploy an app is [container registry](https://devcenter.heroku.com/articles/container-registry-and-runtime)

So, we will deploy only the backend and database (without the Superset web interface) by simply using the CLI to execute the following commands:

Fisrt of all you have to create Heroku account if it already exists just log in to it
``` bash
heroku login
```
Then create a new app
``` bash
heroku create <YOUR APP>
```
Connect [Postgresql](https://devcenter.heroku.com/articles/heroku-postgresql) database add-on
``` bash
heroku addons:create heroku-postgresql:mini -a <YOUR APP>
```
Heroku offers its own docker image hub, you need to login
``` bash
heroku container:login
```
Then navigate to the folder contains the app, build the image and run it
``` bash
cd backend
heroku container:push worker
heroku container:release worker
```
### Helpful advice

Given that Heroku became a paid service recently you probably will not be happy to pay for extra database addons

So, there is a way to [share](https://devcenter.heroku.com/articles/heroku-postgresql#sharing-heroku-postgres-between-applications) one database among different Heroku apps. If you already have a database addon used in another app it can be advantageously for you:


Add existed database to created app
```
heroku addons:attach <YOUR OLD APP>::DATABASE --app <THIS APP>
```
The attached database’s URL is assigned to a config var with the name format `HEROKU_POSTGRESQL_<COLOR>_URL`

You can check the name via web interface or within a command
```
heroku addons -a <THIS APP>
```
Change the default database to [update](https://devcenter.heroku.com/articles/managing-heroku-postgres-using-cli#pg-promote) the value of the `DATABASE_URL` environment variable which is used inside the app
```
heroku pg:promote HEROKU_POSTGRESQL_<YOUR COLOR> --app <THIS APP>
```
Finally, don't forget to destroy the paid database we set up during deployment (The attachment with COLOR name appears for new database after `promote` command)
```
heroku addons:destroy HEROKU_POSTGRESQL_<CORRESPONDING COLOR> --app <THIS APP>
```
Check that for now you have only one Postgres Add-On 
```
heroku pg:info -a movies-watchlist-tgbot
```
