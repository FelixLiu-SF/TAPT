import pandas as pd
import numpy as np
import math
from twilio.rest import Client

# filename parameters

filepath_twilio = "TwilioAuth.csv"
filepath_csv_sms = "C:/Users/fliu2/Box Sync/UCSF_TAPT_Share/UCSF_TAPT_TextMsg_Master.csv"
filepath_csv_greeting = "C:/Users/fliu2/Box Sync/UCSF_TAPT_Share/UCSF_TAPT_GreetingTracker.csv"

#read in twilio authentication info
twilio_dataframe = pd.read_csv(filepath_twilio)
account_sid = str(twilio_dataframe.iloc[0,0])
auth_token = str(twilio_dataframe.iloc[0,1])
twilio_phone = "+" + str(twilio_dataframe.iloc[0,2])

#make twilio object
client = Client(account_sid,auth_token)

#read in spreadsheet for outgoing SMS texts
tapt_sms_dataframe = pd.read_csv(filepath_csv_sms)
tapt_greeting_dataframe = pd.read_csv(filepath_csv_greeting)

tapt_merged_dataframe = pd.merge(tapt_sms_dataframe,tapt_greeting_dataframe,how='left',on='SubjectID')

#loop through spreadsheet
for ix in range(0,len(tapt_merged_dataframe.index)):
    #extract SMS info out of spreadsheet
    temp_ID = tapt_merged_dataframe.iloc[ix,0]
    temp_name = tapt_merged_dataframe.iloc[ix,1]
    temp_phone = tapt_merged_dataframe.iloc[ix,2]
    temp_videourl = tapt_merged_dataframe.iloc[ix,3]
    temp_surveyurl = tapt_merged_dataframe.iloc[ix,4]
    temp_timeflag_morning = tapt_merged_dataframe.iloc[ix,5]
    temp_timeflag_afternoon = tapt_merged_dataframe.iloc[ix,6]
    temp_timeflag_evening = tapt_merged_dataframe.iloc[ix,7]

    temp_phone_plus = "+" + str(temp_phone)

    #construct body of SMS text
    temp_sms_body = ""
    temp_sms_body = temp_sms_body + "Hello " + temp_name + ", this is a message from the UCSF TAPT study. "
    temp_sms_body = temp_sms_body + "We\'d like to remind you to watch the video on posture and practice today. "
    temp_sms_body = temp_sms_body + "You may watch the video at this website: " + temp_videourl

    #check greeting status
    temp_greeting_flag = tapt_merged_dataframe.iloc[ix,9]

    if not(math.isnan(temp_greeting_flag)):
        #not a new subject. no greeting needed
        print(str(ix))
        print(temp_phone_plus)
        print(temp_sms_body)
        print(" ")
    else:
        #new subject! greet the subject!

        tapt_greeting_dataframe = tapt_greeting_dataframe.append({'SubjectID': temp_ID,'GreetingName': temp_name,'GreetingSent':1},ignore_index=True)

        print(str(ix))
        print("Greetings!")
        print(temp_phone_plus)
        print(temp_sms_body)
        print(" ")

    #add twilio sms out data here
    #client.messages.create(
    #    to=temp_phone_plus,
    #    from_=twilio_phone,
    #    body=temp_sms_body
    #)

tapt_greeting_dataframe.to_csv(filepath_csv_greeting,index=False)
