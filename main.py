import sys
import os.path
import time
import psutil
from multiprocessing import Process
import subprocess

sys.path.insert(0, os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + 'rlbot/src/main/python/'))
from tournament_manager import TournamentManager

game_finished = False
score = 0
rocket_league_exe_path = 'C:/Program Files (x86)/Steam/steamapps/common/rocketleague/Binaries/Win32/RocketLeague.exe'


# Print on process termination
def on_terminate(proc):
    print("process {} terminated with exit code {}".format(proc, proc.returncode))


def print_process_start_returncode(process_result):
    if process_result.returncode == 0:
        print("Match started successfully in new process")
    else:
        print("Match was not started and new process returned exit code:", process_result.returncode)


def kill_processes_by_name(process_name):
    pid_self = os.getpid()
    procs = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if process_name in p.info['name']]
    print("Current pid:", pid_self)
    print("Found these Python processes:")
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

def sleep_with_print(seconds):
    increment = 5
    for second in range(0, seconds, increment):
        time.sleep(increment)
        print("Process has slept for", second+1, "seconds of total", seconds, "seconds")

if __name__ == '__main__':
    print("starting")
    tournament = TournamentManager()
    #tournament.verify_dependencies()
    #print("dependencies verified")

    while True:
        print("Starting match")
        match_length, match_participants = tournament.set_config(num_participants=2)
        print("Running bots:", match_participants)
        #tournament.update_config(match_participants)
        print("Config updated")

        rlprocs = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if 'RocketLeague' in p.info['name']]
        if not rlprocs:
            rocket_league_process_result = subprocess.run(rocket_league_exe_path, shell=False)
            print_process_start_returncode(rocket_league_process_result)
            sleep_with_print(60)
        else:
            print("---Rocket League already running---")

        print("Creating match new process")
        match_process = subprocess.run(['start', 'python', 'rlbot_match.py'], shell=True)
        #match_process = subprocess.run(['runas', '/user:ps1icsovj\paperspace', 'start', 'python', 'rlbot_match.py'], shell=True)
        print_process_start_returncode(match_process)
        #match_process = subprocess.Popen(['cmd', 'python', 'rlbot_match.py'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True).pid
        #match_process = subprocess.call('start python rlbot_match.py', shell=True)
        #match_process = Process(target=tournament.start_match(), args={})

        # Waiting for the preset match length + 3 minute grace time to allow for process startups and match replays etc.
        sleep_time = (int(match_length.split()[0]) * 60) + 180
        print("Main process sleeping for", sleep_time, "seconds to allow game to finish")
        sleep_with_print(sleep_time)
        #time.sleep(60) # sleep_time)

        # As cleanup we kill both the bots and game before restarting both before the next match
        kill_processes_by_name("python")
        kill_processes_by_name("RocketLeague")
        
        sleep_with_print(60)

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
