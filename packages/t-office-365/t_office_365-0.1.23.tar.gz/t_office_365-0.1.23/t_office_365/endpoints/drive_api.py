"""This module contains the endpoints for the drive api."""


def folder_id_endpoint(drive_id, folder_path) -> str:
    """Get the endpoint to get the folder id."""
    return f"/drives/{drive_id}/root:/{folder_path}"


def folder_items_endpoint(drive_id, folder_id) -> str:
    """Get the endpoint to get the items of a folder."""
    return f"/drives/{drive_id}/items/{folder_id}/children"


def file_content_endpoint(drive_id, file_id) -> str:
    """Get the endpoint to get the content of a file."""
    return f"/drives/{drive_id}/items/{file_id}/content"


def file_info_endpoint(drive_id, file_path) -> str:
    """Get the endpoint to get the info of a file."""
    return f"/drives/{drive_id}/root:/{file_path}"


def file_upload_session_endpoint(drive_id, folder_id, file_url) -> str:
    """Get the endpoint to create an upload session."""
    return f"/drives/{drive_id}/items/{folder_id}:/{file_url}:/createUploadSession"


def file_content_by_url_endpoint(drive_id, folder_id, file_url) -> str:
    """Get the endpoint to get the content of a file by url."""
    return f"/drives/{drive_id}/items/{folder_id}:/{file_url}:/content"


def file_id_endpoint(drive_id, file_id):
    """Get the endpoint to get the file id."""
    return f"/drives/{drive_id}/items/{file_id}"


def get_drive_id_endpoint(site_id):
    """Get the drive id endpoint."""
    return f"/sites/{site_id}/drive"
