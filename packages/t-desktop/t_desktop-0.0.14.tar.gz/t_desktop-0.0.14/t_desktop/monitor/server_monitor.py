"""Monitor Server."""
import datetime
import os
import threading
import time
from openpyxl import load_workbook
import pytz
import atexit
from typing import Any, Optional
from t_desktop.utils.logger import logger
from t_desktop.monitor.workitems import rc_run_link, empower_url, empower_url_text, OUTPUT_FOLDER
from t_desktop.monitor.managers.cpu_manager import CPUManager
from t_desktop.monitor.managers.disk_manager import DiskManager
from t_desktop.monitor.managers.memory_manager import MemoryManager
from t_desktop.monitor.spreadhseet.g_sheets import GSheets
from google.oauth2.service_account import Credentials


class ServerMonitor:
    """A class to manage and monitor system performance in a separate thread."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of the class is created (Singleton Pattern)."""
        if cls._instance is None:
            cls._instance = super(ServerMonitor, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        process_name: str,
        hostname: str,
        interval: int = 60,
        export_path: Optional[str] = OUTPUT_FOLDER,
    ) -> None:
        """Initialize the server manager with configurations.

        Args:
            process_name (str): The process name to monitor.
            hostname (str): The hostname for the server.
            spreadsheet_id (str, optional): The ID of the Google Spreadsheet.
            spreadsheet_tab (str, optional): The tab name or index within the spreadsheet.
            google_sheet_credentials (list, optional): Credentials Object required for Google Sheets access.
            interval (int, optional): Interval in seconds to tick the stats. Defaults to 60.
            export_path (str, optional): Path to export results locally. Defaults to output.
            if export_path is None or empty, it will not be locally exported.
        """
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True
        self.process_name = process_name
        self._hostname = hostname
        self.interval = interval
        self.export_path = export_path

        self._initialize_managers()
        self._initialize_metrics()
        self._spreadsheet_id = None
        self._spreadsheet_tab = None
        self._setup_urls()
        self.g_sheets = None
        atexit.register(self.stop)

    def _initialize_managers(self) -> None:
        """Initialize resource management classes."""
        self._memory_manager = MemoryManager()
        self._cpu_manager = CPUManager()
        self._disk_manager = DiskManager()

    def _initialize_metrics(self) -> None:
        """Initialize monitoring metrics."""
        self._running = False
        self._thread = None
        self._cpu_usage = []
        self._memory_usage = []
        self._peak_memory_usage = 0.0
        self._peak_cpu_usage = 0.0
        self._system_cpu_usage = []
        self._peak_system_cpu_usage = 0.0
        self._all_users_memory_usage = []
        self._system_process_memory = []
        self._user_cpu_usage = []
        self._start_time = None

    def _setup_urls(self) -> None:
        """Setup URLs for monitoring links."""
        self._empower_url = f'=HYPERLINK("{empower_url}", "{empower_url_text}")'
        self._rc_run_link = f'=HYPERLINK("{rc_run_link}", "RC RUN LINK")'
        self._env = "DEV" if "dev" in empower_url else "PROD"

    def start(self) -> None:
        """Start the monitoring thread."""
        if self._running:
            logger.warning("ServerManager is already running.")
            return
        logger.info("Starting Server Monitor")

        self._running = True
        self._reset_metrics()
        self._thread = threading.Thread(target=self._monitor)
        self._thread.start()

    def stop(self) -> None:
        """Stop the monitoring thread and export results."""
        if not self._running:
            logger.warning("ServerManager is not running.")
            return
        logger.info("Stopping Server Monitor")

        self._running = False
        self._thread.join()

        row_data = self._build_row()
        self._export_results(row_data)

    def export_results(self):
        """Export results without stopping the monitor."""
        row_data = self._build_row()
        self._export_results(row_data)

    def _reset_metrics(self) -> None:
        """Reset monitoring metrics."""
        mst_tz = pytz.timezone("America/Denver")
        now = datetime.datetime.now(mst_tz)
        self._start_time = now.strftime("%H:%M:%S")
        self._cpu_usage.clear()
        self._memory_usage.clear()
        self._all_users_memory_usage.clear()
        self._peak_memory_usage = 0.0
        self._peak_cpu_usage = 0.0
        self._system_cpu_usage.clear()
        self._system_process_memory.clear()
        self._user_cpu_usage.clear()

    def _monitor(self) -> None:
        """Monitor system performance metrics."""
        previous_cpu_usage = None
        previous_memory_usage = None

        while self._running:
            self._collect_metrics(previous_cpu_usage, previous_memory_usage)
            time.sleep(self.interval)

    def _collect_metrics(self, previous_cpu_usage: Optional[float], previous_memory_usage: Optional[float]) -> None:
        """Collect and analyze metrics for CPU and memory usage.

        Args:
            previous_cpu_usage (Optional[float]): The CPU usage from the previous monitoring interval.
            previous_memory_usage (Optional[float]): The memory usage from the previous monitoring interval.
        """
        overall_cpu_usage, system_cpu_usage, user_cpu_usage = self._cpu_manager.get_cpu_stats()
        memory_stats = self._memory_manager.get_memory_stats()

        self._analyze_variation("CPU", previous_cpu_usage, overall_cpu_usage, 20)
        self._analyze_variation("Memory", previous_memory_usage, memory_stats[0], 20)

        self._update_metrics(overall_cpu_usage, system_cpu_usage, user_cpu_usage, memory_stats)
        previous_cpu_usage, previous_memory_usage = overall_cpu_usage, memory_stats[0]

    def _analyze_variation(
        self, metric_name: str, previous_value: Optional[float], current_value: float, threshold: float
    ) -> None:
        """Log warnings if a metric's variation exceeds a specified threshold.

        Args:
            metric_name (str): The name of the metric being analyzed (e.g., "CPU", "Memory").
            previous_value (Optional[float]): The previous value of the metric.
            current_value (float): The current value of the metric.
            threshold (float): The threshold percentage for triggering a warning.
        """
        if previous_value is not None:
            increase = current_value - previous_value
            if increase > threshold:
                logger.warning(
                    f"{metric_name} usage increased by more than {threshold}%. "
                    f"Previous: {previous_value}%, Current: {current_value}%"
                )

    def _update_metrics(
        self,
        overall_cpu_usage: float,
        system_cpu_usage: float,
        user_cpu_usage: float,
        memory_stats: tuple[float, float, float],
    ) -> None:
        """Update monitoring metrics and track peaks.

        Args:
            overall_cpu_usage (float): The total CPU usage percentage.
            system_cpu_usage (float): The system CPU usage percentage.
            user_cpu_usage (float): The user CPU usage percentage.
            memory_stats (Tuple[float, float, float]): A tuple containing:
                - User memory usage (in GB).
                - Memory usage by all users (in GB).
                - System memory usage (in GB).
        """
        self._cpu_usage.append(overall_cpu_usage)
        self._system_cpu_usage.append(system_cpu_usage)
        self._user_cpu_usage.append(user_cpu_usage)

        current_user_memory_usage = memory_stats[0]
        all_users_memory_usage = memory_stats[1]

        self._memory_usage.append(current_user_memory_usage)
        self._all_users_memory_usage.append(all_users_memory_usage)
        self._system_process_memory.append(memory_stats[2])

        self._peak_memory_usage = max(self._peak_memory_usage, current_user_memory_usage)
        self._peak_cpu_usage = max(self._peak_cpu_usage, overall_cpu_usage)

    def _export_results(self, row_data: list[Any]) -> None:
        """Export collected results to a spreadsheet.

        Args:
            row_data (List[Any]): The data to export as a row.
        """
        if self.export_path:
            self._export_to_local_file(row_data)
        if self.g_sheets:
            self._upload_to_google_sheets(row_data)

    def _upload_to_google_sheets(self, row_data: list[Any]) -> None:
        """Upload results to Google Sheets.

        Args:
            row_data (List[Any]): The data to export as a row.
        """
        logger.info("Uploading results to spreadsheet")
        self.g_sheets.append_row(self._spreadsheet_id, self._spreadsheet_tab, row_data)

    def _export_to_local_file(self, row_data: list[Any]) -> None:
        """Export results to a local file.

        Args:
            row_data (List[Any]): The data to export as a row.
        """
        try:
            export_path = self._determine_export_path()
            workbook = load_workbook(self._template_path())
            sheet = workbook.active
            sheet.append(row_data)
            workbook.save(export_path)
            logger.info("Results exported to %s", export_path)
        except Exception as e:
            logger.error("Failed to append to and export spreadsheet: %s", e)

    def setup_google_sheets(
        self,
        credentials: Credentials,
        spreadsheet_id: str = None,
        spreadsheet_tab: str = None,
    ) -> None:
        """Setup the google sheets with the given credentials.

        Args:
            credentials (Credentials): The google sheets credentials object.
            spreadsheet_id (str): spreadsheet_id
            spreadsheet_tab (str): spreadsheet_tab
        """
        self._spreadsheet_id = spreadsheet_id
        self._spreadsheet_tab = spreadsheet_tab
        self.g_sheets = GSheets(credentials=credentials)

    def _determine_export_path(self) -> str:
        """Determine export path for the spreadsheet.

        If `self.export_path` is not specified, use the 'output' folder in the
        project root and create it if necessary.

        Returns:
            str: The full export path for the spreadsheet.
        """
        os.makedirs(self.export_path, exist_ok=True)
        return os.path.join(self.export_path, "PerformanceMonitor.xlsx")

    def _template_path(self) -> str:
        """Get path to the local spreadsheet template."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, "assets", "Template.xlsx")

    def _build_row(self) -> list:
        """Build the row with the result values."""
        average_cpu_usage = sum(self._cpu_usage) / len(self._cpu_usage) if self._cpu_usage else 0
        average_memory_usage = sum(self._memory_usage) / len(self._memory_usage) if self._memory_usage else 0
        average_all_users_memory_usage = (
            sum(self._all_users_memory_usage) / len(self._all_users_memory_usage) if self._all_users_memory_usage else 0
        )
        average_system_memory_usage = (
            sum(self._system_process_memory) / len(self._system_process_memory) if self._system_process_memory else 0
        )
        average_system_cpu_usage = (
            sum(self._system_cpu_usage) / len(self._system_cpu_usage) if self._system_cpu_usage else 0
        )
        average_user_cpu_usage = sum(self._user_cpu_usage) / len(self._user_cpu_usage) if self._user_cpu_usage else 0
        disk_status = self._disk_manager.get_disk_stats()

        total_ram = self._memory_manager.get_total_ram()

        # Calculating percentages
        user_memory_usage_percent = (average_memory_usage / total_ram) * 100 if total_ram else 0
        all_users_memory_usage_percent = (average_all_users_memory_usage / total_ram) * 100 if total_ram else 0
        system_memory_usage_percent = (average_system_memory_usage / total_ram) * 100 if total_ram else 0
        peak_memory_usage_percent = (self._peak_memory_usage / total_ram) * 100 if total_ram else 0

        mst_tz = pytz.timezone("America/Denver")
        now = datetime.datetime.now(mst_tz)

        # Format the date and time separately
        date = now.strftime("%Y-%m-%d")
        end_time = now.strftime("%H:%M:%S")

        # Create row_data with separate date and time
        return [
            date,  # Date
            self._start_time,  # Start Time
            end_time,  # End Time
            self._env,  # Empower ENV
            self._empower_url,  # Empower Run ID
            self._rc_run_link,  # RC Step Run Link
            self.process_name,  # RC Process Name
            self._hostname,  # Server Name
            os.getenv("USERNAME"),  # Username
            f"{average_user_cpu_usage:.2f}",  # [User] AVG CPU Usage
            f"{average_cpu_usage:.2f}",  # [Total] AVG CPU Usage
            f"{self._peak_cpu_usage:.2f}",  # [User] Peak CPU Usage
            f"{average_system_cpu_usage:.2f}",  # System CPU Usage
            f"{average_memory_usage:.2f}",  # [User] Avg Ram Usage GB
            f"{user_memory_usage_percent:.2f}%",  # [User] Avg Ram Usage %
            f"{self._peak_memory_usage:.2f}",  # [User] Peak Ram Usage GB
            f"{peak_memory_usage_percent:.2f}%",  # [User] Peak Ram Usage %
            f"{average_all_users_memory_usage:.2f}",  # [All Users] Avg Ram Usage GB
            f"{all_users_memory_usage_percent:.2f}%",  # [All Users] Avg Ram Usage %
            f"{average_system_memory_usage:.2f}",  # [System] Avg Ram Usage GB
            f"{system_memory_usage_percent:.2f}%",  # [System] Avg Ram Usage %
            f"{total_ram:.2f}",  # Total RAM GB
            f"{disk_status[0]:.2f}",  # Total Disk Space
            f"{disk_status[1]:.2f}",  # Available Disk Space
            f"{disk_status[2]:.2f}",  # Used Disk Space
        ]
