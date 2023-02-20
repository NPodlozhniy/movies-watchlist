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

Then choose the way how you want your movies list will be mounted and run the appropriate command:
 - [bind mount](https://github.com/NPodlozhniy/movies-watchlist/blob/master/bind_mount_run.sh)
 - [volume](https://github.com/NPodlozhniy/movies-watchlist/blob/master/volume_run.sh)

_Important Notes:_

a) For `Windows` you should replace Linux speciefic syntax: `$TOKEN` with `%TOKEN%` and `$pwd` with `%cd%` and

b) if it doesn't work transform the commands into the one row


Since you have run one of the command and the necessary container are set further you can start and stop your app simply using
``` bash
docker start tgbot
docker stop tgbot
```
Also you can easily access the logs using 
``` bash
docker logs -t tgbot
```
