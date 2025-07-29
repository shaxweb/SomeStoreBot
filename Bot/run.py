import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BotReloader(FileSystemEventHandler):
    def __init__(self, bot_script):
        self.bot_script = bot_script
        self.process = self.start_bot()

    def start_bot(self):
        return subprocess.Popen(["python", self.bot_script])

    def stop_bot(self):
        self.process.terminate()
        self.process.wait()

    def restart_bot(self):
        self.stop_bot()
        self.process = self.start_bot()

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"File changed: {event.src_path}. Restarting bot...")
            self.restart_bot()

if __name__ == "__main__":
    bot_script = "main.py"  # Ваш основной файл бота
    event_handler = BotReloader(bot_script)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        event_handler.stop_bot()
    observer.join()