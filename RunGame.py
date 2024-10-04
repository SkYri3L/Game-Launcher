import subprocess
import time
import os
import webbrowser
from LogHours import time_log

def Launch(gamepaths, steampath, steamexepath, steam_app_id):
    # Launch the application
    try:
        if steampath is not None:
            process = subprocess.Popen([steamexepath, steampath])
            # subprocess.run(['xdg-open', steam_url], check=True)  # For Linux
            # subprocess.run(['open', steam_url], check=True)  # For macOS
            print(process)
            print(f"Started application: {steam_app_id}")
        else:
            process = subprocess.Popen(gamepaths)
            print(process)
            print(f"Started application: {gamepaths}")
    except Exception as e:
        print(f'An Error Occurred: {e}')
        exit()


    # Start the timer
    start_time = time.time()

    # Monitor while the application is running
    while True:
        if process.poll() is not None:  # Check if the process has exited
            break
        time.sleep(1)  # Sleep for a while to reduce CPU usage

    # End the timer
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time

    return elapsed_time


def LogTime(app_id, app_name, elapsed_time):
    """Logs the time spent on a specific application."""
    time_log(app_id, app_name, elapsed_time, "logged_hours.json")
