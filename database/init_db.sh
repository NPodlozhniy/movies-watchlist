#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "movies" <<-EOSQL
	CREATE TABLE IF NOT EXISTS movies_table
	(
		movie TEXT PRIMARY KEY,
		status TEXT NOT NULL
	);
EOSQL