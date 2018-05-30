import global_functions as g_func
import variables as var
from data_retrieval.database import database_functions as dbs


class UrlProcessing:

    def __init__(self, url, cnx, cursor, stat_year, is_new_year, is_first):
        self.retry_count = 0
        self.stat_year = stat_year
        self.url = url
        self.cnx = cnx
        self.cursor = cursor
        self.page_soup = g_func.prepare_url(self.url)
        self.team_detail_soup = g_func.prepare_url(var.TEAM_URL.format(self.stat_year))
        self.opponent_detail_soup = g_func.prepare_url(var.OPP_URL.format(self.stat_year))
        if is_new_year is True or is_first is True:
            dbs.add_season_tables(self.cnx, self.cursor, var.DB_NAME, self.stat_year)
            dbs.add_tables(self.cnx, self.cursor, var.DB_NAME, False, self.stat_year)
            self.find_season_stats()
        if self.page_soup is not None:
            self.team_stat_tables = self.page_soup.findAll("table", {"class": "stats_table"})
            self.process_games()

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

            data_entry = favorite + zipped[0] + zipped[1] + zipped[2] + zipped[3] + winner

            print(data_entry)

            dbs.add_game_simp(self.cnx, self.cursor, data_entry, self.stat_year)

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

                    return team_name, team_wl, team_pts_per_game, team_opp_pts_per_game

    def find_season_stats(self):
        info = self.team_detail_soup.findAll("table", {"class": "tablesaw"})[0].findAll("tbody")[0].findAll("tr")
        for team in info:
            team_name = team.findAll("a")[0].text
            team_details = self.get_team_details(team_name, self.team_detail_soup, True)
            opp_team_details = self.get_team_details(team_name, self.opponent_detail_soup, False)

            curr_team = team_name, team_details[0], opp_team_details[0], team_details[1], opp_team_details[1],\
                          team_details[2], team_details[3], team_details[4], team_details[5], team_details[6]

            print(curr_team)

            dbs.add_team(self.cnx, self.cursor, curr_team, self.stat_year)

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
