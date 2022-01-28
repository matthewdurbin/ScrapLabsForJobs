# ScrapLabsForJobs

Simple tool that scraps LLNL and ORNL career pages for job title and links related to a single search word using Google Chrome.
Creates dataframe and saves as a .csv file.

Usage:
  $ python scrapLabsForJobs.py search-word
  
Dependencies
  - selenium
  - pandas
  - cromedriver in directory (https://chromedriver.chromium.org/downloads)

To Do
  - clean up xpaths
  - add next page feature
  - update for multi-word searches
  - add other labs
