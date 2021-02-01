from twilio.rest import Client
# contains Twilio API account information
# THIS INFORMATION IS NOT ACCURATE. ACTUAL ACCOUNT INFO IS STORED LOCALLY ONLY
account_sid, auth_token, from_num, my_phone_number = open("texts/twilio.txt", "r").read().split(",")
# This is not accurate account info! that will be held on my PC only.

client = Client(account_sid, auth_token)


def get_balance():
    return Client(account_sid, auth_token).api.accounts(account_sid).fetch().balance.fetch().balance


def text_numbers(to_number, from_number, message):
    client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )
