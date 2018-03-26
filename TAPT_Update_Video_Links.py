import pandas as pd
import numpy as np
import math
import time
import datetime


# define static video url links

tapt_week_video_url = ['https://courses.ucsf.edu/mod/kalvidres/view.php?id=413234',
'https://courses.ucsf.edu/mod/kalvidres/view.php?id=413235',
'https://courses.ucsf.edu/mod/kalvidres/view.php?id=413236',
'https://courses.ucsf.edu/mod/kalvidres/view.php?id=405698',
'https://courses.ucsf.edu/mod/kalvidres/view.php?id=405699',
'https://courses.ucsf.edu/mod/kalvidres/view.php?id=405700']

# filename parameters
filepath_csv_sms = "C:/Users/fliu2/Box Sync/UCSF_TAPT_Share/UCSF_TAPT_TextMsg_Master.csv"
filepath_csv_enrollment = "C:/Users/fliu2/Box Sync/UCSF_TAPT_Share/VAPT_Participant_Enrolled.csv"

# read in current master txt msg spreadsheet
tapt_sms_dataframe = pd.read_csv(filepath_csv_sms)
tapt_enrolled_dataframe = pd.read_csv(filepath_xls_enrollment, index_col='StudyID')

# read in enrollment date file

# pseudocode for finding correct video links


date_today_dt = datetime.date.today() # today's date
date_format = '%m/%d/%Y' # date format of enrollment spreadsheet

del_array = [] # initialize array for deleting rows


for ix in range(0,len(tapt_sms_datafram.index))

    # current participant ID number
    temp_ID = str(tapt_merged_dataframe.iloc[ix,0])

    # look up enrollment date for this participant

    date_enrolled_str = tapt_enrolled_dataframe.loc(temp_ID, 'VideoStartDates')
    date_enrolled_dt = datetime.strptime(date_enrolled_str, date_format)

    days_since_enrollment = int(date_today_dt - date_enrolled_dt)

    if days_since_enrollment<=(6*7):

        # enrolled less than or equal to 6 weeks, update video link

        fullweeks_since_enrollment = days_since_enrollment//int(7)
        current_week_index = max([fullweeks_since_enrollment,0]) #sanitize the index
        current_video_url = tapt_week_video_url[current_week_index]

        # replace video url link in master txt msg spreadsheet
        tapt_sms_dataframe.iloc[ix,4] = current_video_url

    else:

        # officially over 6 weeks enrolled in the study, remove this ppt
        del_array = [del_array, ix]

if len(del_array>0):
    for jx in range(0,len(del_array)):

        tapt_sms_dataframe.drop(tapt_sms_dataframe.index[del_array], inplace=True)


# write out new master txt msg spreadsheet
tapt_sms_dataframe.to_csv(filepath_csv_sms, index=False)
