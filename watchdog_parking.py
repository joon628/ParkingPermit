import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the folder to monitor and the script to run
folder_to_monitor = './PDFs'
script_to_run = './ParkingPermit.py'

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file created: {event.src_path}")
            # Run your script when a new file is added
            subprocess.run(["python", script_to_run, event.src_path])

if __name__ == "__main__":
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_to_monitor, recursive=False)

    print(f"Watching folder: {folder_to_monitor}")
    print(f"Running script: {script_to_run}")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()





