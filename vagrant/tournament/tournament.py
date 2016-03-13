#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    query =  """DELETE FROM matches;"""
    cursor.execute(query)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    query =  """DELETE FROM players;"""
    cursor.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    count = -1
    conn = connect()
    cursor = conn.cursor()
    query =  """SELECT COUNT(*) FROM players;"""
    cursor.execute(query)
    count =  cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return count

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    query =  """INSERT INTO players (name) VALUES (%s);"""
    cursor.execute(query, (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    query = """
            SELECT player.id, player.name,
            (
                SELECT COUNT(matches.id)
                FROM matches
                WHERE matches.winner_id = player.id
            ) AS wins,
            (
                SELECT COUNT(matches.id)
                FROM matches
                WHERE matches.winner_id = player.id OR matches.loser_id = player.id
            ) AS matches
            FROM players player ORDER by wins DESC;
            """
    cursor.execute(query)
    standings = cursor.fetchall()
    conn.close()

    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    query =  """INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s);"""
    cursor.execute(query, (winner,loser))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    conn = connect()
    cursor = conn.cursor()
    query = """
            WITH wins_table AS
            (
                SELECT player.id, player.name,
                (
                    SELECT COUNT(matches.id)
                    FROM matches
                    WHERE matches.winner_id = player.id
                ) AS wins
                FROM players player ORDER by wins DESC
            ),
            sequence AS
            (
            SELECT
                wins_table.id,
                wins_table.name,
                ROW_NUMBER() OVER(ORDER BY wins DESC) AS seq
            FROM
                wins_table
            )

            SELECT
                r1.id,
                r1.name,
                r2.id,
                r2.name
            FROM
                sequence r1
            JOIN
                sequence r2
                ON  (r1.seq = (r2.seq - 1))
                AND (r2.seq % 2 = 0);
            """
    cursor.execute(query)
    swiss_pairings = cursor.fetchall()
    conn.close()

    return swiss_pairings
