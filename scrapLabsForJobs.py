# -*- coding: utf-8 -*-
"""  Lab Jobs Scrapper

Scraps LLNL, ORNL, and LBL for jobs based on key word(s).
Saves jobs and their links to a csv via a pandas dataframe.

dependencies:
    selenium
    pandas
    chrome driver in active directory (for windows)
    
usage: python scrapLabsForJobs.py keyword (keywords) 

* sleep needs may vary based on internet speed

@author: Matthew Durbin, contact@matthewdurb.in
"""

from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--incognito")
from time import sleep
import sys
import pandas as pd


class LLNL:
    """ Scrapper for LLNL jobs related to key word(s)
    
    Parameters
    ----------
    search: string
        key word(s) to search for
        
    Notes
    -----
    Carrer URL hard plgued into __init__ fuction
    xpath ways et.al. aquired 1/28/2022
    """
    def __init__(self, search):
        """ Initialized and searches

        Parameters
        ----------
        search : string
            keyword(s) to search for
        """
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get("https://www.llnl.gov/join-our-team/careers/find-your-job")
        sleep(1)

        # self.driver.find_element_by_xpath(
        #     "//a[contains(text(), 'Search jobs')]"
        # ).click()
        self.driver.find_element_by_id("search-term").send_keys(search)
        self.driver.find_element_by_id("search-term-btn").click()
        sleep(1)

    def get_jobs(self, close=True):
        """ Scraps search page for jobs       

        Parameters
        ----------
        close: bool, default = True
            closes browser after scrapping
            

        Returns
        -------
        jobs : list
            job names
        links : list
            links to those jobs
        """
        titles = self.driver.find_elements_by_class_name("article-api-title")
        jobs = [job.find_element_by_css_selector("a").text for job in titles]
        links = [
            link.find_element_by_css_selector("a").get_attribute("href")
            for link in titles
        ]

        if close == True:
            self.driver.close()
        return (jobs, links)


class ORNL:
    """ Scrapper for ORNL jobs related to key word(s)
    
    Parameters
    ----------
    search: string
        key word(s) to search for
        
    Notes
    -----
    Carrer URL hard plgued into __init__ fuction
    xpath ways et.al. aquired 1/28/2022
    """
    def __init__(self, search):
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get("https://jobs.ornl.gov/")
        sleep(1)

        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div[2]/div/div/form/div/div[1]/div[1]/div[2]/input"
        ).send_keys(search)
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div/div/div[2]/div/div/form/div/div[1]/div[4]/div[2]/div/input"
        ).click()
        sleep(1)
        
    def _page(self):
        """gives range of current page and total results

        Returns
        -------
        results : string
            range of results on current page
        of : string
            total results
        """
        page_label=self.driver.find_element_by_class_name("paginationLabel")
        results_of =page_label.find_elements_by_css_selector("b")
        results=results_of[0].text
        of=results_of[1].text
        return (results, of)
    
    def _get_jobs_from_page(self):
        """ Scraps search page for jobs                

        Returns
        -------
        jobs : list
            job names from page
        links : list
            links to those jobs 
        """
        titles = self.driver.find_elements_by_class_name("colTitle")
        jobs = [job.find_element_by_css_selector("a").text for job in titles]
        links = [
            link.find_element_by_css_selector("a").get_attribute("href")
            for link in titles
        ]
        return (jobs, links)

    def get_jobs(self, close=True):
        """ scraps each page        

        Parameters
        ----------
        close: bool, default = True
            closes browser after scrappin

        Returns
        -------
        jobs : list
            job names
        links : list
            links to those jobs 
        """
        jobs, links = self._get_jobs_from_page()
        results, of = self._page()
        page = 1
        while not int(results[-3:]) == int(of):
            sleep(2)
            page += 1
            self.driver.find_element_by_xpath(f"//a[@title='Page {page}']").click()
            job, link = self._get_jobs_from_page()
            jobs, links = jobs + job, links + link
            results, of = self._page()

        if close == True:
            self.driver.close()
        return (jobs, links)

class LBL:
    """ Scrapper for LBL jobs related to key word(s)
    
    Parameters
    ----------
    search: string
        key word(s) to search for
        
    Notes
    -----
    Carrer URL hard plgued into __init__ fuction
    xpath ways et.al. aquired 1/28/2022
    """
    def __init__(self, search):
        """ Initialized and searches

        Parameters
        ----------
        search : string
            keyword(s) to search for
        """
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get("https://jobs.lbl.gov/")
        sleep(1)

        self.driver.find_element_by_id("keyword").send_keys(search)
        self.driver.find_element_by_xpath(
            "/html/body/div[5]/div/div[2]/div[1]/div[4]/div/div/div/div[1]/div[2]/button/span[2]"
        ).click()
        sleep(1)

    def _get_jobs_from_page(self):
        """ Scraps search page for jobs                

        Returns
        -------
        jobs : list
            job names from page
        links : list
            links to those jobs 
        """
        titles = self.driver.find_elements_by_class_name("jlr_title")
        jobs_p = [job.find_element_by_css_selector("a").text for job in titles]
        links_p = [
            link.find_element_by_css_selector("a").get_attribute("href")
            for link in titles
        ]
        return (jobs_p, links_p)
    
    def get_jobs(self, close=True):
        """ scraps each page        

        Parameters
        ----------
        close: bool, default = True
            closes browser after scrappin

        Returns
        -------
        jobs : list
            job names
        links : list
            links to those jobs 
        """
        sleep(2)
        jobs, links = self._get_jobs_from_page()
        total_results = int(self.driver.find_element_by_class_name("total_results").text)
        res_per_page = 10
        pages = int(total_results/res_per_page) + 1
        page = 1
        while not page == pages:
            sleep(2)
            self.driver.find_element_by_class_name("next").click()
            page += 1
            job, link = self._get_jobs_from_page()
            jobs, links = jobs + job, links + link          

        if close == True:
            self.driver.close()
        return (jobs, links)

################# main script ######################
###  Takes in argument(s) as key word(s), makes  ###
###  dictionary of labs to scrap through. Saves  ###
###  as a csv via a pandas df.                   ###
####################################################
search_term = " ".join(sys.argv[1:])
labs_to_run = {"LLNL": LLNL, "ORNL": ORNL, "LBL": LBL}

jobs, links, labs = [], [], []
for lab in labs_to_run:
    print(f"Searching {lab} for jobs...")
    lab_class = labs_to_run[lab]
    job_bank = lab_class(search_term)
    job, link = job_bank.get_jobs()
    jobs = jobs + job
    links = links + link
    labs = labs + [lab] * len(job)

df = pd.DataFrame(zip(labs, jobs, links), columns=["Lab", "Job_Name", "Link"])
# LBL saves links from previouis page on current page. This removes dublicate links
df = df[df.Job_Name != ''].reset_index().drop(columns='index')
print(len(df), ' total jobs found')
df.to_csv(f"{search_term} jobs.csv")
