from bs4 import BeautifulSoup as bSoup
from urllib.request import urlopen as ureq
from urllib.error import HTTPError as error
from pathlib import Path
from data_retrieval import database_functions as dbs


class UrlProcessing:

    def __init__(self, url, cnx, cursor):
        self.retry_count = 0
        self.url = url
        self.cnx = cnx
        self.cursor = cursor
        self.page_soup = self.prepare_url(self.url)
        if self.page_soup:
            self.team_stat_tables = self.page_soup.findAll("table", {"class": "stats_table"})
            self.process_games()

    def prepare_url(self, url):
        try:
            u_client = ureq(url)
            page_html = u_client.read()
            u_client.close()
            return bSoup(page_html, "html.parser")
        except error:
            self.retry_count += 1
            if self.retry_count > 3:
                print("Exceeded retry count, skipping url")
                return None
            else:
                print("Error in preparing url, trying again")
                self.prepare_url()

    def process_games(self):
        containers = self.page_soup.findAll("div", {"class": "game_summary"})
        for container in containers:
            visitor_container = container.findAll("tr")[0]
            visitor_details = self.find_stats(visitor_container.td.a["href"])
            home_container = container.findAll("tr")[1]
            home_details = self.find_stats(home_container.td.a["href"])
            winner_container = container.findAll("tr", {"class" : "winner"})[0]
            if winner_container == visitor_container:
                winner = (0,)
            else:
                winner = (1,)

            data_entry = visitor_details + home_details + winner

            dbs.add_game(self.cnx, self.cursor, data_entry)
        return

    def find_stats(self, team_url):
        for team_stat_table in self.team_stat_tables:
            team_stat_containers = team_stat_table.findAll("tr", {"class": "full_table"})

            for team_stat_container in team_stat_containers:
                if team_url == team_stat_container.findAll("th", {"data-stat": "team_name"})[0].a["href"]:
                    team_wl = float(team_stat_container.findAll("td", {"data-stat": "win_loss_pct"})[0].text)
                    team_pts_per_game = round(float(team_stat_container
                                              .findAll("td", {"data-stat": "pts_per_g"})[0].text) / 100.0, 4)
                    team_opp_pts_per_game = round(float(team_stat_container
                                                  .findAll("td", {"data-stat": "opp_pts_per_g"})[0].text) / 100.0, 4)

                    return team_wl, team_pts_per_game, team_opp_pts_per_game
