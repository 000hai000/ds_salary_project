import pandas as pd
import numpy as np
import copy

df_indeed = pd.read_csv('indeed_ds_jobs.csv')
df_indeed = df_indeed[df_indeed['Salary'] != 'None']
df_indeed = df_indeed.reset_index(drop=True)

#Removing all words
indeed_salary = df_indeed['Salary'].apply(lambda x: x.split('a')[0])
#Deleting all the $ sign
indeed_remove_sign = indeed_salary.apply(lambda x: x.replace('$', ''))
#removing all , and spaces
indeed_salary_formatted = indeed_remove_sign.apply(lambda x: x.replace(',', '').replace(' ', ''))

#getting minimum and maximum salary
df_indeed['Minimum Salary'] = indeed_salary_formatted.apply(lambda x: float((x.split('-'))[0]))
df_indeed['Maximum Salary'] = indeed_salary_formatted.apply(lambda x: float((x.split('-'))[-1]))
df_indeed['Average Salary'] = (df_indeed['Minimum Salary'] + df_indeed['Maximum Salary']) / 2

#formatting all salaries into annual
for i in range(len(df_indeed['Minimum Salary'])):
    if 'hour' in df_indeed['Salary'][i].lower():
        df_indeed.loc[i, 'Minimum Salary'] = df_indeed['Minimum Salary'][i] * 40 * 52
        df_indeed.loc[i, 'Maximum Salary'] = df_indeed['Maximum Salary'][i] * 40 * 52
        df_indeed.loc[i, 'Average Salary'] = df_indeed['Average Salary'][i] * 40 * 52
    if 'day' in df_indeed['Salary'][i].lower():
        df_indeed.loc[i, 'Minimum Salary'] = df_indeed['Minimum Salary'][i] * 7 * 52
        df_indeed.loc[i, 'Maximum Salary'] = df_indeed['Maximum Salary'][i] * 7 * 52
        df_indeed.loc[i, 'Average Salary'] = df_indeed['Average Salary'][i] * 7 * 52
        
df_seek = pd.read_csv('seek_ds_jobs.csv')
df_seek.fillna('None', inplace=True)
df_seek = df_seek[df_seek['Salary'] != 'None']
df_seek = df_seek[df_seek['Salary'].str.contains(r"[0-9]")]
df_seek = df_seek.reset_index(drop=True)

seek_salary = copy.deepcopy(df_seek['Salary'])

def remove_percentage_substring(string):
    res = string
    end = string.find("%")
    for i in range(end, -1, -1):
        if string[i] == " ":
            stop = i
            res = string[0:stop]
            break
    return res

for i in range(len(seek_salary)):
    seek_salary[i] = remove_percentage_substring(seek_salary[i])
    
#Replacing any words that has a k 
seek_salary = seek_salary.str.lower()
seek_salary = seek_salary.str.replace("parking", "")
seek_salary = seek_salary.str.replace("package", "")
seek_salary = seek_salary.str.replace("pack", "")
        
# Changing all k's to 000
seek_salary = seek_salary.str.replace(r"[kK]", "000")
       
# Removing all words
seek_salary = seek_salary.str.replace(r"[a-z]", "")
seek_salary = seek_salary.str.replace(r"[A-Z]", "")
    
#Remove anything but numbers, $, . and -
seek_salary = seek_salary.str.replace(r"[^0-9$.-]+", "")

df_seek['Salary'] = seek_salary
df_seek = df_seek[df_seek['Salary'].str.contains(r"[$]")]
df_seek = df_seek.reset_index(drop=True)

seek_salary = copy.deepcopy(df_seek['Salary'])
                  
def slicer(my_str,sub):
    index=my_str.find(sub)
    if index !=-1:
        return my_str[index:] 
    
def remove_decimal_point(string):
    res = string
    if string[-1] == ".":
        res = res.rstrip(".")
    return res

for i in range(len(seek_salary)):
    #removing all characters that dont start with $
    seek_salary[i] = slicer(seek_salary[i], "$")
    #removing all random decimal points
    seek_salary[i] = remove_decimal_point(seek_salary[i])
    seek_salary[i] = seek_salary[i].split("..")[0]

#Changing all $ into - then removing all - duplicates
seek_salary = seek_salary.str.replace("$", "-")

def remove_divider(string):
    res = string
    if res[0] == "-":
        res = res[1:]
    if res[-1] == "-":
        res = res[0:-1]
    for i in range(len(res) - 1):
        if res[i] == "-" and res[i + 1] == "-":
            res = res[0:i] + res[i + 1:]
    return res

for i in range(len(seek_salary)):
    seek_salary[i] = remove_divider(seek_salary[i])
    if seek_salary[i][0] == "-":
        seek_salary[i] = seek_salary[i][1:]
        
df_seek['Minimum Salary'] = seek_salary.apply(lambda x: float((x.split('-'))[0]))
df_seek['Maximum Salary'] = seek_salary.apply(lambda x: float((x.split('-'))[-1]))
df_seek['Average Salary'] = (df_seek['Minimum Salary'] + df_seek['Maximum Salary']) / 2

#formatting all salaries into annual plus superannuation
hourly = ['hour', 'p.h.']
daily = ['day', 'p.d.', 'p\d', 'p/d']
superannuation = ['super', 'superannuation']
includesuper = ['inc', 'inclusive', 'include']
for i in range(len(df_seek['Minimum Salary'])):
    if any(word in df_seek['Salary'][i].lower() for word in hourly):
        df_seek.loc[i, 'Minimum Salary'] = df_seek['Minimum Salary'][i] * 40 * 52
        df_seek.loc[i, 'Maximum Salary'] = df_seek['Maximum Salary'][i] * 40 * 52
        df_seek.loc[i, 'Average Salary'] = df_seek['Average Salary'][i] * 40 * 52
    if any(word in df_seek['Salary'][i].lower() for word in daily):
        df_seek.loc[i, 'Minimum Salary'] = df_seek['Minimum Salary'][i] * 7 * 52
        df_seek.loc[i, 'Maximum Salary'] = df_seek['Maximum Salary'][i] * 7 * 52
        df_seek.loc[i, 'Average Salary'] = df_seek['Average Salary'][i] * 7 * 52
    if any(word in df_seek['Salary'][i].lower() for word in superannuation):
        df_seek.loc[i, 'Minimum Salary'] = df_seek['Minimum Salary'][i] * 1.095
        df_seek.loc[i, 'Maximum Salary'] = df_seek['Maximum Salary'][i] * 1.095
        df_seek.loc[i, 'Average Salary'] = df_seek['Average Salary'][i] * 1.095
    if any(word in df_seek['Salary'][i].lower() for word in includesuper):
        df_seek.loc[i, 'Minimum Salary'] = df_seek['Minimum Salary'][i] / 1.095
        df_seek.loc[i, 'Maximum Salary'] = df_seek['Maximum Salary'][i] / 1.095
        df_seek.loc[i, 'Average Salary'] = df_seek['Average Salary'][i] / 1.095

#removing anomalies
df_seek = df_seek[df_seek['Minimum Salary'] > 10000]
df_seek = df_seek[df_seek['Maximum Salary'] > 10000]
df_seek = df_seek[df_seek['Minimum Salary'] < 2000000]
df_seek = df_seek[df_seek['Maximum Salary'] < 2000000]

df = pd.concat([df_indeed, df_seek])
df = df.reset_index(drop=True)