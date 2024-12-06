import json
from typing import Any, Dict, Generator, List, cast
from unittest.mock import MagicMock, patch

import gspread  # type: ignore[import-untyped]
import pytest
from gspread.exceptions import (  # type: ignore
    APIError,
    SpreadsheetNotFound,
    WorksheetNotFound,
)
from gspread.spreadsheet import Spreadsheet  # type: ignore
from pandas import DataFrame

from strideutils.sheets_connector import GoogleSheetsClient
from strideutils.stride_config import Environment as e

# Test data types
MockCredentials = Dict[str, str]
MockSheetData = List[Dict[str, Any]]


@pytest.fixture
def mock_auth_env() -> Generator[MockCredentials, None, None]:
    """Mock environment variable for authentication"""
    mock_creds: MockCredentials = {
        "type": "service_account",
        "project_id": "test-project",
        "private_key": "test-key",
        "client_email": "test@example.com",
    }
    with patch.dict('os.environ', {e.PUBLICSHEETS_AUTH: json.dumps(mock_creds)}):
        yield mock_creds


@pytest.fixture
def sheets_client() -> Generator[GoogleSheetsClient, None, None]:
    """Provide a GoogleSheetsClient with mocked gspread client"""
    with patch('strideutils.sheets_connector.GoogleSheetsClient._get_auth_client'):
        client = GoogleSheetsClient()
        mock_client = MagicMock(spec=gspread.Client)
        client.client = mock_client
        yield client


def test_singleton_pattern() -> None:
    """Test that GoogleSheetsClient maintains singleton pattern"""
    with patch('strideutils.sheets_connector.GoogleSheetsClient._get_auth_client'):
        client1 = GoogleSheetsClient()
        client2 = GoogleSheetsClient()
        assert client1 is client2
        client1.cache_enabled = True
        assert client2.cache_enabled is True


def test_authentication_flow() -> None:
    """Test the complete authentication flow"""
    GoogleSheetsClient._instance = None

    with patch('strideutils.sheets_connector.GoogleSheetsClient._get_auth_client') as mock_auth:
        mock_auth.return_value = MagicMock(spec=gspread.Client)
        client1 = GoogleSheetsClient()
        assert mock_auth.call_count == 1
        client2 = GoogleSheetsClient()
        assert mock_auth.call_count == 1
        assert client1 is client2


def test_cache_management(sheets_client: GoogleSheetsClient) -> None:
    """Test cache functionality including edge cases"""
    sheets_client.cache_enabled = True
    mock_data = [{'A': 1, 'B': 2}]

    # Setup mock for when cache miss occurs
    mock_worksheet = MagicMock()
    mock_worksheet.get_all_records.return_value = mock_data

    assert sheets_client.client is not None
    mock_spreadsheet = MagicMock(spec=Spreadsheet)
    mock_spreadsheet.worksheet.return_value = mock_worksheet
    sheets_client.client.open_by_key = MagicMock(return_value=mock_spreadsheet)  # type: ignore[method-assign]

    # Test cache miss and population
    key = 'test_sheet_test_name'
    result1 = sheets_client.grab_sheet('test_sheet', 'test_name')
    assert sheets_client._cache[key].to_dict('records') == mock_data

    # Test cache hit
    result2 = sheets_client.grab_sheet('test_sheet', 'test_name')
    assert result1.equals(result2)
    # Verify we only called the API once
    cast(MagicMock, sheets_client.client.open_by_key).assert_called_once()


def test_error_handling(sheets_client: GoogleSheetsClient) -> None:
    """Test error propagation from gspread"""
    assert sheets_client.client is not None

    # First test - API Error
    mock_response = MagicMock()
    mock_response.text = 'API Error'
    mock_response.json.return_value = {
        'error': {
            'code': 400,
            'message': 'API Error',
            'status': 'INVALID_ARGUMENT',
        }
    }
    sheets_client.client.open_by_key = MagicMock(side_effect=APIError(mock_response))  # type: ignore[method-assign]

    with pytest.raises(APIError):
        sheets_client.grab_sheet('sheet_id', 'sheet_name')

    # Second test - WorksheetNotFound
    mock_client = MagicMock(spec=gspread.Client)
    sheets_client.client = mock_client
    mock_spreadsheet = MagicMock(spec=Spreadsheet)
    mock_client.open_by_key = MagicMock(return_value=mock_spreadsheet)  # type: ignore[method-assign]
    mock_spreadsheet.worksheet.side_effect = WorksheetNotFound
    mock_spreadsheet.add_worksheet.return_value = MagicMock()

    df = DataFrame({'A': [1]})
    sheets_client.write_sheet(df, 'sheet_id', 'sheet_name')
    mock_spreadsheet.add_worksheet.assert_called_once_with(title='sheet_name', rows=1, cols=1)


