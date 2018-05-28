from bs4 import BeautifulSoup as bSoup
from urllib.request import urlopen as ureq
from urllib.error import HTTPError as error
from data_retrieval import database_functions as dbs
import data_retrieval.detail_webscraper as dws
import variables as var
import global_functions as g_func

class UrlProcessing:

    def __init__(self, url, cnx, cursor, stat_year):
        self.stat_year = stat_year
        self.retry_count = 0
        self.url = url
        self.cnx = cnx
        self.cursor = cursor
        self.page_soup = g_func.prepare_url(self.url)
        self.team_detail_soup = g_func.prepare_url(var.TEAM_URL.format(self.stat_year))
        self.opponent_detail_soup = g_func.prepare_url(var.OPP_URL.format(self.stat_year))
        if self.page_soup is not None:
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
            visitor_details = self.find_stats(visitor_container.td.a)
            home_container = container.findAll("tr")[1]
            home_details = self.find_stats(home_container.td.a)
            winner_container = container.findAll("tr", {"class": "winner"})[0]
            if winner_container == visitor_container:
                winner = (0,)
            else:
                winner = (1,)

            if visitor_details[0] > home_details[0]:
                favorite = (0,)
            else:
                favorite = (1,)

            zipped = list(zip(visitor_details, home_details))

            data_entry = favorite + zipped[0] + zipped[1] + zipped[2] + zipped[3] + zipped[4] + zipped[5] + \
                zipped[6] + zipped[7] + zipped[8] + zipped[9] + zipped[10] + zipped[11] + winner
            dbs.add_game_comp(self.cnx, self.cursor, data_entry)

        return

    def find_stats(self, team_url):
        team_name = team_url.text
        team_url = team_url['href']
        for team_stat_table in self.team_stat_tables:
            team_stat_containers = team_stat_table.findAll("tr", {"class": "full_table"})

            for team_stat_container in team_stat_containers:
                if team_url == team_stat_container.findAll("th", {"data-stat": "team_name"})[0].a["href"]:
                    team_wl = float(team_stat_container.findAll("td", {"data-stat": "win_loss_pct"})[0].text)
                    team_pts_per_game = round(float(team_stat_container
                                              .findAll("td", {"data-stat": "pts_per_g"})[0].text) / 100.0, 4)
                    team_opp_pts_per_game = round(float(team_stat_container
                                                  .findAll("td", {"data-stat": "opp_pts_per_g"})[0].text) / 100.0, 4)

                    team_details = self.get_team_details(team_name, self.team_detail_soup, True)
                    opp_team_details = self.get_team_details(team_name, self.opponent_detail_soup, False)

                    return team_wl, team_pts_per_game, team_opp_pts_per_game, team_details[0], opp_team_details[0],\
                           team_details[1], opp_team_details[1], team_details[2], team_details[3], team_details[4],\
                           team_details[5], team_details[6]

    def get_team_details(self, name, url_soup, is_team):
        name = var.TEAM_MAP[name]
        table = url_soup.findAll("table", {"class": "tablesaw"})[0].findAll("tbody")[0].findAll("tr")

        for i in range(len(table)):
            current_team = table[i]
            if current_team.findAll("a")[0].text == name:
                fgp = float(current_team.findAll("td")[6].text)
                tfgp = float(current_team.findAll("td")[9].text)
                tov = float(current_team.findAll("td")[13].text)
                rpg = float(current_team.findAll("td")[17].text)
                apg = float(current_team.findAll("td")[18].text)
                spg = float(current_team.findAll("td")[19].text)
                bpg = float(current_team.findAll("td")[20].text)
        if is_team:
            return fgp, tfgp, tov, rpg, apg, spg, bpg
        else:
            return fgp, tfgp

