import time
import os

# responsible for validation of game bots


class ValidationManager:

    def __init__(self):
        print('Validation Manager - stub file')

    # returns True if bot is valid and eligible for tournament
    # False if not
    def validate(self, full_path_to_bot):
        print("validate "+full_path_to_bot)
        time.sleep(1)
        print("validation done, bot is valid")
        is_valid = self.validate_required_files(full_path_to_bot) and self.validate_bot(full_path_to_bot)
        return is_valid

    def validate_required_files(self, full_path_to_bot):
        dir_content = os.listdir(full_path_to_bot)
        final_path_to_bot_dir = full_path_to_bot
        if len(dir_content) == 1 and os.path.isdir(dir_content[0]):
                final_path_to_bot_dir = dir_content[0]
        print("validate bot config "+final_path_to_bot_dir)
        return True

    # validate Bot is doing something in RocketLeague

    def validate_bot(self, full_path_to_bot):
        return True