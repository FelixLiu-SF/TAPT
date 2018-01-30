import pandas as pd
import numpy as np
import math
import time
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

    #process spreadsheet data
    temp_phone_plus = "+1" + str(temp_phone)
    temp_name = str(temp_name)
    temp_videourl = str(temp_videourl)
    temp_timeflag_morning = int(temp_timeflag_morning)
    temp_timeflag_afternoon = int(temp_timeflag_afternoon)
    temp_timeflag_evening = int(temp_timeflag_evening)

    #construct body of SMS text
    temp_sms_body = ""
    temp_sms_body = temp_sms_body + "Please watch the video today. Practice the video tips 3x/day or more and hold for 10 seconds for good posture. Increase slowly as you get stronger (goal is 5 minutes).\n"
    temp_sms_body = temp_sms_body + temp_videourl

    #construct greeting SMS texts
    temp_sms_greeting = ""
    temp_sms_greeting = temp_sms_greeting + "Hello " + temp_name + ", this is the posture training study. Welcome to the study.\n"
    temp_sms_greeting = temp_sms_greeting + "You can expect daily text messages from us, depending upon your preferences, from 8am-8pm every day of the week. "
    temp_sms_greeting = temp_sms_greeting + "At least one message will contain a video link. The last message of the day will ask if you practiced, and prompt for a reply.\n"
    temp_sms_greeting = temp_sms_greeting + "Please contact Shirley Wong at Wong2@ucsf.edu if you have any questions. "

    #construct questionnaire SMS text
    temp_sms_question = ""
    temp_sms_question = temp_sms_question + "Did you practice today?\nPlease reply with 0 or 1: \n\n"
    temp_sms_question = temp_sms_question + "1 = Yes, I practiced 3x or more.\n"
    temp_sms_question = temp_sms_question + "0 = No, I did not practice 3x today.\n"

    #check greeting status
    temp_greeting_flag = tapt_merged_dataframe.iloc[ix,9]

    if not(math.isnan(temp_greeting_flag)):
        #not a new subject. no greeting needed
        print(str(ix))
        print(temp_phone_plus)

        if temp_timeflag_evening:

            print(temp_sms_body)

            #send an SMS text message
            client.messages.create(
               to=temp_phone_plus,
               from_=twilio_phone,
               body=temp_sms_body
            )

            print(temp_sms_question)

            #send questionnare
            client.messages.create(
               to=temp_phone_plus,
               from_=twilio_phone,
               body=temp_sms_question
            )
        else:
            # no reminder, but ask the questionnaire
            print(temp_sms_question)

            #send questionnare
            client.messages.create(
               to=temp_phone_plus,
               from_=twilio_phone,
               body=temp_sms_question
            )

        print(" ")

    else:
        #new subject! greet the subject!

        print(str(ix))
        print(temp_phone_plus)

        if temp_timeflag_evening:

            tapt_greeting_dataframe = tapt_greeting_dataframe.append({'SubjectID': temp_ID,'GreetingName': temp_name,'GreetingSent':1},ignore_index=True)

            print(temp_sms_greeting)

            #send greeting
            client.messages.create(
               to=temp_phone_plus,
               from_=twilio_phone,
               body=temp_sms_greeting
            )

            print(temp_sms_body)

            #send an SMS text message
            client.messages.create(
               to=temp_phone_plus,
               from_=twilio_phone,
               body=temp_sms_body
            )

            print(temp_sms_question)
            print(" ")
            time.sleep(3)

            #send questionnare
            client.messages.create(
               to=temp_phone_plus,
               from_=twilio_phone,
               body=temp_sms_question
            )


tapt_greeting_dataframe.to_csv(filepath_csv_greeting,index=False)
