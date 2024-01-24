**Process Run Time Monitoring Script:**

This Python script allows you to monitor the run time of any process on a Windows system.


**1.) File Renaming:**
  Rename the file "DCS Run Time.bat" to your preference or keep it as is.

**2.) Editing the files:**
  Open the .bat file and update the paths for both your Python installation (pythonw.exe) and the location of the "elapsed_time.pyw" file.
  In the "elapsed_time.pyw" file, replace "DCS.exe" with the name of the process you wish to monitor.

**3.) Shortcut Creation:**
  Create a shortcut for the .bat file.

**4.) Startup Folder Placement:**
  Move the shortcut to "C:\Users<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup."

**5.) System Reboot:**
  Reboot the system to ensure the script runs automatically.


To monitor multiple processes simultaneously, you need to create distinct .pyw files, each with a unique name, and edit the process name as well as the name of the .txt files that they generate, inside each one of them. Then, configure separate batch files each pointing to its respective .pyw file, and execute all the batch files at startup.


After the monitored process is executed, the script will generate two .txt files in the same folder where it is saved. These files will contain the total time the monitored process has run/has been running in seconds and in hours, minutes, and seconds, respectively. The script will continuously update the run time upon each execution of the monitored process and every 5 seconds while the process is running.

To end the scripts' execution, either terminate the Python process via Task Manager or remove the shortcut to the .bat file from the startup folder and reboot the system.
