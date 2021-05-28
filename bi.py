# -*- coding: utf-8 -*-
"""
Created on Thu May 27 20:22:57 2021

@author: Kyle
"""
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

###############################################################################
wd = Path("C:/Users/Kyle/Google Drive/Research/Python Misc/Odum Data/") # working directory

f = wd / "Kyle.csv"

dat = pd.read_csv(f)

###############################################################################
# How many clients did I see?
dat.shape[0] #93 Clients

###############################################################################
#Find counts and proportions of the clients by dept.
###############################################################################

# how many different departments?
dat[["Unnamed: 0","DEPT NAME Consultee Dept Name from Lookup"]].groupby("DEPT NAME Consultee Dept Name from Lookup").count().shape[0]
dept_full = dat[["Unnamed: 0","DEPT NAME Consultee Dept Name from Lookup"]].groupby("DEPT NAME Consultee Dept Name from Lookup").count()



f = wd / "dept.png"
dept = dat[["Unnamed: 0","Dept_category"]].groupby("Dept_category").count()

fig1, ax1 = plt.subplots()
explode = (0,0,0.1,0,0.1,0.1,0.3)
ax1.pie(dept["Unnamed: 0"], explode=explode, labels=dept.index, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')
plt.title("Distribution of Client Departments")
plt.savefig(f, dpi=150)

######ＴＯＤＯ：　Group Depts


###############################################################################
#Find clients by period served
###############################################################################

period = dat[["Unnamed: 0","period"]].groupby("period").count()
f = wd / "period.png"
fig1, ax1 = plt.subplots()
explode = (0,0,0.1,0)
ax1.pie(period["Unnamed: 0"], labels=period.index, explode=explode,autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')
plt.title("Distribution of Consultations by Semester")
plt.savefig(f, dpi=150)

###############################################################################
#Find clients by Status
###############################################################################
status = dat[["Unnamed: 0","STATUS"]].groupby("STATUS").count()
status = status.rename(index={'None of the above': 'Other'})
f = wd / "status.png"
fig1, ax1 = plt.subplots()
#explode= (0,0,0.1,0,0,0,0)
patches, texts, autotexts = ax1.pie(status["Unnamed: 0"], labels=status.index, autopct='%1.1f%%',
        shadow=True, startangle=90)
[t.set_fontsize(7) for t in autotexts]
ax1.axis('equal')

plt.title("Distribution of Client Type", y=1.08)
plt.savefig(f, dpi=150)