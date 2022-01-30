# ScrapLabsForJobs

Simple tool that scraps LLNL, ORNL, LBL career pages for job title and links related to a single search word using Google Chrome.
Creates dataframe and saves as a .csv file.
Authored by Matthew Duribn (contact@matthewdurb.in)

Usage:
  $ python scrapLabsForJobs.py search-words
  
Dependencies
  - selenium
  - pandas
  - cromedriver in directory (https://chromedriver.chromium.org/downloads)

To Do
  - clean up xpaths
  - optimize delays (sleep) for iterating through pages
  - add other labs
