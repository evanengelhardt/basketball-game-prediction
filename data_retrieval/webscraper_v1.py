from data_retrieval.url_processing import UrlProcessing
import variables as var

filename = "practice-nba-games.csv"
base_url = 'https://www.basketball-reference.com/boxscores/'
team_url = 'https://basketball.realgm.com/nba/team-stats/{}/Averages/Team_Totals/Regular_Season'
opp_url = 'https://basketball.realgm.com/nba/team-stats/{}/Averages/Opponent_Totals/Regular_Season'

days_of_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def get_data(cnx, cursor, isComplex):
    start_month, start_day, start_year = var.START_DATE['month'], var.START_DATE['day'], var.START_DATE['year']
    while start_month != var.END_DATE['month'] or start_day != var.END_DATE['day'] or start_year != var.END_DATE['year']:
        url_data = update_url(start_month, start_day, start_year)
        stat_year = setup_url_details(url_data[1], url_data[3])
        new_url = url_data[0]
        print(new_url)
        UrlProcessing(new_url, cnx, cursor, stat_year, team_url, opp_url, isComplex, new_url[4])

        start_month = url_data[1]
        start_day = url_data[2] + 1
        start_year = url_data[3]


def update_url(month, day, year):
    isNewSeason = False
    if day > days_of_month[month - 1]:
        month += 1
        day = 1
    if month > 12:
        month = 1
        year += 1
    if month == 4 and day == 15:
        month = 10
        print("Starting Season: " + str(year))
        isNewSeason = True

    updated_url = base_url + '?month=' + str(month) + '&day=' + str(day) + '&year=' + str(year)

    return updated_url, month, day, year, isNewSeason


def setup_url_details(month, year):
    if month < 5:
        return year
    else:
        return year + 1
