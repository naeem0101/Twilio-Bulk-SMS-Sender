import csv, sys
from twilio.rest import Client

MESSAGE_FILE = 'message.txt'     # File containing text message
CSV_FILE = 'participants.csv'    # File containing participant numbers
SMS_LENGTH = 160                 # Max length of one SMS message
MSG_COST = 0.057                 # Cost per message

account_sid = "AC0528d01825d7620c9468c8306a35a3e4"
auth_token = "6cbb83e2a914c0d5f26134f5f9f6f87b"
from_num = "+15309245367"

# Now put your SMS in a file called message.txt, and it will be read from there.
with open(MESSAGE_FILE, 'r') as content_file:
    sms = content_file.read()

# Check we read a message OK
if len(sms.strip()) == 0:
    print("SMS message not specified- please make a {}' file containing it. \r\nExiting!".format(MESSAGE_FILE))
    sys.exit(1)
else:
    print("> SMS message to send: \n\n{}".format(sms))

# How many segments is this message going to use?
segments = int(len(sms.encode('utf-8')) / SMS_LENGTH) +1

# Open the people CSV and get all the numbers out of it
with open(CSV_FILE, 'r') as csvfile:
    peoplereader = csv.reader(csvfile)
    numbers = set([p[0] for p in peoplereader]) # remove duplicate numbers


# Calculate how much it's going to cost:
messages = len(numbers)
cost = MSG_COST * segments * messages

print("> {} messages of {} segments each will be sent, at a cost of ${} ".format(messages, segments, cost))

# Check you really want to send them
confirm = raw_input("Send these messages? [Y/n] ")
if confirm[0].lower() == 'y':
    # Set up Twilio client
    client = Client(account_sid, auth_token)

    # Send the messages
    for num in numbers:
        # Send the sms text to the number from the CSV file:
        print("Sending to " + num)
        message = client.messages.create(to=num, from_=from_num, body=sms)

print("Exiting!")
