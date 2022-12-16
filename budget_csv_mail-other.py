import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

import csv


budget = {
    "rent": 1000,
    "utilities": 100,
    "groceries": 300,
    "entertainment": 50
}




# Open a file for writing
with open("monthly_budget.csv", "w", newline="") as csv_file:
    # Create a CSV writer object
    writer = csv.writer(csv_file)
    
    # Write the header row
    writer.writerow(["Item", "Amount"])
    
    # Write the budget items and amounts
    for item, amount in budget.items():
        writer.writerow([item, amount])

Item,Amount
rent,1000
utilities,100
groceries,300
entertainment,50




# Specify the sender's and recipient's email addresses
sender = "sender@example.com"
recipient = "recipient@example.com"

# Create a message object
msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = COMMASPACE.join([recipient])
msg["Subject"] = "Monthly budget"

# Add the CSV file as an attachment
with open("monthly_budget.csv", "rb") as csv_file:
    # Create a MIMEBase object for the attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload((csv_file).read())

# Encode the attachment and add it to the message
encoders.encode_base64(part)
part.add_header("Content-Disposition", "attachment", filename="monthly_budget.csv")
msg.attach(part)

# Create an SMTP client and send the email
server = smtplib.SMTP("smtp.example.com")
server.sendmail(sender, recipient, msg.as_string())
server.quit()