def test_worksheet_operations(sheets_client: GoogleSheetsClient) -> None:
    """Test comprehensive worksheet operations"""
    mock_spreadsheet = MagicMock(spec=Spreadsheet)
    mock_worksheet = MagicMock()

    # Setup initial state
    assert sheets_client.client is not None
    sheets_client.client.open_by_key = MagicMock(return_value=mock_spreadsheet)  # type: ignore[method-assign]
    mock_spreadsheet.worksheet.return_value = mock_worksheet

    # Test write with different data types
    test_cases: List[DataFrame] = [
        DataFrame({'A': [1, 2], 'B': [3, 4]}),
        DataFrame({'A': ['a', 'b'], 'B': ['c', 'd']}),
        DataFrame({'A': [1.5, 2.5], 'B': [True, False]}),
    ]

    for df in test_cases:
        sheets_client.write_sheet(df, 'sheet_id', 'sheet_name')
        mock_worksheet.update.assert_called()
        # Verify the data was properly formatted
        call_args = mock_worksheet.update.call_args[1]['values']
        assert len(call_args) == len(df) + 1  # +1 for headers


def test_data_handling(sheets_client: GoogleSheetsClient) -> None:
    """Test data handling capabilities"""
    mock_spreadsheet = MagicMock(spec=Spreadsheet)
    mock_worksheet = MagicMock()
    assert sheets_client.client is not None
    sheets_client.client.open_by_key = MagicMock(return_value=mock_spreadsheet)  # type: ignore[method-assign]
    mock_spreadsheet.worksheet.return_value = mock_worksheet

    test_cases: List[DataFrame] = [
        DataFrame(),  # Empty DataFrame
        DataFrame({'A': [None, 1, 2]}),  # None values
        DataFrame({'A': [1], 'B': ['text'], 'C': [True]}),  # Mixed types
    ]

    for df in test_cases:
        sheets_client.write_sheet(df, 'sheet_id', 'sheet_name')
        mock_worksheet.update.assert_called()
        call_args: List[Any] = mock_worksheet.update.call_args[1]['values']
        assert isinstance(call_args, list)


def test_sheets_grab_sheet(sheets_client: GoogleSheetsClient) -> None:
    """Test grabbing sheet data"""
    mock_worksheet = MagicMock()
    mock_data: List[Dict[str, int]] = [{'A': 1, 'B': 2}, {'A': 3, 'B': 4}]
    mock_worksheet.get_all_records.return_value = mock_data

    mock_spreadsheet = MagicMock(spec=Spreadsheet)
    mock_spreadsheet.worksheet.return_value = mock_worksheet
    assert sheets_client.client is not None
    sheets_client.client.open_by_key = MagicMock(return_value=mock_spreadsheet)  # type: ignore[method-assign]

    result = sheets_client.grab_sheet('sheet_id', 'sheet_name')

    cast(MagicMock, sheets_client.client.open_by_key).assert_called_once_with('sheet_id')
    mock_spreadsheet.worksheet.assert_called_once_with('sheet_name')
    assert isinstance(result, DataFrame)
    assert result.to_dict('records') == mock_data


def test_sheets_grab_sheet_not_found(sheets_client: GoogleSheetsClient) -> None:
    """Test handling of non-existent spreadsheet"""
    assert sheets_client.client is not None
    sheets_client.client.open_by_key = MagicMock(side_effect=SpreadsheetNotFound)  # type: ignore[method-assign]

    with pytest.raises(SpreadsheetNotFound):
        sheets_client.grab_sheet('nonexistent_id', 'sheet_name')


def test_sheets_grab_sheet_with_cache(sheets_client: GoogleSheetsClient) -> None:
    """Test sheet data retrieval with caching"""
    assert sheets_client.client is not None
    sheets_client.cache_enabled = True
    cached_data = DataFrame({'A': [1, 3], 'B': [2, 4]})
    sheets_client._cache['sheet_id_sheet_name'] = cached_data

    results = sheets_client.grab_sheet('sheet_id', 'sheet_name')

    assert isinstance(results, DataFrame)
    assert results.to_dict('records') == [{'A': 1, 'B': 2}, {'A': 3, 'B': 4}]
    cast(MagicMock, sheets_client.client.open_by_key).assert_not_called()


