from abc import ABC, abstractmethod

class CleanerBase(ABC):
    @abstractmethod
    def clear_cache(self):
        pass

    @abstractmethod
    def clean_logs(self):
        pass

    @abstractmethod
    def empty_trash(self):
        pass

    @abstractmethod
    def find_large_files(self, directory: str, size_mb: int):
        pass