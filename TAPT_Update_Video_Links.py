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
# read in enrollment date file
tapt_enrolled_dataframe = pd.read_csv(filepath_csv_enrollment, index_col='StudyID')

# get dates
date_today_dt = dt.datetime.today() # today's date
date_format = '%m/%d/%Y' # date format of enrollment spreadsheet

del_array = list() # initialize array for deleting rows

# loop through each participant and check number of days since enrollment
for ix in range(0,len(tapt_sms_dataframe.index)):

    # current participant ID number
    temp_ID = tapt_sms_dataframe.iloc[ix,0]

    # look up enrollment date for this participant
    reindex_enrolled_dataframe = tapt_enrolled_dataframe.reindex([temp_ID], copy=True, fill_value='missing') # reindex the dataframe to catch missing ppts
    date_enrolled_str = reindex_enrolled_dataframe.loc[temp_ID, 'VideoStartDates']

    # continue is ppt was non missing (not a NaN value for date)
    if date_enrolled_str!='missing':
        date_enrolled_dt = dt.datetime.strptime(date_enrolled_str, date_format)

        # calculate days since enrollment
        dt_since_enrollment = date_today_dt - date_enrolled_dt
        days_since_enrollment = dt_since_enrollment.days

        # update links or delete finished ppts
        if days_since_enrollment<=(6*7):

            # enrolled less than or equal to 6 weeks, update video link

            fullweeks_since_enrollment = days_since_enrollment//int(7)
            remain_in_week_enrollment = days_since_enrollment%7

            #sanitize the week-index
            if remain_in_week_enrollment>0.5:

                # ppt is in the next week
                current_week_index = max([fullweeks_since_enrollment,0])
                current_week_index = min([current_week_index,5])

            else:

                # ppt is on the last day of this week
                current_week_index = max([fullweeks_since_enrollment-1,0])
                current_week_index = min([current_week_index,5])

            # get the video url link
            current_video_url = tapt_week_video_url[current_week_index]

            # replace video url link in master txt msg spreadsheet
            tapt_sms_dataframe.iloc[ix,3] = current_video_url

        elif days_since_enrollment>(6*7):

            # officially over 6 weeks enrolled in the study, remove this ppt
            del_array.append(ix)

    else:
        print('The ID below is missing from the enrollment log')
        print(temp_ID)

# delete ppts who have finished the study, if any
if len(del_array)>0.5:
    for jx in range(0,len(del_array)):

        tapt_sms_dataframe.drop(tapt_sms_dataframe.index[del_array[ix]], inplace=True)


# write out new master txt msg spreadsheet
tapt_sms_dataframe.to_csv(filepath_csv_sms, index=False)
