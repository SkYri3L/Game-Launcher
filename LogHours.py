import json
import os

def read_logged_hours(log_file_path):
    """Read the logged hours from the JSON file and return a formatted string."""
    if not os.path.exists(log_file_path) or os.path.getsize(log_file_path) == 0:
        # If the file doesn't exist or is empty, return a default message
        return "No logged hours yet."

    try:
        with open(log_file_path, "r") as log_file:
            app_times = json.load(log_file)
    except json.JSONDecodeError:
        # If the file exists but is corrupted or empty, initialize it
        app_times = {}

    hours_result = ""
    min_result = ""
    for app_id, data in app_times.items():
        game_name = data['name']

        min_time = data['total_time'] / 60
        min_result += f"Application: {game_name}, Total time: {min_time:.2f} Mins\n"

        hours_time = data['total_time'] / 3600  # Convert seconds to hours
        hours_result += f"Application: {game_name}, Total time: {hours_time:.2f} hours\n"

    return hours_result.strip() if hours_result else "No logged hours yet.", min_result.strip() if min_result else "No logged minutes yet."

def time_log(app_id, app_name, elapsed_time, log_file_path):
    """Logs the total time spent on a specific application to the JSON file."""
    app_times = {}

    if os.path.exists(log_file_path):
        try:
            with open(log_file_path, "r") as log_file:
                app_times = json.load(log_file)
        except json.JSONDecodeError:
            # If the file is corrupted, initialize it
            app_times = {}

    if app_id in app_times:
        app_times[app_id]['total_time'] += elapsed_time
        app_times[app_id]['name'] = app_name  # In case the name was updated
    else:
        app_times[app_id] = {
            "name": app_name,
            "total_time": elapsed_time
        }

    with open(log_file_path, "w") as log_file:
        json.dump(app_times, log_file, indent=4)
