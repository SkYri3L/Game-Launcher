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

    result = ""
    for app_id, data in app_times.items():
        game_name = data['name']
        total_time = data['total_time'] / 3600  # Convert seconds to hours
        result += f"Application: {game_name}, Total time: {total_time:.2f} hours\n"

    return result.strip() if result else "No logged hours yet."

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
