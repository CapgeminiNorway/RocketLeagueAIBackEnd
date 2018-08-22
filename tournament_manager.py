import sys
import os.path
import configparser
import random

from rlbot.setup_manager import SetupManager

class TournamentManager:
    def __init__(self):
        self.available_bots_path = "C:\gitrepos\Tournament_bots"
        self.rlbot_cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/rlbot.cfg')

    def start_match(self):
        print("starting")
        manager = SetupManager()
        manager.startup()
        manager.load_config()
        manager.launch_bot_processes()
        manager.run()  # Runs forever until interrupted
        manager.shut_down()

    def set_config(self, num_participants):
        match_participants = self.read_botlist(num_participants)
        match_length = self.update_config(match_participants)
        return match_length, match_participants

    def read_botlist(self, num_participants):
        # TODO: Select match participants based on predetermined schedule
        available_bots = os.listdir(self.available_bots_path)
        match_participants = random.sample(available_bots, k=num_participants)
        print("Bot folders:", available_bots)
        print("match participants:", match_participants)
        return match_participants

    def update_config(self, match_participants):
        print("config at path:", self.rlbot_cfg_path)
        config = configparser.ConfigParser()
        config.read_file(open(self.rlbot_cfg_path))
        print("Getting num_participants:", config["Match Configuration"]["num_participants"])
        config["Match Configuration"]["num_participants"] = str(len(match_participants))
        print("Getting num_participants:", config["Match Configuration"]["num_participants"])
        match_length = config["Mutator Configuration"]["match length"]

        for i, bot in enumerate(match_participants):
            print("Participant" + str(i) + ":", config["Participant Configuration"]["participant_config_" + str(i)])
            bot_config_path = os.path.join(os.path.join(self.available_bots_path, bot), bot + ".cfg")
            print("Bot" + str(i), "config path:", bot_config_path)
            config["Participant Configuration"]["participant_config_"+str(i)] = bot_config_path
            print("Participant" + str(i) + " set to:", config["Participant Configuration"]["participant_config_" + str(i)])

        with open(self.rlbot_cfg_path, 'w') as configfile:
            config.write(configfile)

        return match_length

    def add_score_to_database(self):
        return ""

    def verify_dependencies(self):
        if not os.path.isdir(os.path.dirname(os.path.abspath(__file__)) + '/rlbot/src/main/python/rlbot/messages'):
            sys.exit("RLBot repository was not found. Have you initialized submodules?")
        if not os.path.isdir(os.path.dirname(os.path.abspath(__file__)) + '/rlbot/src/main/python/rlbot/messages/flat'):
            print("Assuming the tournament runner is being started for the first time")
            print("Running installation of RLBot submodule")
            # Running setup.bat inside RLBot submodule to install dependencies
            # and move the flatbuffers to the correct location
            exec(open(os.path.isdir(os.path.dirname(os.path.abspath(__file__)) + 'rlbot/setup.bat')).read())