from twilio.rest import Client

# Your Twilio account SID and auth token
account_sid = "ACxxxxxxxxxxxxxx"
auth_token = "your_auth_token"

# Your Twilio phone number
from_number = "+12345678901"

# The phone number you want to send the SMS to
to_number = "+12345678902"

# The message you want to send
message = "Hello, this is a test SMS message."

# Create a Twilio client and send the SMS
client = Client(account_sid, auth_token)
client.messages.create(to=to_number, from_=from_number, body=message)
