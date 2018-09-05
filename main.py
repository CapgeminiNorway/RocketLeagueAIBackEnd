import sys
import os.path
import time
import psutil
from multiprocessing import Process
import subprocess

from tournament_manager import TournamentManager

game_finished = False
score = 0

if __name__ == '__main__':
    print("starting")
    tournament = TournamentManager()
    #tournament.verify_dependencies()
    #print("dependencies verified")

    while True:
        print("Starting match")
        tournament.run_tournament()
