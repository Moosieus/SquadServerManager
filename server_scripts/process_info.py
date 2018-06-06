"""
All of the psutil and process operations are contained within this file.
Further network monitoring utilities are planned.
"""

import psutil, os, time


def get_process(path):
    """Looks for the specified executable to be running."""
    if os.path.isfile(path) == False:
        raise FileNotFoundError
    for proc in psutil.process_iter():
        try:
            if proc.exe() == path:
                print(f"Process found! (PID={proc.pid})")
                return proc
        except psutil.AccessDenied:
            continue
    print('Process not found. Manager will wait until server process has started.')
    return


def wait_for_process(path, interval=10):
    """Waits for the specified executable to be running."""
    print("Waiting for server process...")
    proc = get_process(path)
    while proc == None:
        time.sleep(interval)
        proc = get_process(path)
    return proc
