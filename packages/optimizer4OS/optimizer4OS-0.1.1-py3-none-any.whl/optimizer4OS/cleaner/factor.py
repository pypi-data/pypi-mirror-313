import platform
from .platform_cleaner import MacCleaner, WindowsCleaner, LinuxCleaner

class CleanerFactory:
    @staticmethod
    def get_cleaner():
        os_name = platform.system()
        if os_name == "Darwin":
            return MacCleaner()
        elif os_name == "Windows":
            return WindowsCleaner()
        elif os_name == "Linux":
            return LinuxCleaner()
        else:
            raise NotImplementedError(f"Unsupported OS: {os_name}")