t-office-365
============

Description
-----------
This library simplifies Microsoft Office 365 integration by enabling authentication
once and allowing the use of a single instance to access various services seamlessly.

Installation
------------
The T-Office-365 package is available on PyPi. This library simplifies Microsoft Office 365 integration by enabling authentication once and allowing the use of a single instance to access various services seamlessly.You can use pip and can add it to your project by running the following command:

.. code-block:: bash

    pip install t-office-365

Key features
------------

**1. Authentication once and all services available**:

    office = OfficeAccount('client_id', 'client_secret', 'tenant_id')


**2. Outlook App:** send, get and parse emails

    emails = office.outlook.get_emails(subject='OTP Code', unread=True)

**3. OneDrive Integration:** for efficient file storage, retrieval, and management

    onedrive_site = office.onedrive.site(email_id='user@example.com')

**4. SharePoint Integration:** for efficient collaboration and document management

    sharepoint_site = office.sharepoint.site(site_name='example_site')

**5. Excel Operations:** creating, updating, and retrieving data from live Excel files

    # for Onedrive site

    sheet_names = onedrive_site.excel.get_sheet_names(file_id='file_id')

    # for SharePoint site

    sheet_names = sharepoint_site.excel.get_sheet_names(file_id='file_id')
