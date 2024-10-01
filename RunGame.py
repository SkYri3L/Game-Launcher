import subprocess
import time
import os

def GameRun(app_path):
    """Launch the application and return its process."""
    # Start the timer
    start_time = time.time()

    # Launch the application
    process = subprocess.Popen(app_path)
    print(f"Started application: {app_path}")

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

def LogTime(elapsed_time):
    with open("logged_hours.txt", "a") as log_file:
        log_file.write(f"Time spent: {elapsed_time:.2f} seconds\n")

