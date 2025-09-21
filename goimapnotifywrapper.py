#!/usr/bin/env python3

"""
goimapnotify wrapper.

necessary because goimapnotify keeps crashing when no network is available,
and does not restart endlessly.
"""

import signal
import subprocess
import sys
from time import sleep

class TermHandler:
    def __init__(self, proc):
        self.proc = proc
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)

    def terminate(self, signum, frame):
        _, _ = signum, frame
        self.proc.terminate()
        exit(0)

def main():
    deathcounter = 1
    while True:
        proc = subprocess.Popen(["goimapnotify"], text=True, stderr=subprocess.PIPE)
        TermHandler(proc)
        for line in proc.stderr:
            sys.stderr.write(line)
            result = proc.poll()
            if "cannot make IMAP client" not in line:
                if result is not None:
                    exit(result)
                deathcounter = 1
        sys.stderr.write("wrapper: goimapnotify died for lack of network, restarting")
        sleep(60 * deathcounter)
        deathcounter += 1

if __name__ == "__main__":
    main()
