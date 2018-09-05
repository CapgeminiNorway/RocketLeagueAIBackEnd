# RocketLeagueAIBackEnd
Python server Back-end for running automated Rocket League AI tournament

## Installation instructions
- `pip install -r requirements.txt`
- add rocketleague.cfg prod key for storage Azure.account_key
- Edit `self.available_bots_path = "C:/tournament_bots"` in tournament_manager.py to point to the folder where you will store all bots participating in the tournament. *Important dependency: foldername for the agent is expected to be the same as the config file inside the folder*
- Ensure that `rocket_league_exe_path = 'C:/Program Files (x86)/Steam/steamapps/common/rocketleague/Binaries/Win32/RocketLeague.exe'` is the correct installation path for Rocket League

## Run tournament after installation
`python main.py`