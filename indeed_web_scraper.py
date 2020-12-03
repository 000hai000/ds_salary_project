from selenium import webdriver

DRIVER_PATH = '/Users/hainguyen/Python/ds_salary_project/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

driver.get('https://au.indeed.com')

search_job = driver.find_element_by_xpath('//input[@id="text-input-what"]')
search_job.send_keys(['data scientist'])

search_location = driver.find_element_by_xpath('//*[@id="text-input-where"]')
search_location.send_keys(['victoria'])

initial_search_button = driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button')
initial_search_button.click()

driver.implicitly_wait(3) 

titles=[]
companies=[]
locations=[]
links =[]
reviews=[]
salaries = []
descriptions=[]

for i in range(0,1):
    
    job_card = driver.find_elements_by_xpath('//div[contains(@class,"clickcard")]')
    
    for job in job_card:
       
        try:
            title  = job.find_element_by_xpath('.//h2[@class="title"]//a').text
        except:
            title = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="title")
        titles.append(title)
        
        try:
            company = job.find_element_by_xpath('.//span[@class="company"]').text
        except:
            company = "None"
        companies.append(company)
        
        try:
            location = job.find_element_by_xpath('.//span[contains(@class,"location")]').text
        except:
            location = "None"      
        locations.append(location)
        
        try:
            link = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="href")
        except:
            link = "None"
        links.append(link)
        
        try:
            review = job.find_element_by_xpath('.//span[@class="ratingsContent"]').text
        except:
            review = "None"
        reviews.append(review)

        try:
            salary = job.find_element_by_xpath('.//span[@class="salaryText"]').text
        except:
            salary = "None"      
        salaries.append(salary)
    
    try:
        next_page = driver.find_element_by_xpath('//a[@aria-label={}]//span[@class="pn"]'.format(i+2))
        next_page.click()

    except:
        next_page = driver.find_element_by_xpath('//a[@aria-label="Next"]//span[@class="np"]')
        next_page.click()
        
    print("Page: {}".format(str(i+2)))
    
for link in links:
    
    driver.get(link)
    jd = driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text
    descriptions.append(jd)
    
import pandas as pd
df=pd.DataFrame()
df['Title']=titles
df['Company']=companies
df['Location']=locations
df['Link']=links
df['Review']=reviews
df['Salary']=salaries
df['Description']=descriptions

df.to_csv(r'/Users/hainguyen/Python/ds_salary_project/indeed_ds_jobs.csv', index=False, header=True)