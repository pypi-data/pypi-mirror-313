"""
Google Sheets Connector for Stride Utils

This module provides a singleton client for interacting with Google Sheets
in the Stride project. It uses the configuration from stride_config to authenticate
and access Google Sheets. The module offers methods to read, write, and manipulate
Google Sheets data.

By default, any Google Sheet that the email
publicsheets@stride-nodes.iam.gserviceaccount.com can access will be readable by this API.
"""

import json
import warnings
from typing import Dict, List, Tuple

import gspread  # type: ignore
import pandas as pd
from google.oauth2 import service_account  # type: ignore
from gspread.exceptions import WorksheetNotFound  # type: ignore
from gspread.http_client import BackOffHTTPClient  # type: ignore

from strideutils.stride_config import Environment as e
from strideutils.stride_config import get_env_or_raise

# These are default scopes that we hope to access
SCOPES: Tuple[str, str, str] = (
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
)


class GoogleSheetsClient:
    """Singleton client used to interact with Google Sheets."""

    _instance = None
    client: gspread.Client = None  # type: ignore
    cache_enabled: bool = False
    _cache: Dict[str, pd.DataFrame] = {}

    def __new__(cls) -> 'GoogleSheetsClient':
        if cls._instance is None:
            cls._instance = super(GoogleSheetsClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, cache_enabled: bool = False) -> None:
        """
        Initialize the Google Sheets client.

        Args:
             cache_enabled:  Whether to cache sheet data in memory.
        """
        if self.client is None:
            self.client = self._get_auth_client()
            self.cache_enabled = cache_enabled
            self._cache = {}

    @staticmethod
    def _get_auth_client() -> gspread.Client:
        """
        Creates and returns an authenticated gspread client.

        Returns:
            An authenticated gspread client
        """
        auth_dict_contents = get_env_or_raise(e.PUBLICSHEETS_AUTH)
        auth_dict = json.loads(auth_dict_contents, strict=False)

        creds = service_account.Credentials.from_service_account_info(auth_dict, scopes=SCOPES)
        return gspread.authorize(creds, http_client=BackOffHTTPClient)

    def grab_sheet(
        self,
        sheet_id: str,
        sheet_name: str,
        columns_labeled: bool = True,
    ) -> pd.DataFrame:
        """
        Retrieves the contents of a specified Google Sheet as a Pandas DataFrame.

        Args:
            sheet_id: The ID of the Sheet (found in the URL)
            sheet_name: The name of the worksheet within the Sheet
            columns_labeled: If True, uses the first row as column names

        Returns:
            DataFrame containing the sheet's data

        Raises:
            gspread.exceptions.WorksheetNotFound: If the worksheet doesn't exist
            gspread.exceptions.APIError: If there's an error accessing the sheet
        """
        cache_key = f"{sheet_id}_{sheet_name}"
        if self.cache_enabled and cache_key in self._cache:
            return self._cache[cache_key]

        spreadsheet = self.client.open_by_key(sheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)

        data = worksheet.get_all_records() if columns_labeled else worksheet.get_all_values()
        df = pd.DataFrame(data)

        if self.cache_enabled:
            self._cache[cache_key] = df

        return df

    def write_sheet(
        self,
        df: pd.DataFrame,
        sheet_id: str,
        sheet_name: str,
    ) -> None:
        """
        Writes a Pandas DataFrame to a specified Google Sheet.

        Args:
            df: The DataFrame to write to the sheet
            sheet_id: The ID of the Sheet (found in the URL)
            sheet_name: The name of the worksheet to write to

        Raises:
            gspread.exceptions.APIError: If there's an error accessing the sheet
        """
        # Fetch the worksheet if it exists, otherwise create a new worksheet.
        spreadsheet = self.client.open_by_key(sheet_id)
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1, cols=1)

        # Build the list of values to add.
        df = df.fillna('')
        columns = [df.columns.values.tolist()]
        rows = df.values.tolist()
        range_name = f"A1:ZZ{len(df)+1}"

        # Write the new values with update (which will override an existing sheet).
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            worksheet.update(values=columns + rows, range_name=range_name)

    def reorder_sheet(
        self,
        sheet_id: str,
        sheet_name: str,
        new_location: int = 0,
    ) -> None:
        """
        Moves a worksheet to a new position within a Google Sheet.

        Args:
            sheet_id: The ID of the Sheet (found in the URL)
            sheet_name: The name of the worksheet to move
            new_location: The new index (0-based) for the worksheet

        Raises:
            ValueError: If the sheet_name is not found or new_location is invalid
            gspread.exceptions.APIError: If there's an error accessing the sheet
        """
        spreadsheet = self.client.open_by_key(sheet_id)
        all_sheets = spreadsheet.worksheets()
        current_order = [sheet.title for sheet in all_sheets]

        if sheet_name not in current_order:
            raise ValueError(f'{sheet_name} not found. Current sheets: {current_order}')

        if (new_location > len(current_order)) or (new_location < 0):
            raise ValueError(f'New location must be between 0 and {len(current_order)}')

        # Get the desired new order
        location_of_sheet = current_order.index(sheet_name)
        location_of_next_sheet = location_of_sheet + 1
        new_worksheets = all_sheets[:location_of_sheet] + all_sheets[location_of_next_sheet:]
        new_worksheets.insert(new_location, all_sheets[location_of_sheet])

        # Update the sheet
        requests = []
        for i, sheet in enumerate(new_worksheets):
            requests.append(
                {"updateSheetProperties": {"properties": {"index": i + 1, "sheetId": sheet.id}, "fields": "index"}}
            )
        spreadsheet.batch_update({"requests": requests})

    def get_sheet_names(self, sheet_id: str) -> List[str]:
        """
        Retrieves the names of all worksheets in a Google Sheet.

        Args:
            sheet_id: The ID of the Sheet (found in the URL)

        Returns:
            List of worksheet names in the specified Google Sheet

        Raises:
            RuntimeError: If the client is not initialized
            gspread.exceptions.APIError: If there's an error accessing the sheet
        """
        spreadsheet = self.client.open_by_key(sheet_id)
        all_sheets = spreadsheet.worksheets()
        return [sheet.title for sheet in all_sheets]
