from calc_div import *
import pickle

import pandas as pd
import pdb
import os

from datetime import datetime

import sys
import time
pd.options.display.max_columns = None

import pandas as pd
import pdb
import os

from datetime import datetime

import sys
import time
pd.options.display.max_columns = None
import json

#Load 2016 NY data
df = pd.read_csv('2017.zip',encoding='ISO-8859-1',low_memory=False,compression='zip', header=0) #,nrows=20000
df.columns = ["Name Last","Name First","Name Middle","Name Suffix","Residence House Number","Residence Fractional Address","Residence Apartment","Residence Pre Street Direction","Residence Street Name","Residence Post Street Direction","Residence City","Residence Zip Code 5","Zip code plus 4","Mailing Address Line 1","Mailing Address Line 2","Mailing Address Line 3","Mailing Address 4","Birth Date","Gender","Party Affiliation","Name or Party if Voter Checks “Other” on registration form.","County Code","Election district","Legislative district","Town/City","Ward","Congressional district","Senate district","Assembly district","Last date voted","Last year voted (from registration form)","Last county voted in (from registration form ).","Last registered address","Last registered name (if different)","County Voter Registration Number.","Registration Date","Application Source","Identification Required Flag.","Identification Verification Requirement Met Flag.","Voter Status Codes.","Status Reason Codes","Date Voter made Inactive","Date voter was Purged","Voter ID","Voter History"]
df = df.loc[:,["Voter ID","Name Last","Name First","Name Middle","Residence House Number","Residence Street Name","Residence City","Residence Zip Code 5","Gender","Birth Date","Registration Date","Party Affiliation","County Code"]]
df['Birth Date'] = df['Birth Date'].apply(lambda x : str(x)  )
df['Birth Date'] = df['Birth Date'].apply(lambda x : x[4:6] +  '/' + x[6:8]  +  '/' + x[0:4] ) #Format date
df = df.dropna(subset=["Voter ID", "Name Last","Birth Date","Name First","Residence House Number","Residence Street Name","Residence City","Gender","Party Affiliation","County Code"])
temp_dataframe = df[df['Gender'].isin(['M', 'F'])] #Only consider male female
temp2 = temp_dataframe 
coupes_same,coupes_diff =  identify_couples_countywise(temp2,True) #Identify the couples


#Code below is the exact copy of above - only loads 2017 data
df = pd.read_csv('2016.zip',encoding='ISO-8859-1',low_memory=False,compression='zip', header=0) #,nrows=20000
df.columns = ["Name Last","Name First","Name Middle","Name Suffix","Residence House Number","Residence Fractional Address","Residence Apartment","Residence Pre Street Direction","Residence Street Name","Residence Post Street Direction","Residence City","Residence Zip Code 5","Zip code plus 4","Mailing Address Line 1","Mailing Address Line 2","Mailing Address Line 3","Mailing Address 4","Birth Date","Gender","Party Affiliation","Name or Party if Voter Checks “Other” on registration form.","County Code","Election district","Legislative district","Town/City","Ward","Congressional district","Senate district","Assembly district","Last date voted","Last year voted (from registration form)","Last county voted in (from registration form ).","Last registered address","Last registered name (if different)","County Voter Registration Number.","Registration Date","Application Source","Identification Required Flag.","Identification Verification Requirement Met Flag.","Voter Status Codes.","Status Reason Codes","Date Voter made Inactive","Date voter was Purged","Voter ID","Voter History"]
df = df.loc[:,["Voter ID","Name Last","Name First","Name Middle","Residence House Number","Residence Street Name","Residence City","Residence Zip Code 5","Gender","Birth Date","Registration Date","Party Affiliation","County Code"]]
df['Birth Date'] = df['Birth Date'].apply(lambda x : str(x)  )
df['Birth Date'] = df['Birth Date'].apply(lambda x : x[4:6] +  '/' + x[6:8]  +  '/' + x[0:4] )
df = df.dropna(subset=["Voter ID", "Name Last","Birth Date","Name First","Residence House Number","Residence Street Name","Residence City","Gender","Party Affiliation","County Code"])
temp_dataframe = df[df['Gender'].isin(['M', 'F'])]
temp3 = temp_dataframe 
coupes1_same,coupes1_diff =  identify_couples_countywise(temp3,True)



#Calculate divorce per county
cty_divorce = {}
for cty,key_couples in coupes_same.items() :
    if cty not in cty_divorce :
       cty_divorce[cty] = {}
    key_couples_2 = coupes1_same[cty]
    cty_divorce[cty]["same"] = check_divorced_countywise(key_couples,key_couples_2)
    cty_divorce[cty]["diff"] = check_divorced_countywise(coupes_diff[cty],coupes1_diff[cty])
    



#Save results to file
f = open('div.json','w')
json.dump(cty_divorce,f)
f.close()