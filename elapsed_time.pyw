import psutil
import time
import os
        
def get_elapsed_time_from_file(file_name):
    # If the file exists, read the previously recorded start time
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return float(file.read().strip())
    # Create the file if it doesn't exist
    with open(file_name, 'w') as file:
        file.write('0')
    return 0

def format_elapsed_time(elapsed_time):
    # Convert elapsed time to hours, minutes, and seconds
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

def save_elapsed_time_to_file(file_name, elapsed_time):
    # If the file exists, read the previously recorded elapsed time
    existing_elapsed_time = get_elapsed_time_from_file(file_name)
    
    # Add the new elapsed time to the existing value
    total_elapsed_time = existing_elapsed_time + elapsed_time

    # Save the total elapsed time to the file
    with open(file_name, 'w') as file:
        file.write(str(total_elapsed_time))
    
    # Save the total elapsed time to the file in a human-readable format
    hours, minutes, seconds = format_elapsed_time(total_elapsed_time)
    readable_file_name = file_name.replace(".txt", "_readable.txt")
    
    # Create the readable file if it doesn't exist
    if not os.path.exists(readable_file_name):
        with open(readable_file_name, 'w') as file:
            file.write('0 hours, 0 minutes, 0 seconds')
    
    with open(readable_file_name, 'w') as file:
        file.write(f"{int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
        
def monitor_process(process_name, file_name):
    counter_started = False
    start_time = None

    while True:
        process_found = False

        # Check for the monitored process
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == process_name:
                process_found = True
                if not counter_started:
                    counter_started = True
                    start_time = time.time()
                    break
                # Continuously update elapsed time at every iteration of while loop whilst monitored process is running. 
                end_time = time.time()
                elapsed_time = end_time - start_time
                start_time = time.time()
                save_elapsed_time_to_file(file_name, elapsed_time)
                break
        
        # If the monitored process is not found, stop the counter
        if not process_found and counter_started:
            counter_started = False
            end_time = time.time()
            elapsed_time = end_time - start_time
            save_elapsed_time_to_file(file_name, elapsed_time)
        
        # Add a small delay to avoid excessive CPU usage
        time.sleep(1)


if __name__ == "__main__":
    # Replace "DCS.exe" with the name of the process you want to monitor
    process_to_monitor = "DCS.exe"
    file_name = "elapsed_time.txt"
    monitor_process(process_to_monitor, file_name)
