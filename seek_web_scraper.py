from selenium import webdriver
from time import sleep
from random import randint

DRIVER_PATH = '/Users/hainguyen/Python/ds_salary_project/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

driver.get('https://www.seek.com.au')

search_job = driver.find_element_by_xpath('//*[@id="keywords-input"]')
search_job.send_keys(['data science'])

search_location = driver.find_element_by_xpath('//*[@id="SearchBar__Where"]')
search_location.send_keys(['All Australia']) 

initial_search_button = driver.find_element_by_xpath('//*[@id="SearchBar"]/button')
initial_search_button.click()

driver.implicitly_wait(3) 

titles=[]
companies=[]
locations=[]
links=[]
reviews=[]
salaries=[]
descriptions=[]

for i in range(0,93):
    
    job_card = driver.find_elements_by_xpath('//div[contains(@data-search-sol-meta,"searchRequestToken")]')
    
    for job in job_card:
       
        try:
            title = job.find_element_by_xpath('.//h1//a[@data-automation="jobTitle"]').text
        except:
            title = "None"
        titles.append(title)
        
        try:
            company = job.find_element_by_xpath('.//span//a[@data-automation="jobCompany"]').text
        except:
            company = "None"
        companies.append(company)
        
        try:
            location = job.find_element_by_xpath('.//span//a[@data-automation="jobLocation"]').text
        except:
            location = "None"      
        locations.append(location)
        
        try:
            link = job.find_element_by_xpath('.//h1//a[@data-automation="jobTitle"]').get_attribute(name="href")
        except:
            link = "None"
        links.append(link)
        
        try:
            salary = job.find_element_by_xpath('.//span[@data-automation="jobSalary"]').text
        except:
            salary = "None"
        salaries.append(salary)
        
    next_page = driver.find_element_by_xpath('//a[@data-automation="page-next"]'.format(i+2))
    next_page.click()
        
    print("Page: {}".format(str(i+2)))
    sleep(randint(3, 10))
    
import pandas as pd
df=pd.DataFrame()
df['Title']=titles
df['Company']=companies
df['Location']=locations
df['Link']=links
df['Salary']=salaries

df = df.drop_duplicates()

links = df['Link']
for link in links:
    driver.get(link)
    
    try:
        review = driver.find_element_by_xpath('//span[@class="_1erK2ob"]').text
    except:
        review = "None"
    reviews.append(review)
    
    try:
        description = driver.find_element_by_xpath('//div[@data-automation="jobDescription"]').text
    except:
        description = "None"
    descriptions.append(description)
    
    sleep(randint(3, 10))

df['Review']=reviews
df['Description']=descriptions 

df.to_csv(r'seek_ds_jobs.csv', index=False, header=True)