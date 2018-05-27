from bs4 import BeautifulSoup as bSoup
from urllib.request import urlopen as ureq
import config
from urllib.error import HTTPError as error


def get_team_details(name, url_soup, isFor):
    name = config.TEAM_MAP[name]
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
    if isFor:
        return fgp, tfgp, tov, rpg, apg, spg, bpg
    else:
        return fgp, tfgp