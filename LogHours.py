def read_logged_hours(log_file_path):
    #Read the logged hours from the specified file and sum them up.
    total_seconds = 0

    try:
        with open(log_file_path, "r") as log_file:
            for line in log_file:
                parts = line.strip().split(": ")
                if len(parts) == 2:
                    time_spent = float(parts[1].split()[0])
                    total_seconds += time_spent
    except FileNotFoundError:
        print("Log file not found.")
        return
    total_hours = total_seconds / 3600
    Total_H = f"Total time: {total_hours:.2f} hours."
    return Total_H
