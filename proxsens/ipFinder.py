import socket
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient


account_sid = "AC32dc469056fcc10397cc8890568574e9" # Your Account SID from www.twilio.com/console
auth_token  = "92c21219bdf7769b3494096b6c2dcc80"  # Your Auth Token from www.twilio.com/console

client = TwilioRestClient(account_sid, auth_token)

try:
    message = client.messages.create(body=socket.gethostbyname(socket.gethostname()),to="+972543014987",    # Replace with your phone number
from_="+17028007210") # Replace with your Twilio number



except TwilioRestException as e:
    print(e)