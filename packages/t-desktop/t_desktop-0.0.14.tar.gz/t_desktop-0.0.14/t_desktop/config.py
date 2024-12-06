import os
import platform
import socket
from pathlib import Path

IS_WINDOWS_OS = platform.system() == "Windows"


class Config:
    """Static class container for all variables."""

    class DIRECTORIES:
        """Container for any directories required for this library.

        Folders will be created automatically
        """

        OUTPUT = Path().cwd() / "output"
        SCREENSHOTS = os.path.join(OUTPUT, "screenshots")

    if IS_WINDOWS_OS:
        username = os.getlogin()
        hostname = socket.gethostname()
    else:
        username = ""
        hostname = ""


CONFIG = Config()
