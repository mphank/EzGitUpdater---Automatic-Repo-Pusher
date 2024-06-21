import json
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, repo_path, branch):
        self.repo_path = repo_path
        self.branch = branch

    def on_any_event(self, event):
        if event.is_directory:
            return
        print(f"Detected change in {event.src_path}. Committing and pushing to GitHub.")
        self.commit_and_push()

    def commit_and_push(self):
        commands = [
            f"cd {self.repo_path} && git add .",
            f'cd {self.repo_path} && git commit -m "Automated commit for changes in watched directories"',
            f"cd {self.repo_path} && git push origin {self.branch}"
        ]
        for cmd in commands:
            subprocess.run(cmd, shell=True)

def main():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    
    event_handler = ChangeHandler(settings['repo_path'], settings['branch'])
    observer = Observer()
    
    for directory in settings['watch_directories']:
        observer.schedule(event_handler, directory, recursive=True)
    
    observer.start()
    print("Started monitoring directories for changes. Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
