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
-  

Alternatively, use this command to clone this repository:
`git clone https://github.com/CapgeminiNorway/RocketLeagueAIBackEnd.git --recurse-submodules`

## dependecies
azure
azure-storage
