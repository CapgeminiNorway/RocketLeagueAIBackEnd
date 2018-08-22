import sys
import os.path
sys.path.insert(0, os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + 'rlbot/src/main/python/'))
from rlbot import runner as framework_runner
from tournament_manager import TournamentManager

game_finished = False
score = 0
bot_location = "C:\gitrepos\Tournament_bots"

if __name__ == '__main__':
    print("starting")
    tournament = TournamentManager()
    tournament.verify_dependencies()
    print("dependencies verified")

    while True:
        print("Starting match")
        match_participants = tournament.get_bots(2)
        print("Running bots:", match_participants)
        #tournament.update_config(match_participants)
        print("Config updated")
        framework_runner.main()
        print("Match started")
        while not game_finished:
            # TODO: framework_runner.game_finished() function does not exist
            if framework_runner.game_finished():
                game_not_finished = True
                score = framework_runner.get_score()

        if game_finished:
            # TODO: tournament.add_score_to_database() function does not exist yet
            tournament.add_score_to_database()
