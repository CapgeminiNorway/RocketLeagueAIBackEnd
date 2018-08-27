# RocketLeagueAIBackEnd
Python Back-end for running Rocket League AI tournament and managing bots

## How to run tournament after installation
`python main.py`

## Installation instructions
This repository includes RLBot as a submodule: https://github.com/RLBot/RLBot
If you want to clone this reposityr remember to run the following two commands from within the cloned repository:
- `git submodule init`
- `git submodule update`
- `pip install azure azure-storage`
- add rocketleague.cfg prod key for storage Azure.account_key
-  Edit `self.available_bots_path = "C:/tournament_bots"` in tournament_manager.py to point to the folder where you will store all bots participating in the tournament. *Important dependency: foldername for the agent is expected to be the same as the config file inside the folder*
- Ensure that `rocket_league_exe_path = 'C:/Program Files (x86)/Steam/steamapps/common/rocketleague/Binaries/Win32/RocketLeague.exe'` is the correct installation path for Rocket League

Alternatively, use this command to clone this repository:
`git clone https://github.com/CapgeminiNorway/RocketLeagueAIBackEnd.git --recurse-submodules`

## dependecies
azure
azure-storage
