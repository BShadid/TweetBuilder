#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3

# interface.py :: interface for twitterRNN
#	       :: main driver for project, integrates graphics

import os, sys
import datetime
import time
import subprocess
import signal

def handler(signal, frame):
	x = 2

signal.signal(signal.SIGHUP, handler)
signal.signal(signal.SIGINT, handler)

while (True):
	subprocess.call("cat .m_freqs.txt | shuf -n 1 | cut -f 1 | ./interface2.py", shell=True)
	time.sleep(1200)
