#!/usr/bin/env python3

import imaplib
import email
import os
import calendar
from datetime import datetime

# Configuration
IMAP_SERVER = 'mail.habbestad.tech'  # Change for other providers
EMAIL_ACCOUNT = 'hotell@habbestad.tech'
PASSWORD = ''  # Use an app password for security
ATTACHMENTS_DIR = 'attachments'  # Directory to save attachments

def connect_to_email():
    """Connect to the email server."""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    return mail

def save_attachment(msg, download_path):
    """Save the attachment to the specified path."""
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        file_name = part.get_filename()
        if file_name:
            file_path = os.path.join(download_path, file_name)
            with open(file_path, 'wb') as file:
                file.write(part.get_payload(decode=True))

def organize_attachments_by_month(mail):
    """Download and organize attachments by month."""
    mail.select('inbox')  # Select the inbox
    status, messages = mail.search(None, 'ALL')  # Fetch all emails
    email_ids = messages[0].split()

    for email_id in email_ids:
        # Fetch the email
        status, data = mail.fetch(email_id, '(RFC822)')
        if status != 'OK':
            print(f"Failed to fetch email ID {email_id}")
            continue

        # Parse the email
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        email_date = msg['Date']
        if not email_date:
            continue

        # Convert email date to a datetime object
        date_tuple = email.utils.parsedate_tz(email_date)
        if date_tuple:
            email_datetime = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            month_name = calendar.month_name[email_datetime.month]
            year = email_datetime.year

            # Create a folder for the month if it doesn't exist
            month_dir = os.path.join(ATTACHMENTS_DIR, f"{year}-{month_name}")
            os.makedirs(month_dir, exist_ok=True)

            # Save the attachments
            save_attachment(msg, month_dir)

if __name__ == '__main__':
    # Ensure the attachments directory exists
    os.makedirs(ATTACHMENTS_DIR, exist_ok=True)

    # Connect to the email server and process emails
    try:
        mail = connect_to_email()
        organize_attachments_by_month(mail)
    finally:
        mail.logout()

