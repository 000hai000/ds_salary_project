import pandas as pd
from selenium import webdriver
from time import sleep
from random import randint

DRIVER_PATH = '/Users/hainguyen/Python/ds_salary_project/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

df = pd.read_csv("indeed_ds_jobs.csv")

df = df.drop_duplicates()

descriptions=[]

links = df['Link']

for link in links:
    driver.get(link)
    description = driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text
    descriptions.append(description)
    sleep(randint(5, 15))
    
df['Description']=descriptions 

df.to_csv(r'/Users/hainguyen/Python/ds_salary_project/indeed_ds_jobs.csv', index=False, header=True)