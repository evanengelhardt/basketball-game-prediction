from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

practice_schedule_url = 'https://www.basketball-reference.com/boxscores/?month=10&day=26&year=2016'

uClient = uReq(practice_schedule_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")


filename = "practice-nba-games.csv"
f = open(filename, "w")
headers = "visitor-win-pct, visitor-ppg, visitor-oppg, home-win-pct, home-ppg, home-oppg, winner\n"
f.write(headers)

containers = page_soup.findAll("div", {"class": "game_summary"})

team_stat_tables = page_soup.findAll("table", {"class": "stats_table"})


def find_stats(team_url):
    for team_stat_table in team_stat_tables:
        team_stat_containers = team_stat_table.findAll("tr", {"class": "full_table"})

        for team_stat_container in team_stat_containers:
            if team_url == team_stat_container.findAll("th", {"data-stat": "team_name"})[0].a["href"]:
                team_wl = team_stat_container.findAll("td", {"data-stat": "win_loss_pct"})[0].text
                team_pts_per_game = team_stat_container.findAll("td", {"data-stat": "pts_per_g"})[0].text
                team_opp_pts_per_game = team_stat_container.findAll("td", {"data-stat": "opp_pts_per_g"})[0].text

                f.write(str(team_wl) + "," + str(team_pts_per_game) + "," + str(team_opp_pts_per_game) + ",")
                return


for container in containers:
    visitor_container = container.findAll("tr")[0]
    find_stats(visitor_container.td.a["href"])

    home_container = container.findAll("tr")[1]
    find_stats(home_container.td.a["href"])

    winner_container = container.findAll("tr", {"class" : "winner"})[0]

    if winner_container == visitor_container:
        f.write("v\n")
    else:
        f.write("h\n")

f.close()
