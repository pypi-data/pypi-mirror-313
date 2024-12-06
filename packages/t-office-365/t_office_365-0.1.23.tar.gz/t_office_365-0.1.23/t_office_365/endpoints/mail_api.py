"""This module contains the Outlook class for interacting with Outlook email."""


def mail_child_folders_endpoint(folder_id) -> str:
    """Get the endpoint to get the child folders of a mail folder."""
    return f"/mailFolders/{folder_id}/childFolders"


@property
def get_messages_from_folder_endpoint(folder_id):
    """Get the endpoint to get the messages from a mail folder."""
    return f"/mailFolders/{folder_id}/messages"
