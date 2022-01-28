# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 09:39:48 2022

@author: matth
"""

from selenium import webdriver
from time import sleep
import sys
import pandas as pd


class LLNL:
    def __init__(self, search):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.llnl.gov/join-our-team/careers")
        sleep(1)
        
        self.driver.find_element_by_xpath("//a[contains(text(), 'Search jobs')]").click()
        self.driver.find_element_by_id("search-term").send_keys(search)
        self.driver.find_element_by_id("search-term-btn").click()        
        sleep(1)
        
    def get_jobs(self, close=True):
        titles = self.driver.find_elements_by_class_name("article-api-title")
        jobs = [job.find_element_by_css_selector('a').text for job in titles]
        links = [link.find_element_by_css_selector('a').get_attribute('href') for link in titles]
        
        if close == True:
            self.driver.close()
        return (jobs, links)
    
class ORNL:
    def __init__(self, search):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://jobs.ornl.gov/")
        sleep(1)
        
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div[2]/div/div/form/div/div[1]/div[1]/div[2]/input").send_keys(search)
        self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div[2]/div/div/form/div/div[1]/div[4]/div[2]/div/input").click()   
    
    def get_jobs(self, close=True):
        titles = self.driver.find_elements_by_class_name("colTitle")
        jobs = [job.find_element_by_css_selector('a').text for job in titles]
        links = [link.find_element_by_css_selector('a').get_attribute('href') for link in titles]
        
        if close == True:
            self.driver.close()
        return (jobs, links) 

#%%
search_term = sys.argv[1]
LLNL_Job_Bank = LLNL(search_term)
jobs_LLNL, links_LLNL = LLNL_Job_Bank.get_jobs()
ORNL_Job_Bank = ORNL(search_term)
jobs_ORNL, links_ORNL = ORNL_Job_Bank.get_jobs()

print(f"""There are: 
      {len(jobs_LLNL)} jobs at LLNL and
      {len(jobs_ORNL)} jobs at ORNL
      related to {search_term}""" )

jobs = jobs_LLNL + jobs_ORNL
links = links_LLNL + links_ORNL
labs = ['LLNL']*len(jobs_LLNL) + ['ORNL']*len(jobs_ORNL)


df = pd.DataFrame(zip(labs,jobs,links), columns=['Lab', 'Name', 'Link'])

df.to_csv(f'{search_term}_jobs.csv')
