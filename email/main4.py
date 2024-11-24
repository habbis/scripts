#!/usr/bin/env python3

import imaplib
import email
import os
import calendar
from datetime import datetime
from datetime import timedelta

# Configuration
ACCOUNTS = [
    {
        'imap_server': 'mail.habbestad.tech',
        'email_account': 'hotell@habbestad.tech',
        'password': ''
    },
    {
        'imap_server': 'mail.habbestad.org',
        'email_account': 'habbis@habbestad.org',
        'password': ''
    }
]
ATTACHMENTS_DIR = 'attachments4'  # Directory to save attachments


def connect_to_email(account):
    """Connect to the email server for a specific account."""
    mail = imaplib.IMAP4_SSL(account['imap_server'])
    mail.login(account['email_account'], account['password'])
    return mail


def save_attachment(msg, download_path, sender_email):
    """Save the attachment to the specified path, including sender email in the filename."""
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        file_name = part.get_filename()
        if file_name:
            # Add sender email to the filename
            sender_safe = sender_email.replace('@', '_at_').replace('.', '_')
            new_file_name = f"{sender_safe}_{file_name}"
            file_path = os.path.join(download_path, new_file_name)
            with open(file_path, 'wb') as file:
                file.write(part.get_payload(decode=True))


def organize_attachments_by_week(mail):
    """Download and organize attachments from all emails by week."""
    mail.select('inbox')  # Select the inbox

    # Search for all emails
    status, messages = mail.search(None, 'ALL')
    if status != 'OK':
        print("Failed to search emails")
        return

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

        # Extract the sender's email
        sender = email.utils.parseaddr(msg['From'])[1]

        # Extract the email date
        email_date = msg['Date']
        if not email_date:
            continue

        # Convert email date to a datetime object
        date_tuple = email.utils.parsedate_tz(email_date)
        if date_tuple:
            email_datetime = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            year = email_datetime.year
            week_number = email_datetime.isocalendar()[1]  # Get ISO week number

            # Create a folder for the week if it doesn't exist
            week_dir = os.path.join(ATTACHMENTS_DIR, f"{year}-Week-{week_number}")
            os.makedirs(week_dir, exist_ok=True)

            # Save the attachments
            save_attachment(msg, week_dir, sender)


def process_accounts():
    """Process multiple email accounts."""
    for account in ACCOUNTS:
        print(f"Processing account: {account['email_account']}")
        try:
            mail = connect_to_email(account)
            organize_attachments_by_week(mail)
        except Exception as e:
            print(f"Error processing account {account['email_account']}: {e}")
        finally:
            try:
                mail.logout()
            except:
                pass


if __name__ == '__main__':
    # Ensure the attachments directory exists
    os.makedirs(ATTACHMENTS_DIR, exist_ok=True)

    # Process all accounts
    process_accounts()

