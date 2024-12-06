"""Deal with disk related stuffs."""
import psutil


class DiskManager:
    """A class to manage and retrieve disk space information."""

    @staticmethod
    def get_disk_stats() -> tuple[float, float, float]:
        """Retrieves disk space statistics for the system.

        Returns:
            tuple: A tuple containing:
                - Total disk space in gigabytes (GB).
                - Available disk space in gigabytes (GB).
                - Used disk space in gigabytes (GB).

        Raises:
            None
        """
        total, _, free, _ = psutil.disk_usage("/")
        gb_conversion = 1024**3
        total_gb = round(total / gb_conversion, 2)
        free_gb = round(free / gb_conversion, 2)
        used_gb = round(total_gb - free_gb, 2)

        return total_gb, free_gb, used_gb
