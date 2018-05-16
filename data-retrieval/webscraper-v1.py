from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

practice_schedule_url = 'https://www.basketball-reference.com/boxscores/?month=10&day=26&year=2016'

uClient = uReq(practice_schedule_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")


filename = "practice-nba-games.csv"
f = open(filename, "w")
headers = "winning-team, winning-points, losing-team, losing-points\n"
f.write(headers)

containers = page_soup.findAll("div", {"class": "game_summary"})

for container in containers:
    loser_container = container.findAll("tr", {"class": "loser"})
    loser_name = loser_container[0].td.a.text
    loser_score = loser_container[0].findAll("td", {"class": "right"})[0].text

    winner_container = container.findAll("tr", {"class": "winner"})
    winner_name = winner_container[0].td.a.text
    winner_score = winner_container[0].findAll("td", {"class": "right"})[0].text

    f.write(winner_name + "," + winner_score + "," + loser_name + "," + loser_score + "\n")

f.close()
