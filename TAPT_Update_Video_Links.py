import pandas as pd
import numpy as np
import math
import datetime as dt


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
tapt_enrolled_dataframe = pd.read_csv(filepath_csv_enrollment, index_col='StudyID')

# read in enrollment date file

# pseudocode for finding correct video links


date_today_dt = dt.datetime.today() # today's date
date_format = '%m/%d/%Y' # date format of enrollment spreadsheet

del_array = list() # initialize array for deleting rows


for ix in range(0,len(tapt_sms_dataframe.index)):

    # current participant ID number
    temp_ID = tapt_sms_dataframe.iloc[ix,0]

    # look up enrollment date for this participant

    date_enrolled_str = tapt_enrolled_dataframe.loc[temp_ID, 'VideoStartDates']
    date_enrolled_dt = dt.datetime.strptime(date_enrolled_str, date_format)

    dt_since_enrollment = date_today_dt - date_enrolled_dt
    days_since_enrollment = dt_since_enrollment.days


    if days_since_enrollment<=(6*7):

        # enrolled less than or equal to 6 weeks, update video link

        fullweeks_since_enrollment = days_since_enrollment//int(7)
        remain_in_week_enrollment = days_since_enrollment%7

        #sanitize the index
        if remain_in_week_enrollment>0.5:

            current_week_index = max([fullweeks_since_enrollment,0])
            current_week_index = min([current_week_index,5])

        else:

            current_week_index = max([fullweeks_since_enrollment-1,0])
            current_week_index = min([current_week_index,5])


        current_video_url = tapt_week_video_url[current_week_index]

        # replace video url link in master txt msg spreadsheet
        tapt_sms_dataframe.iloc[ix,3] = current_video_url

    else:

        # officially over 6 weeks enrolled in the study, remove this ppt
        del_array.append(ix)

if len(del_array)>0.5:
    for jx in range(0,len(del_array)):

        tapt_sms_dataframe.drop(tapt_sms_dataframe.index[del_array], inplace=True)


# write out new master txt msg spreadsheet
tapt_sms_dataframe.to_csv(filepath_csv_sms, index=False)
