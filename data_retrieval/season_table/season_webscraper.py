import variables as var
from data_retrieval.season_table.season_url_processing import UrlProcessing


def get_data(cnx, cursor):
    start_month, start_day, start_year = var.START_DATE['month'], var.START_DATE['day'], var.START_DATE['year']
    is_first = True
    while start_month != var.END_DATE['month'] or start_day != var.END_DATE['day'] or start_year != var.END_DATE['year']:
        url_data = update_url(start_month, start_day, start_year)
        stat_year = setup_url_details(url_data[1], url_data[3])
        new_url = url_data[0]
        print(new_url)
        UrlProcessing(new_url, cnx, cursor, stat_year, url_data[4], is_first)
        is_first = False

        start_month = url_data[1]
        start_day = url_data[2] + 1
        start_year = url_data[3]


def update_url(month, day, year):
    is_new_season = False
    if day > var.DAYS_OF_MONTH[month - 1]:
        month += 1
        day = 1
    if month > 12:
        month = 1
        year += 1
    if month == 4 and day == 15:
        month = 10
        print("Starting Season: " + str(year))
        is_new_season = True

    updated_url = var.GAME_URL + '?month=' + str(month) + '&day=' + str(day) + '&year=' + str(year)

    return updated_url, month, day, year, is_new_season


def setup_url_details(month, year):
    if month < 5:
        return year
    else:
        return year + 1