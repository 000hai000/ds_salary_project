import pandas as pd
import numpy as np
import copy

df_indeed = pd.read_csv('indeed_ds_jobs.csv')
df_indeed = df_indeed.drop_duplicates()
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
df_seek = df_seek.drop_duplicates()
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

#combining the 2 dataframes
df = pd.concat([df_indeed, df_seek])
df = df.reset_index(drop=True)

#Skills required
df['Python'] = df['Description'].apply(lambda x: True if 'python' in x.lower() else False)
df['R'] = df['Description'].apply(lambda x: True if ' r ' in x.lower() else False)
df['Spark'] = df['Description'].apply(lambda x: True if 'spark' in x.lower() else False)
df['SQL'] = df['Description'].apply(lambda x: True if 'sql' in x.lower() else False)
df['Excel'] = df['Description'].apply(lambda x: True if 'excel' in x.lower() or 'vba' in x.lower() else False)
df['AWS'] = df['Description'].apply(lambda x: True if 'amazon' in x.lower() or 'aws' in x.lower() else False)
df['Tableau'] = df['Description'].apply(lambda x: True if 'tableau' in x.lower() else False)

#Casual or part time
df['Part or Casual'] = df['Description'].apply(lambda x: True if 'part time' in x.lower() or 'part-time' in x.lower() or 'casual' in x.lower() else False)

#title simplifier
def title_simplifier(title):
    if 'data scientist' in title.lower() or 'data specialist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'data analyst'
    elif 'machine learning' in title.lower():
        return 'machine learning expert'
    elif 'software engineer' in title.lower():
        return 'software engineer'
    elif 'research' in title.lower() or 'researcher' in title.lower():
        return 'researcher'
    else:
        return 'None'
df['Simplified Title'] = df['Title'].apply(title_simplifier)

#job description length
df['Description Length'] = df['Description'].apply(lambda x: len(x))

#Formatting State
def state(location):
    if 'sydney' in location.lower() or 'nsw' in location.lower() or 'new south wales' in location.lower() or 'wollongong' in location.lower():
        return 'New South Wales'
    elif 'melbourne' in location.lower() or 'vic' in location.lower() or 'victoria' in location.lower():
        return 'Victoria'
    elif 'brisbane' in location.lower() or 'qld' in location.lower() or 'queensland' in location.lower() or 'toowoomba' in location.lower():
        return 'Queensland'
    elif 'perth' in location.lower() or 'wa' in location.lower() or 'western australia' in location.lower():
        return 'Western Australia'
    elif 'canberra' in location.lower() or 'act' in location.lower() or 'australian capital territory' in location.lower():
        return 'Australian Capital Territory'
    elif 'adelaide' in location.lower() or 'sa' in location.lower() or 'south australia' in location.lower():
        return 'South Australia'
    elif 'hobart' in location.lower() or 'tas' in location.lower() or 'tasmania' in location.lower():
        return 'Tasmania'
    else:
        return 'None'
df['State'] = df['Location'].apply(state)

#save as csv
df.to_csv(r'ds_jobs.csv', index=False, header=True)