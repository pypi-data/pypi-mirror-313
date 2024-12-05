import os
import shutil
from .base import CleanerBase

class MacCleaner(CleanerBase):
    """Cleaner for macOS systems."""

    def clear_cache(self):
        cache_dirs = [os.path.expanduser("~/Library/Caches"), os.path.expanduser("/Library/Caches")]
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                print(f"Cleared cache: {cache_dir}")

    def clean_logs(self):
        log_dirs = [os.path.expanduser("~/Library/Logs"), os.path.expanduser("/Library/Logs")]
        for log_dir in log_dirs:
            if os.path.exists(log_dir):
                shutil.rmtree(log_dir)
                print(f"Cleared logs: {log_dir}")

    def empty_trash(self):
        trash_dir = os.path.expanduser("~/.Trash")
        if os.path.exists(trash_dir):
            for item in os.listdir(trash_dir):
                item_path = os.path.join(trash_dir, item)
                shutil.rmtree(item_path) if os.path.isdir(item_path) else os.remove(item_path)
            print("Trash emptied.")

    def find_large_files(self, directory: str = "~", size_mb: int = 100):
        directory = os.path.expanduser(directory)
        size_bytes = size_mb * 1024 * 1024
        print(f"Searching for files larger than {size_mb}MB in {directory}...")
        os.system(f"find {directory} -size +{size_mb}M -print")

class WindowsCleaner(CleanerBase):
    """Cleaner for Windows systems."""

    def clear_cache(self):
        cache_dirs = [os.getenv("TEMP"), os.path.join(os.getenv("LOCALAPPDATA"), "Temp")]
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                print(f"Cleared cache: {cache_dir}")

    def clean_logs(self):
        log_dir = os.path.join(os.getenv("LOCALAPPDATA"), "Logs")
        if os.path.exists(log_dir):
            shutil.rmtree(log_dir)
            print(f"Cleared logs: {log_dir}")

    def empty_trash(self):
        trash_dir = os.path.join(os.getenv("SYSTEMDRIVE"), "$Recycle.Bin")
        if os.path.exists(trash_dir):
            for item in os.listdir(trash_dir):
                item_path = os.path.join(trash_dir, item)
                shutil.rmtree(item_path) if os.path.isdir(item_path) else os.remove(item_path)
            print("Trash emptied.")

    def find_large_files(self, directory: str = "C:\\", size_mb: int = 100):
        size_bytes = size_mb * 1024 * 1024
        print(f"Searching for files larger than {size_mb}MB in {directory}...")
        os.system(f'forfiles /P {directory} /S /M *.* /C "cmd /c if @fsize GTR {size_bytes} echo @path"')

class LinuxCleaner(CleanerBase):
    """Cleaner for Linux systems."""

    def clear_cache(self):
        cache_dirs = [os.path.expanduser("~/.cache"), "/var/cache"]
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                print(f"Cleared cache: {cache_dir}")

    def clean_logs(self):
        log_dirs = ["/var/log", os.path.expanduser("~/.log")]
        for log_dir in log_dirs:
            if os.path.exists(log_dir):
                shutil.rmtree(log_dir)
                print(f"Cleared logs: {log_dir}")

    def empty_trash(self):
        trash_dir = os.path.expanduser("~/.local/share/Trash/files")
        if os.path.exists(trash_dir):
            for item in os.listdir(trash_dir):
                item_path = os.path.join(trash_dir, item)
                shutil.rmtree(item_path) if os.path.isdir(item_path) else os.remove(item_path)
            print("Trash emptied.")

    def find_large_files(self, directory: str = "~", size_mb: int = 100):
        directory = os.path.expanduser(directory)
        size_bytes = size_mb * 1024 * 1024
        print(f"Searching for files larger than {size_mb}MB in {directory}...")
        os.system(f"find {directory} -size +{size_mb}M -print")