Multi-player Swiss Tournament Tracker
=====================================

Uses a PostgreSQL database to keep track of players and matches in an even-number player Swiss tournament.

Requirements
---------------

* psql
* python 2.x
* psycopg2 module for interfacing python and psql
* tournament.sql for database setup
* tournament.py for keeping track of the tournament results

Usage
------
* Database Setup : Login to the psql environment and run the following command

psql => \i tournament.sql

* Running the Program

python tournament_test.py

