from twilio.rest import Client

account_sid = ''
auth_token = ''

client = Client(account_sid, auth_token)

client.messages.create(
    to="+14157106405",
    from_="+14159803374",
    body="This is a a test Twilio message for TAPT Conference Call www.youtube.com"
)

client.messages.create(
    to="+15108825920",
    from_="+14159803374",
    body="This is a a test Twilio message for TAPT Conference Call www.youtube.com"
)
