"""Module to deal with google sheets."""

from json.decoder import JSONDecodeError
from typing import Any

import gspread
from gspread.exceptions import APIError
from retry import retry

from t_desktop.utils.logger import logger


class GSheets:
    """Class to deal with Google sheets rows."""

    def __init__(self, credentials: Any):
        """Initializes the Mapping class."""
        self.client = gspread.authorize(credentials)

    @retry(
        exceptions=(APIError, JSONDecodeError),
        tries=10,
        delay=5,
        backoff=2,
        max_delay=64,
        jitter=(0, 20),
        logger=logger,
    )
    def append_row(self, spreadsheet_id: str, tab: str, row: list) -> None:
        """Appends a row to the end of the specified worksheet.

        Args:
            tab (Any): The tab configuration to access the worksheet.
            row (list): The row data to append.

        Returns:
            None

        Raises:
            ValueError: If the row data is not in list format.
        """
        if not isinstance(row, list):
            raise ValueError("Row data must be provided as a list.")

        spreadsheet = self.client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.get_worksheet_by_id(tab)

        worksheet.append_row(row, value_input_option="USER_ENTERED")
        logger.info(f"Row appended to {tab}: {row}")
