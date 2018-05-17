from bs4 import BeautifulSoup as bSoup
from urllib.request import urlopen as ureq
from pathlib import Path


class UrlProcessing:

    def __init__(self, url, file_name):
        self.url = url
        self.file_name = file_name
        self.page_soup = self.prepare_url()
        self.f = self.prepare_file()
        self.team_stat_tables = self.page_soup.findAll("table", {"class": "stats_table"})
        self.process_games()

        self.f.close()

    def prepare_url(self):
        u_client = ureq(self.url)
        page_html = u_client.read()
        u_client.close()
        return bSoup(page_html, "html.parser")

    def prepare_file(self):
        file = Path("./" + self.file_name)
        if file.is_file():
            f = open(self.file_name, "a")
        else:
            f = open(self.file_name, "w")
            headers = "visitor-win-pct, visitor-ppg, visitor-oppg, home-win-pct, home-ppg, home-oppg, winner\n"
            f.write(headers)

        return f

    def process_games(self):
        containers = self.page_soup.findAll("div", {"class": "game_summary"})
        for container in containers:
            visitor_container = container.findAll("tr")[0]
            self.find_stats(visitor_container.td.a["href"])
            home_container = container.findAll("tr")[1]
            self.find_stats(home_container.td.a["href"])
            winner_container = container.findAll("tr", {"class" : "winner"})[0]
            if winner_container == visitor_container:
                self.f.write("v\n")
            else:
                self.f.write("h\n")
        return

    def find_stats(self, team_url):
        for team_stat_table in self.team_stat_tables:
            team_stat_containers = team_stat_table.findAll("tr", {"class": "full_table"})

            for team_stat_container in team_stat_containers:
                if team_url == team_stat_container.findAll("th", {"data-stat": "team_name"})[0].a["href"]:
                    team_wl = team_stat_container.findAll("td", {"data-stat": "win_loss_pct"})[0].text
                    team_pts_per_game = team_stat_container.findAll("td", {"data-stat": "pts_per_g"})[0].text
                    team_opp_pts_per_game = team_stat_container.findAll("td", {"data-stat": "opp_pts_per_g"})[0].text

                    self.f.write(str(team_wl) + "," + str(team_pts_per_game) + "," + str(team_opp_pts_per_game) + ",")
                    return
