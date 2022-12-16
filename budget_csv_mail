import csv
import smtplib
from email.mime.text import MIMEText


def read_budget_data(filename):
    budget = {}
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip the header row
        for row in reader:
            category = row[0]
            amount = float(row[1])
            budget[category] = amount
    return budget

def send_email(server, sender, password, recipient, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    s = smtplib.SMTP(server)
    s.login(sender, password)
    s.send_message(msg)
    s.quit()
