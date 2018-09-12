import sys
import os.path
import configparser
import random
import psutil
import subprocess
import time
import win32gui
from pyautogui import press

from rlbot.setup_manager import SetupManager

class TournamentManager:
    def __init__(self):
        self.available_bots_path = "C:/tournament_bots"
        # Default Rocket League exe path
        # C:/Program Files (x86)/Steam/steamapps/common/rocketleague/Binaries/Win32/RocketLeague.exe
        self.rocket_league_exe_path = 'D:/Steam/steamapps/common/rocketleague/Binaries/Win32/RocketLeague.exe'
        self.rlbot_cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/rlbot.cfg')

    def run_tournament(self):
        match_length, match_participants = self.set_config(num_participants=2)
        print("Running bots:", match_participants)
        # tournament.update_config(match_participants)
        print("Config updated")

        rlprocs = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if 'RocketLeague' in p.info['name']]
        if not rlprocs:
            #rl_process = subprocess.Popen(self.rocket_league_exe_path)
            #print("Rocket League running in process:", rl_process)
            # When starting Rocket League process the actual process running RL is not returned
            # We get returncode 53 when successfully starting the game
            rocket_league_process_result = subprocess.run(self.rocket_league_exe_path, shell=False)
            self.print_process_start_returncode(rocket_league_process_result)
            self.sleep_with_print(10)
        else:
            print("---Rocket League already running---")

        print("Creating match new process")
        match_process = subprocess.Popen(r"python rlbot_match.py", creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("Match runnning in process:", match_process)
        #match_process = subprocess.run(['start', 'python', 'rlbot_match.py'], shell=True)
        # match_process = subprocess.run(['runas', '/user:ps1icsovj\paperspace', 'start', 'python', 'rlbot_match.py'], shell=True)
        self.print_process_start_returncode(match_process)
        # match_process = subprocess.Popen(['cmd', 'python', 'rlbot_match.py'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True).pid
        # match_process = subprocess.call('start python rlbot_match.py', shell=True)
        # match_process = Process(target=tournament.start_match(), args={})

        #Before going to sleep, focus the game window to enable sound
        self.set_game_window_in_focus()

        # Waiting for the preset match length + 3 minute grace time to allow for process startups and match replays etc.
        sleep_time = 30  # (int(match_length.split()[0]) * 60) + 180
        print("Main process sleeping for", sleep_time, "seconds to allow game to finish")
        self.sleep_with_print(sleep_time)
        # time.sleep(60) # sleep_time)

        # As cleanup we kill both the bots and game before restarting both before the next match
        subprocess.Popen("TASKKILL /F /PID {} /T".format(match_process.pid))
        #self.kill_processes_by_name("python")
        self.kill_processes_by_name("RocketLeague")

        self.sleep_with_print(10)

        """
                print("Match started")
                while not game_finished:
                    # TODO: framework_runner.game_finished() function does not exist
                    if framework_runner.game_finished():
                        game_not_finished = True
                        score = framework_runner.get_score()

                if game_finished:
                    # TODO: tournament.add_score_to_database() function does not exist yet
                    tournament.add_score_to_database()
        """

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

    # Print on process termination
    def on_terminate(self, proc):
        print("process {} terminated with exit code {}".format(proc, proc.returncode))

    def print_process_start_returncode(self, process_result):
        if process_result.returncode == 0 or process_result.returncode == 53:
            print("Match started successfully in new process")
        else:
            print("Match was not started and new process returned exit code:", process_result.returncode)

    def kill_processes_by_name(self, process_name):
        pid_self = os.getpid()
        procs = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if process_name in p.info['name']]
        print("Current pid:", pid_self)
        print("Found these", process_name, "processes:")
        print(procs)

        self_process = [proc for proc in procs if proc['pid'] == pid_self]  # Should only return one element
        print("Removing main process from process list:", self_process)

        for proc in self_process:
            try:
                procs.remove(proc)
            except Exception as e:
                print("Access denied on process", proc['pid'], "when trying to remove")
                print("Exception thrown:", str(e))
        # We need the actual process elements in the end and not just a dictionary of pid + names
        procs = [psutil.Process(proc["pid"]) for proc in procs]

        timeout = 3
        for process in procs:
            pid = process.pid
            if pid != pid_self:
                print("Terminating process:", pid)
                # python_process = psutil.Process(pid)
                try:
                    process.terminate()
                except Exception as e:
                    print("Permission error or access denied on process", proc['pid'], "when trying to terminate")
                    print("Exception thrown:", str(e))
        """
        time.sleep(0.5)
        try:
            gone, alive = psutil.wait_procs(procs, timeout=timeout, callback=on_terminate)
            if alive:
                # send SIGKILL
                for p in alive:
                    try:
                        print("process {} survived SIGTERM; trying SIGKILL" % p)
                        p.kill()
                    except (PermissionError, AccessDenied):
                        print("Permission error or access denied on process", proc['pid'], "when trying to kill")
                time.sleep(0.5)
                try:
                    process.terminate()
                except (PermissionError, AccessDenied):
                    print("Permission error or access denied on process", proc['pid'], "when trying to terminate")
                gone, alive = psutil.wait_procs(alive, timeout=timeout, callback=on_terminate)
                if alive:
                    # give up
                    for p in alive:
                        print("process {} survived SIGKILL; giving up" % p)
        except (PermissionError, AccessDenied):
            print("Permission error or access denied on process when checking if processes are removed")
        """

    def sleep_with_print(self, seconds):
        increment = 5
        for second in range(0, seconds, increment):
            time.sleep(increment)
            print("Process has slept for", second, "seconds of total", seconds, "seconds")

    def set_game_window_in_focus(self):
        handle = win32gui.FindWindow(None, "Rocket League (32-bit, DX9, Cooked)")
        if handle is None:
            return
        try:
            win32gui.BringWindowToTop(handle)
            press('alt')
            win32gui.SetForegroundWindow(handle)
        except Exception as e:
            print("While trying to focus game window thre exception:", str(e))
