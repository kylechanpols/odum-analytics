# -*- coding: utf-8 -*-
"""
Created on Thu May 27 15:50:29 2021

@author: Kyle
"""
##################################################################################
#A program to find out the number of students seen at Odum/ Davis Lab
##################################################################################
#0. Load modules and def custom funx
from pathlib import Path
import pandas as pd
import numpy as np
import datetime
import calendar

def findDay(date):
    date = str(date)
    born = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
    return (calendar.day_name[born])

def checkRoster(s):
    if(s.shape[0] == 0):
        raise NameError("Roster is empty - Consultant Name either incorrect or Consultant does not exist")
        
def checkOutput(s):
    if(s.shape[0] == 0):
        raise ValueError("Output is empty!")

##################################################################################
#1. Read Data
wd = Path("C:/Users/Kyle/Google Drive/Research/Python Misc/Odum Data/") # working directory

f = wd / 'Hub Stat Data 2020-5-26-21.xlsx'

odum = pd.read_excel(f)

##################################################################################
#2. String split time stamp
# see attributes of https://docs.python.org/2/library/datetime.html for details
# must be vectorized

odum['date'] = [d.date() for d in odum['RecordedDate']]
odum['time'] = [d.time() for d in odum['RecordedDate']]

##################################################################################
#3. Turn into Week Days

odum['day'] = [findDay(d) for d in odum['date']]

##################################################################################
odum["period"] = "None" #create new column called period for further processing.

##################################################################################
#4. Import sorting rules dataset

f = wd / 'sort.csv'

sort = pd.read_csv(f).dropna()
sort['StartDate'] = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in sort["StartDate"]]
sort['EndDate'] = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in sort["EndDate"]]
sort['StartTime'] = [datetime.datetime.strptime(d, "%H:%M:%S").time() for d in sort["StartTime"]]
sort['EndTime'] = [datetime.datetime.strptime(d, "%H:%M:%S").time() for d in sort["EndTime"]]

##################################################################################
#5. Loop and Populate Consultations Done

#psuedo code:
# for each row in odum.
# get the date, time and day of consultation.
# check if date fall within any interval of StartDate and EndDate.

out = pd.DataFrame() #init output pd.
#out = out.append(odum.iloc[3], ignore_index=True)

### !Dev: may have to add a filtering mechanism here to prevent the program from running throughout sort.csv

consultant = "Kyle"

s = sort[sort["Consultant"] == consultant]   

checkRoster(s) #sanity check - see if the returned roster is empty. If so, flag the user

# by default the use of loops will only return the first result in the dataset if there are multiple matches
for i in range(0,odum.shape[0]):
    d = odum.iloc[i]["date"]
    t = odum.iloc[i]["time"]
    w = odum.iloc[i]["day"]

    for j in range(0, s.shape[0]):
        if((s.iloc[j]["StartDate"] <= d and s.iloc[j]["EndDate"] >= d) and
           (s.iloc[j]["StartTime"] <= t and s.iloc[j]["EndTime"] >= t) and
           (s.iloc[j]["WeekDay"] == w)):
                odum.iloc[i, odum.columns.get_loc("period")] = s.iloc[j]["Period"]
                out = out.append(odum.iloc[i], ignore_index=True)
                next

consultant = consultant + ".csv" #rename path - use consultant name automatically
target = wd / consultant

checkOutput(out)

out.to_csv(target)
            
    
    