-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Clean up
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;
--DROP DATABASE IF EXISTS tournament;

-- Create the tournament database
--CREATE DATABASE tournament;

-- Connect to the tournament database
\connect tournament;

-- Create tables
CREATE TABLE IF NOT EXISTS players (id serial NOT NULL PRIMARY KEY, name text NOT NULL);
CREATE TABLE IF NOT EXISTS matches (id serial NOT NULL PRIMARY KEY, loser_id integer NOT NULL, winner_id integer NOT NULL);

ALTER TABLE matches ADD CONSTRAINT matches_loser_id_fk FOREIGN KEY (loser_id) REFERENCES players (id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE matches ADD CONSTRAINT matches_winner_id_fk FOREIGN KEY (winner_id) REFERENCES players (id) DEFERRABLE INITIALLY DEFERRED;

SELECT * FROM players WHERE id NOT IN ( SELECT winner_id FROM matches GROUP BY winner_id );
