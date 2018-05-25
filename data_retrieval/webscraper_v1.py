from data_retrieval.url_processing import UrlProcessing

filename = "practice-nba-games.csv"
base_url = 'https://www.basketball-reference.com/boxscores/'
days_of_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def get_data(start_month, start_day, start_year, end_month, end_day, end_year):
    while start_month != end_month or start_day != end_day or start_year != end_year:
        url_data = update_url(start_month, start_day, start_year)
        new_url = url_data[0]
        print(new_url)
        UrlProcessing(new_url, filename)

        start_month = url_data[1]
        start_day = url_data[2] + 1
        start_year = url_data[3]


def update_url(month, day, year):
    if day > days_of_month[month - 1]:
        month += 1
        day = 1
    if month > 12:
        month = 1
        year += 1
    if month == 4 and day == 15:
        month = 10
        print("Starting Season: " + str(year))

    updated_url = base_url + '?month=' + str(month) + '&day=' + str(day) + '&year=' + str(year)

    return updated_url, month, day, year
