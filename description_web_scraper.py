import pandas as pd
from selenium import webdriver
from time import sleep
from random import randint

DRIVER_PATH = '/Users/hainguyen/Python/ds_salary_project/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

driver.get('https://au.indeed.com')

search_job = driver.find_element_by_xpath('//input[@id="text-input-what"]')
search_job.send_keys(['data science'])

search_location = driver.find_element_by_xpath('//*[@id="text-input-where"]')
search_location.send_keys(['victoria'])

initial_search_button = driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button')
initial_search_button.click()

driver.implicitly_wait(3) 

df = pd.read_csv("indeed_ds_jobs.csv")
descriptions=[]
links = df['Link']
for link in links:
    
    driver.get(link)
    description = driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text
    descriptions.append(description)
    
    sleep(randint(1, 5))
    
df['Description']=descriptions