def test_sheets_write_sheet(sheets_client: GoogleSheetsClient) -> None:
    """Test writing data to sheet"""
    mock_worksheet = MagicMock()
    mock_spreadsheet = MagicMock(spec=Spreadsheet)
    mock_spreadsheet.worksheet.return_value = mock_worksheet
    assert sheets_client.client is not None
    sheets_client.client.open_by_key = MagicMock(return_value=mock_spreadsheet)  # type: ignore[method-assign]

    test_data = DataFrame({'A': [1, 3], 'B': [2, 4]})
    sheets_client.write_sheet(test_data, 'sheet_id', 'sheet_name')

    cast(MagicMock, sheets_client.client.open_by_key).assert_called_once_with('sheet_id')
    mock_spreadsheet.worksheet.assert_called_once_with('sheet_name')
    mock_worksheet.update.assert_called_once()


def test_sheets_write_sheet_new_worksheet(sheets_client: GoogleSheetsClient) -> None:
    """Test writing data to a new worksheet"""
    mock_spreadsheet = MagicMock(spec=Spreadsheet)
    mock_spreadsheet.worksheet.side_effect = WorksheetNotFound
    assert sheets_client.client is not None
    sheets_client.client.open_by_key = MagicMock(return_value=mock_spreadsheet)  # type: ignore[method-assign]

    test_data = DataFrame({'A': [1, 3], 'B': [2, 4]})
    sheets_client.write_sheet(test_data, 'sheet_id', 'new_sheet')

    mock_spreadsheet.add_worksheet.assert_called_once_with(title='new_sheet', rows=1, cols=1)


def test_sheets_reorder_sheet(sheets_client: GoogleSheetsClient) -> None:
    """Test reordering worksheets"""
    mock_sheets: List[MagicMock] = [
        MagicMock(title='Sheet1', id=1),
        MagicMock(title='Sheet2', id=2),
        MagicMock(title='Sheet3', id=3),
    ]

    mock_spreadsheet = MagicMock(spec=Spreadsheet)
    mock_spreadsheet.worksheets.return_value = mock_sheets
    assert sheets_client.client is not None
    sheets_client.client.open_by_key = MagicMock(return_value=mock_spreadsheet)  # type: ignore[method-assign]

    sheets_client.reorder_sheet('sheet_id', 'Sheet2', 0)

    mock_spreadsheet.batch_update.assert_called_once()
    call_args: Dict[str, List[Dict[str, Any]]] = mock_spreadsheet.batch_update.call_args[0][0]
    assert call_args['requests'][0]['updateSheetProperties']['properties']['index'] == 1
    assert call_args['requests'][0]['updateSheetProperties']['properties']['sheetId'] == 2


def test_sheets_reorder_sheet_invalid_name(sheets_client: GoogleSheetsClient) -> None:
    """Test reordering with invalid sheet name"""
    mock_sheets: List[MagicMock] = [
        MagicMock(title='Sheet1', id=1),
        MagicMock(title='Sheet2', id=2),
    ]
    mock_spreadsheet = MagicMock(spec=Spreadsheet)
    mock_spreadsheet.worksheets.return_value = mock_sheets
    assert sheets_client.client is not None
    sheets_client.client.open_by_key = MagicMock(return_value=mock_spreadsheet)  # type: ignore[method-assign]

    with pytest.raises(ValueError, match="Sheet3 not found"):
        sheets_client.reorder_sheet('sheet_id', 'Sheet3', 0)


def test_sheets_get_sheet_names(sheets_client: GoogleSheetsClient) -> None:
    """Test getting list of sheet names"""
    mock_sheets: List[MagicMock] = [
        MagicMock(title='Sheet1'),
        MagicMock(title='Sheet2'),
        MagicMock(title='Sheet3'),
    ]
    mock_spreadsheet = MagicMock(spec=Spreadsheet)
    mock_spreadsheet.worksheets.return_value = mock_sheets
    assert sheets_client.client is not None
    sheets_client.client.open_by_key = MagicMock(return_value=mock_spreadsheet)  # type: ignore[method-assign]

    result = sheets_client.get_sheet_names('sheet_id')

    assert result == ['Sheet1', 'Sheet2', 'Sheet3']


def test_sheets_get_sheet_names_empty(sheets_client: GoogleSheetsClient) -> None:
    """Test getting sheet names from empty spreadsheet"""
    mock_spreadsheet = MagicMock(spec=Spreadsheet)
    mock_spreadsheet.worksheets.return_value = []
    assert sheets_client.client is not None
    sheets_client.client.open_by_key = MagicMock(return_value=mock_spreadsheet)  # type: ignore[method-assign]

    result = sheets_client.get_sheet_names('sheet_id')

    assert result == []
