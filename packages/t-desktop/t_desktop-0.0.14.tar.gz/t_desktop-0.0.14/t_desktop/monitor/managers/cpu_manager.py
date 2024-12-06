"""Deals with CPU related stuffs."""
import psutil


class CPUManager:
    """A class to manage and retrieve CPU usage information."""

    @staticmethod
    def get_cpu_stats() -> tuple:
        """Retrieves the overall current CPU usage percentage and CPU usage by system processes.

        Returns:
            tuple: A tuple containing (overall CPU usage, system process CPU usage).

        Raises:
            None
        """
        return CPUManager._get_cpu_usage()

    @staticmethod
    def _get_cpu_usage() -> tuple:
        """Retrieves the overall current CPU usage percentage.

        Returns:
            tuple: (overall CPU usage percentage, CPU usage by system processes,
                    CPU usage by the current user).

        Raises:
            None
        """
        overall_cpu = psutil.cpu_percent(interval=1)
        cpu_times = psutil.cpu_times_percent(interval=1)
        system_cpu = cpu_times.system
        user_cpu = cpu_times.user

        return overall_cpu, system_cpu, user_cpu
