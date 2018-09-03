from calculateElo import elo, expected

"""updateElo explained
losing_bots is an array of the names of the bots that lost. 
winning_bots is an array of the names of the bots that won. 
These arrays have an unique Elo-rating regardless of the number of players (i.e. only one for the whole team)
"""

def updateElo(losing_bots, winning_bots):
    elo_winning_team = 1478     # TODO: Read Elo rating for the winning team from a database
    elo_losing_team = 1658      # TODO: Read the Elo rating for the losing team from a database

    exp_win = expected(elo_winning_team, elo_losing_team)
    exp_lose = expected(elo_losing_team, elo_winning_team)

    new_elo_winning_team = elo(elo_winning_team, exp_win, 1, k=32)
    new_elo_losing_team = elo(elo_losing_team, exp_lose, 0, k=32)

    print(new_elo_winning_team)
    print(new_elo_losing_team)

    # TODO: Write Elo rating for the winning and losing team to the database




