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

# Print on process termination
def on_terminate(proc):
    print("process {} terminated with exit code {}".format(proc, proc.returncode))

if __name__ == '__main__':
    print("starting")
    tournament = TournamentManager()
    tournament.verify_dependencies()
    print("dependencies verified")

    while True:
        print("Starting match")
        match_length, match_participants = tournament.set_config(num_participants=2)
        print("Running bots:", match_participants)
        #tournament.update_config(match_participants)
        print("Config updated")


        print("Creating new process")
        match_process = subprocess.run('start python rlbot_match.py', shell=True)
        #match_process = subprocess.Popen(['cmd', 'python', 'rlbot_match.py'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True).pid
        #match_process = subprocess.call('start python rlbot_match.py', shell=True)
        #match_process = Process(target=tournament.start_match(), args={})
        if match_process.returncode == 0:
            print("Match started successfully in new process")
        else:
            print("Match was not started and new process returned exit code:", match_process.returncode)

       # print("Current running child processes:", procs)
        #match_process.start()

        #print("Match is running in process:", match_process)
        sleep_time = (int(match_length.split()[0]) * 60) + 120
        print("Main process sleeping for", sleep_time, "seconds to allow game to finish")
        time.sleep(sleep_time)  # Waiting for the preset match length + 2 minute grace time

        pid_self = os.getpid()
        procs = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if 'python' in p.info['name']]
        print("Current pid:", pid_self)
        print("Found these Python processes:")
        print(procs)

        self_process = [proc for proc in procs if proc['pid'] == pid_self] # Should only return one element
        print("Removing main process from process list:", self_process)
        # either:
        for proc in self_process:
            procs.remove(proc)
        # We need the actual process elements in the end and not just a dictionary of pid + names
        procs = [psutil.Process(proc["pid"]) for proc in procs]

        timeout = 3
        for process in procs:
            pid = process.pid
            if pid != pid_self:
                print("Terminating process:", pid)
                #python_process = psutil.Process(pid)
                process.terminate()
        gone, alive = psutil.wait_procs(procs, timeout=timeout, callback=on_terminate)
        if alive:
            # send SIGKILL
            for p in alive:
                print("process {} survived SIGTERM; trying SIGKILL" % p)
                p.kill()
            gone, alive = psutil.wait_procs(alive, timeout=timeout, callback=on_terminate)
            if alive:
                # give up
                for p in alive:
                    print("process {} survived SIGKILL; giving up" % p)

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
