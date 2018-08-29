import os.path
import configparser


class Config:
    def __init__(self):
        try:
            self.config = configparser.ConfigParser()
            self.config.read_file(open(os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/rocketleague.cfg")))
            home_dir = self.config["RocketLeague"]["home"]
            if not os.path.exists(home_dir):
                os.makedirs(home_dir)
            print("RocketLeague home: "+os.path.abspath(home_dir))
        except FileNotFoundError as e:
            print(e)
            print("create file rocketleague.cfg, use rocketleague-template.cfg as example")
            raise

    def account_name(self):
        return self.config["Azure"]["account_name"]

    def account_key(self):
        return self.config["Azure"]["account_key"]

    def bots_dir(self):
        return self.config["RocketLeague"]["home"]+"/bots"

    def bots_test_dir(self):
        return self.config["RocketLeague"]["home"]+"/bots_test"


# Main method.
if __name__ == '__main__':
    config = Config()
    print(config.account_name())
    print(config.account_key())
