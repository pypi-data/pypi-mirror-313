"""Utility functions."""
import json
import os
import re
from json import JSONDecodeError
from typing import List
from venv import logger

from t_office_365.exceptions import (
    AssetLockedError,
    AssetNotFoundError,
    AuthenticationGraphError,
    BadRequestError,
    InvalidJSONError,
    ServiceUnavailableError,
    UnexpectedError,
)
from t_office_365.models import Cell


def get_validated_target_folder(target_folder: str):
    """Check if the given path exists as a directory.

    :param:
        - target_folder (str): The path to be checked.

    :raise:
        AssetNotFoundError: If the path does not exist as a directory.
    """
    if not os.path.isdir(target_folder):
        raise AssetNotFoundError(f"No such directory: '{target_folder}'")

    return target_folder


def check_result(result, asset: str = "") -> None:
    """Checks the HTTP status code of a request result and raises specific exceptions based on common error codes.

    :param:
    - result: The result of an HTTP request (response object).
    - asset: Optional. The asset associated with the request, used for error messages.

    :raises:
     - AuthenticationGraphError: If the status code is 401.
     - AssetLockedError: If the status code is 423, with a message indicating the asset is locked.
     - BadRequestError: If the status code is 400, with a message indicating processing failure for the asset.
     - AssetNotFoundError: If the status code is 404, with a message indicating the asset was not found.
     - ServiceUnavailableError: If the status code is 503.
     - UnexpectedError: If the status code is not 200, with a generic error message.
     - InvalidJSONError: If the response is required to be JSON but is invalid.
    """
    status_code = result.status_code
    error = None

    if "application/json" in result.headers.get("Content-Type", ""):
        try:
            error = result.json().get("error", None)
        except JSONDecodeError:
            try:
                fixed_content = re.sub(r"\\\\", r"\\", result.text)
                result_json = json.loads(fixed_content)
                error = result_json.get("error", None)
            except JSONDecodeError:
                logger.error("Failed to decode JSON response even after fixing.")
                raise InvalidJSONError("Invalid JSON response received for asset: {}".format(asset))
    else:
        error = None

    error_message = error.get("message", result.text) if error else result.text

    success_codes = [200, 201, 204]
    error_details = f"\nError details: {error_message}" if error_message else ""

    status_code_exceptions_map = {
        401: AuthenticationGraphError(error_message),
        423: AssetLockedError(f"Asset '{asset}' locked!" + error_details),
        400: BadRequestError(f"Unable to process: '{asset}'" + error_details),
        404: AssetNotFoundError(f"Asset '{asset}' not found!" + error_details),
        503: ServiceUnavailableError(error_message),
    }
    ex = status_code_exceptions_map.get(status_code, None)
    if ex:
        raise ex
    if status_code not in success_codes:
        raise UnexpectedError(
            f'An unexpected error while processing asset "{asset}". (Status code {status_code})' + error_details
        )


def json_to_cells(data) -> List[List[Cell]]:
    """Convert JSON data to a list of rows and cells."""
    rows_list = []
    for index in range(1, len(data.get("values", []))):
        cell_list = []
        row_data = zip(data.get("values", [])[0], data.get("numberFormat", [])[index], data["values"][index])
        for i, row in enumerate(row_data):
            column, data_type, value = row
            cell_data = Cell(column_name=column, data_type=data_type, value=value, row_num=index, col_num=i + 1)
            cell_list.append(cell_data)
        rows_list.append(cell_list)
    return rows_list


def json_to_row_cells(data, headers, row_num) -> List[Cell]:
    """Convert JSON data to a list of cells for a single row."""
    cells_list = []
    cell_data = zip(headers.get("values", [])[0], data.get("numberFormat", [])[0], data.get("values", [])[0])
    for i, cell in enumerate(cell_data):
        column, cell_type, cell_value = cell
        cells_list.append(
            Cell(column_name=column, data_type=cell_type, value=cell_value, row_num=row_num, col_num=i + 1)
        )
    return cells_list
