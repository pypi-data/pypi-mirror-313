"""This module contains the Outlook class for interacting with Outlook email."""

import base64
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Union

from O365 import Account, Message
from O365.mailbox import Folder
from O365.message import MessageAttachment
from O365.utils import Query

from t_office_365.core import Core
from t_office_365.exceptions import AssetNotFoundError


@dataclass
class QueryMap:
    """Data class for mapping query attributes and values."""

    def __init__(self, key: str, value: str or bool, method: str) -> None:
        """Initialize QueryMap with key, value, and method.

        :param key: Key to map to in query.
        :param value: Value to filter on.
        :param method: Method to apply for filtering.
        """
        self.key = key
        self.value = value
        self.method = method


class Outlook(Core):
    """A class for interacting with Outlook email."""

    def __init__(self, account: Account) -> None:
        """Initialize the Outlook interface with the specified account.

        :param:
            account (Account): The account used to authenticate with Outlook.
        """
        super().__init__(account)

    @property
    def mailbox(self):
        """Get the mailbox of the account."""
        return self.account.mailbox()

    @property
    def inbox_folder(self):
        """Get the inbox folder of the mailbox."""
        return self.mailbox.inbox_folder()

    def get_emails(
        self,
        folder: Union[str, Folder] = "Inbox",
        subject: str = "",
        from_email: str = "",
        to: str = "",
        after: datetime = None,
        before: datetime = None,
        unread: bool = None,
        has_attachments: bool = None,
        pattern_by_subject: re.Pattern | str = None,
        pattern_by_attachment: re.Pattern | str = None,
    ) -> List[Message]:
        """Retrieve emails.

        :param:
            folder (Union[str, Folder], optional): Folder path or object from which to retrieve emails.
            subject (str, optional): Subject filter for emails.
            from_email (str, optional): Sender email filter for emails.
            to (str, optional): Recipient email filter for emails.
            after (datetime, optional): Filter for emails received after this datetime.
            before (datetime, optional): Filter for emails received before this datetime.
            unread (bool, optional): Filter for unread emails.
            has_attachments (bool, optional): Filter for emails with attachments.
            pattern_by_subject (str, optional): Filter for emails matching a pattern in subject.
            pattern_by_attachment (str, optional): Filter for emails matching a pattern in attachments.

        :return: List of messages retrieved.
        """
        q_args = []
        if unread is not None:
            q_args.append(QueryMap(key="isRead", value=not unread, method="equals"))
        if has_attachments is not None:
            q_args.append(QueryMap(key="has_attachments", value=has_attachments, method="equals"))
        if subject:
            q_args.append(QueryMap(key="subject", value=subject, method="equals"))
        if pattern_by_subject is not None:
            q_args.append(QueryMap(key="subject", value=pattern_by_subject, method="contains"))
        if from_email:
            q_args.append(QueryMap(key="from", value=from_email, method="equals"))
        if to:
            q_args.append(QueryMap(key="to", value=to, method="equals"))
        if after:
            q_args.append(QueryMap(key="receivedDateTime", value=after, method="greater_equal"))
        if before:
            q_args.append(QueryMap(key="receivedDateTime", value=before, method="less_equal"))

        if isinstance(folder, Folder):
            email_folder = folder
        elif isinstance(folder, str):
            folder_path = folder.split("/")
            email_folder = self.mailbox.get_folder(folder_name=folder_path[0])
            if len(folder_path) > 1:
                for sub_folder in folder_path[1:]:
                    email_folder = email_folder.get_folder(folder_name=sub_folder)
            if not email_folder:
                raise AssetNotFoundError(f"No such folder: {folder=}")
        else:
            raise TypeError(f"The {folder=} argument must be of type {str} or {Folder}.")

        query = self.__query_map(email_folder.new_query(), q_args)
        messages = list(email_folder.get_messages(query=query))
        messages.sort(key=lambda x: x.received, reverse=True)
        list(map(lambda m: m.attachments.download_attachments(), messages))

        if pattern_by_attachment:
            # Filter messages based on attachment filenames
            filtered_messages = []
            for message in messages:
                attachments = message.attachments
                for attachment in attachments:
                    if re.match(pattern_by_attachment, attachment.name):
                        filtered_messages.append(message)
                        # No need to check other attachments if one matches
                        break
            return filtered_messages
        else:
            return messages

    def send_message(
        self,
        to: Union[List, str],
        cc: Union[List, str] = "",
        subject: str = "",
        body: str = "",
        attachments: Union[List, str, Path] = (),
        html: bool = False,
    ) -> None:
        """Send an email message.

        :param:
            to (Union[List, str]): List of email addresses to send the message to.
            cc (Union[List, str], optional): List of email addresses to include in the CC field.
            subject (str): Subject of the email message.
            body (str): Body of the email message.
            attachments (Union[List, str, Path], optional): List of file paths or attachments to include in the email.
            html (bool): Indicates whether the body of the email is HTML formatted.

        :return:
            None
        """
        m = self.account.new_message()

        # Add recipients (To and CC)
        if isinstance(to, str):
            to = [to]
        if cc and isinstance(cc, str):
            cc = [cc]
        list(map(lambda _to: m.to.add(_to), to))
        if cc:
            list(map(lambda _cc: m.cc.add(_cc), cc))

        # Set subject and body
        m.subject = subject
        m.body = body

        # Save the message
        m.save_message()

        # Add attachments
        list(map(lambda attachment: m.attachments.add(attachment), attachments))

        # Set email body format (HTML or plain text)
        if html:
            m.body_format = "HTML"

        # Send the message
        m.send()

    def get_two_factor_code_email(
        self,
        subject_pattern: str = "",
        otp_code_pattern: str = r"\b\d{6}\b",
        folder_name: str = "Inbox",
        from_email: str = "",
        unread: bool = True,
        after: Optional[datetime] = None,
    ) -> str:
        """Retrieve two-factor authentication code from email.

        :param:
            subject_pattern (str):  Filter for emails matching a pattern in subject.
            otp_code_pattern (re.Pattern): regex pattern for the otp code on the email body.
            folder_name (str): Name of the folder to retrieve.
            from_email (str): Sender email filter for emails.
            unread (bool, optional): Filter for unread emails.
            after (datetime, optional): Filter emails received after this datetime. If 'None' defaults to now - 1 hour.

        :return:
            str: Two-factor authentication code extracted from the email.

        :raise:
            ValueError: If no email is found.
        """
        # Sets default 'after' to current time minus 1 hour
        if after is None:
            after = datetime.now() - timedelta(hours=1)

        q_args = [QueryMap(key="isRead", value=not unread, method="equals")]
        if subject_pattern:
            q_args.append(QueryMap(key="subject", value=subject_pattern, method="contains"))
        if from_email:
            q_args.append(QueryMap(key="from", value=from_email, method="equals"))
        if after:
            q_args.append(QueryMap(key="receivedDateTime", value=after, method="greater_equal"))

        folder = self.mailbox.get_folder(folder_name=folder_name)

        query = self.__query_map(folder.new_query(), q_args)

        for _ in range(12):
            if result := self.__get_by_date_emails(folder, query):
                match = re.search(otp_code_pattern, result.body)
                if match:
                    return match.group(1)
            time.sleep(5)
        else:
            raise ValueError("No email found")

    @staticmethod
    def download_attachment(file: MessageAttachment, download_dir: str = ""):
        """Download an attachment from an email message and save it to the specified directory.

        :param:
            file (MessageAttachment): The attachment file object to download.
            download_dir (str): The directory where the attachment will be saved.

        :return:
            str: The file path of the downloaded attachment.
        """
        if not download_dir:
            download_dir = os.getcwd()
        file_path = os.path.join(download_dir, str(file.name))
        with open(file_path, "wb") as w:
            decoded_content = base64.b64decode(file.content)
            w.write(decoded_content)
        return file_path

    def __get_by_date_emails(self, folder: Folder, query=None) -> Message or None:
        """Retrieve emails by date.

        :param:
            folder (Folder): folder containing messages.
            query: Query for filtering emails.

        :return:
            Message: Email message object or None if no email is found.
        """
        all_messages = list(folder.get_messages(query=query, download_attachments=False))
        for message in all_messages:
            if self.__check_date(message.created):
                message.mark_as_read()
                message.move(self.mailbox.archive_folder())
                return message
        return None

    @staticmethod
    def __query_map(query_obj: Query, query_args: List[QueryMap]) -> Query:
        """Method that Maps attributes and values to a query object.

        :param:
            query (Query):  Query object to which attributes and values will be mapped.

        :return:
            Query: Modified query object.
        """
        for q in query_args:
            query_obj = getattr(query_obj.on_attribute(q.key), q.method)(q.value)
        return query_obj

    @staticmethod
    def __check_date(mail_date):
        """Check if the mail date is within 2 minutes of the current time."""
        time_now = datetime.now()
        return (
            time_now.date() == mail_date.date()
            and time_now.hour == mail_date.hour
            and time_now.minute - mail_date.minute <= 2
        )
