# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC8e14b1e892a9456d0a2656ac0ca8634e'
auth_token = '003436af2c87166e199a44c46a299403'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+12565008428',
                     to='+16039735334'
                 )

print(message.sid)