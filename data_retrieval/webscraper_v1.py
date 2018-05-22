from data_retrieval.url_processing import UrlProcessing
from data_retrieval.url_setup import UrlSetUp

filename = "practice-nba-games.csv"

# All of the 15-16 and 16-17 seasons
startMonth = 10
startDay = 30
startYear = 2012

endMonth = 4
endDay = 14
endYear = 2017

while startMonth != endMonth or startDay != endDay or startYear != endYear:
    new_url = UrlSetUp(startMonth, startDay, startYear)
    UrlProcessing(new_url.newUrl, filename)
    startMonth = new_url.month
    startDay = new_url.day + 1
    startYear = new_url.year

    print(new_url.newUrl)
