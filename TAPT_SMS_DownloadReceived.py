import pandas as pd
import numpy as np
import math
import datetime
from twilio.rest import Client

# filename parameters

filepath_twilio = "TwilioAuth.csv"
filepath_csv_sms_recd = "C:/Users/fliu2/Box Sync/UCSF_TAPT_Share/UCSF_TAPT_ReceivedMessages.csv"

#read in twilio authentication info
twilio_dataframe = pd.read_csv(filepath_twilio)
account_sid = str(twilio_dataframe.iloc[0,0])
auth_token = str(twilio_dataframe.iloc[0,1])
twilio_phone = "+" + str(twilio_dataframe.iloc[0,2])

#make twilio object
client = Client(account_sid,auth_token)

messages = client.messages.list(to=twilio_phone)

msg_list = []

for message in messages:
    msg_list.append([str(message.date_sent), message.direction, message.from_, message.to, message.body])

msg_df = pd.DataFrame(data=msg_list)
msg_df.columns = ["DateTime", "Direction", "From", "To", "Body"]

print(msg_df)

msg_df.to_csv(filepath_csv_sms_recd)
