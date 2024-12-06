"""Deals with memory related stuffs."""
import psutil


class MemoryManager:
    """A class to manage and retrieve memory usage information."""

    @staticmethod
    def get_memory_stats() -> tuple[float, float, float, float]:
        """Retrieves memory statistics for the current user, total system, system processes, and available memory.

        Returns:
            tuple: A tuple containing:
                - Total RAM used by the current user in gigabytes (GB) with two decimal places.
                - Total RAM used by all users in gigabytes (GB) with two decimal places.
                - Average RAM used by system processes in gigabytes (GB) with two decimal places.
                - Available RAM in gigabytes (GB) with two decimal places.

        Raises:
            None
        """
        current_user_memory = MemoryManager._get_current_user_memory_usage()
        total_memory_used = MemoryManager._get_total_memory_usage()
        system_processes_memory = MemoryManager._get_system_processes_memory_usage()
        available_memory = MemoryManager._get_available_memory()

        return (
            round(current_user_memory, 2),
            round(total_memory_used, 2),
            round(system_processes_memory, 2),
            round(available_memory, 2),
        )

    @staticmethod
    def _get_current_user_memory_usage() -> float:
        """Retrieves the total RAM used by the current user.

        Returns:
            float: RAM used by the current user in gigabytes (GB).

        Raises:
            None
        """
        current_user = psutil.Process().username()  # Get the current user's username
        total_memory = 0.0

        for proc in psutil.process_iter(["memory_info", "username"]):
            try:
                if proc.info["username"] == current_user:
                    total_memory += proc.info["memory_info"].rss
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return total_memory / (1024**3)  # Convert from bytes to GB

    @staticmethod
    def _get_total_memory_usage() -> float:
        """Retrieves the total RAM used by all users.

        Returns:
            float: Total RAM used in gigabytes (GB).

        Raises:
            None
        """
        total_memory = sum(proc.memory_info().rss for proc in psutil.process_iter() if proc.is_running())
        return total_memory / (1024**3)  # Convert from bytes to GB

    @staticmethod
    def _get_system_processes_memory_usage() -> float:
        """Retrieves the total RAM used by system processes, excluding users with 'thoughtful' in their names.

        Returns:
            float: Total RAM used by system processes in gigabytes (GB), rounded to 2 decimal places.

        Raises:
            None
        """
        system_memory = 0.0

        for proc in psutil.process_iter(["memory_info", "username"]):
            try:
                username = proc.info.get("username", "")
                if username and "thoughtful" in username.lower():
                    continue
                system_memory += proc.info["memory_info"].rss / (1024**3)  # Convert bytes to GB
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return round(system_memory, 2)

    @staticmethod
    def _get_available_memory() -> float:
        """Retrieves the available system RAM.

        Returns:
            float: Available RAM in gigabytes (GB).

        Raises:
            None
        """
        available_memory = psutil.virtual_memory().available
        return available_memory / (1024**3)  # Convert from bytes to GB

    @staticmethod
    def get_total_ram() -> float:
        """Retrieves the total RAM in the machine.

        Returns:
            float: Total RAM in the machine in gigabytes (GB) with two decimal places.

        Raises:
            None
        """
        total_ram = psutil.virtual_memory().total
        return round(total_ram / (1024**3), 2)  # Convert from bytes to GB
