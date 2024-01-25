import psutil
import shelve
import time
import os
        
def get_elapsed_time_from_shelve(shelve_file):
    # Create the "shelve files" directory if it doesn't exist
    directory = "Shelve files" #os.path.dirname("Shelve files")
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Join the directory and shelve file name to get the full path
    shelve_path = os.path.join(directory, os.path.basename(shelve_file))

    # Create or open the shelve file
    with shelve.open(shelve_path) as shelf:
        # Return the value associated with 'start_time', defaulting to 0.0 if the key doesn't exist
        return float(shelf.get('start_time', 0.0))

def format_elapsed_time(elapsed_time):
    # Convert elapsed time to hours, minutes, and seconds
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

def save_elapsed_time_to_shelve(shelve_file, elapsed_time):
    # If the shelve file exists, read the previously recorded elapsed time
    existing_elapsed_time = get_elapsed_time_from_shelve(shelve_file)
    
    # Add the new elapsed time to the existing value
    total_elapsed_time = existing_elapsed_time + elapsed_time

    # Join the directory and shelve file name to get the full path
    directory = "Shelve files"
    shelve_path = os.path.join(directory, os.path.basename(shelve_file))
    
    # Save the total elapsed time to the shelve file
    with shelve.open(shelve_path) as shelf:
        shelf['start_time'] = total_elapsed_time
    
    # Convert the total elapsed time to a human-readable form
    hours, minutes, seconds = format_elapsed_time(total_elapsed_time)
    readable_file_name = f"{shelve_file}_readable.txt"
    
    # Create the readable file if it doesn't exist
    if not os.path.exists(readable_file_name):
        with open(readable_file_name, 'w') as file:
            file.write('0 hours, 0 minutes, 0 seconds')
    
    # Save total elapsed time to the readable file
    with open(readable_file_name, 'w') as file:
        file.write(f"{int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
        
def monitor_process(process_name, shelve_file):
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
                save_elapsed_time_to_shelve(shelve_file, elapsed_time)
                break
        
        # If the monitored process is not found, stop the counter
        if not process_found and counter_started:
            counter_started = False
            end_time = time.time()
            elapsed_time = end_time - start_time
            save_elapsed_time_to_shelve(shelve_file, elapsed_time)
        
        # Add a small delay to avoid excessive CPU usage
        time.sleep(5)


if __name__ == "__main__":
    # Replace "DCS.exe" with the name of the process you want to monitor
    process_to_monitor = "DCS.exe"
    shelve_file = "elapsed_time"
    monitor_process(process_to_monitor, shelve_file)
