import pandas as pd
import numpy as np

tapt_sms_dataframe = pd.read_csv("TAPT.csv")

for ix in range(0,len(tapt_sms_dataframe.index)):
    #add twilio sms out data here
