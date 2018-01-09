import pandas as pd
import numpy as np
from twilio.rest import Client

#read in twilio authentication info
twilio_dataframe = pd.read_csv("TwilioAuth.csv")
account_sid = str(twilio_dataframe.iloc[0,0])
auth_token = str(twilio_dataframe.iloc[0,1])
twilio_phone = "+" + str(twilio_dataframe.iloc[0,2])

#make twilio object
client = Client(account_sid,auth_token)

#read in spreadsheet for outgoing SMS texts
tapt_sms_dataframe = pd.read_csv("UCSF_TAPT_TextMsg_FelixOnly.csv")

for ix in range(0,len(tapt_sms_dataframe.index)):
    #extract SMS info out of spreadsheet
    temp_ID = tapt_sms_dataframe.iloc[ix,0]
    temp_name = tapt_sms_dataframe.iloc[ix,1]
    temp_phone = tapt_sms_dataframe.iloc[ix,2]
    temp_videourl = tapt_sms_dataframe.iloc[ix,3]
    temp_surveyurl = tapt_sms_dataframe.iloc[ix,4]
    temp_timeflag_morning = tapt_sms_dataframe.iloc[ix,5]
    temp_timeflag_afternoon = tapt_sms_dataframe.iloc[ix,6]
    temp_timeflag_evening = tapt_sms_dataframe.iloc[ix,7]

    temp_phone_plus = "+1" + str(temp_phone)

    #construct body of SMS text
    temp_sms_body = ""
    temp_sms_body = temp_sms_body + "Hello " + temp_name + ", this is a message from the UCSF TAPT study. \n"
    temp_sms_body = temp_sms_body + "We\'d like to remind you to watch the video on posture and practice today. \n"
    temp_sms_body = temp_sms_body + "You may watch the video at this website: " + temp_videourl

    #debug
    print(temp_phone_plus)
    print(twilio_phone)
    print(temp_sms_body)

    #add twilio sms out data here
    client.messages.create(
       to=temp_phone_plus,
       from_=twilio_phone,
       body=temp_sms_body
    )
