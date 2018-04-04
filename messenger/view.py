import os
import subprocess
import sys
import tempfile
from Queue import Queue, Empty
from threading import Thread

def launch_entry_console(named_pipe):
    if os.name == 'nt': # or use sys.platform for more specific names
        console = ['cmd.exe', '/c'] # or something
    else:
        console = ['xterm', '-e'] # specify your favorite terminal
                                  # emulator here

    cmd = ['python', 'entry.py', named_pipe]
    return subprocess.Popen(console + cmd)

def print_updates(queue):
    value = queue.get() # wait until value is available

    msg = ""
    while True:
        for c in "/-\|":
            minwidth = len(msg) # make sure previous output is overwritten
            msg = "\r%s %s" % (c, value)
            sys.stdout.write(msg.ljust(minwidth))
            sys.stdout.flush()

            try:
                value = queue.get(timeout=.1) # update value
                print
            except Empty:
                pass

print 'view console'
# launch updates thread
q = Queue(maxsize=1) # use queue to communicate with the thread
t = Thread(target=print_updates, args=(q,))
t.daemon = True # die with the program
t.start()

# create named pipe to communicate with the entry console
dirname = tempfile.mkdtemp()
named_pipe = os.path.join(dirname, 'named_pipe')
os.mkfifo(named_pipe) #note: there should be an analog on Windows
try:
    p = launch_entry_console(named_pipe)
    # accept input from the entry console
    with open(named_pipe) as file:
        for line in iter(file.readline, ''):
            # pass it to 'print_updates' thread
            q.put(line.strip()) # block until the value is retrieved
    p.wait()
finally:
    os.unlink(named_pipe)
    os.rmdir(dirname)
