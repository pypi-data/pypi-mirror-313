"""This module contains the endpoints for the workbook API."""


def worksheets(drive_id, file_id) -> str:
    """Get worksheets endpoint.

    Returns:
        str: worksheets endpoint path
    """
    return f"/drives/{drive_id}/items/{file_id}/workbook/worksheets"


def get_row_endpoint(
    drive_id, file_id, sheet_name, start_row: int = 1, end_row: int = 100, start_column="A", end_column="Z"
) -> str:
    """Get excel row endpoint.

    Returns:
        str: excel row endpoint path
    """
    return (
        f"/drives/{drive_id}/items/{file_id}/workbook/worksheets/"
        f"{sheet_name}/range(address='{start_column}{start_row}:{end_column}{end_row}')"
    )


def get_cell_endpoint(drive_id, file_id, sheet_name, row, column) -> str:
    """Get excel cell endpoint.

    Returns:
        str: excel cell endpoint path
    """
    return f"/drives/{drive_id}/items/{file_id}/workbook/worksheets/{sheet_name}/cell(row={row}, column={column})"


def get_used_range(drive_id, file_id, sheet_name):
    """Get the used range endpoint."""
    return f"/drives/{drive_id}/items/{file_id}/workbook/worksheets/{sheet_name}/usedRange"
