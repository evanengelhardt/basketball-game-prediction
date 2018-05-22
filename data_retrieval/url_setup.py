class UrlSetUp:

    def __init__(self, month, day, year):
        self.newUrl = 'https://www.basketball-reference.com/boxscores/'
        self.month = month
        self.day = day
        self.year = year
        self.month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.update_date()
        self.update_url()

    def update_date(self):
        if self.day > self.month_day[self.month - 1]:
            self.month += 1
            self.day = 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        if self.month == 4 and self.day == 15:
            self.month = 10
            print("Starting Season: " + str(self.year))

    def update_url(self):
        self.newUrl += '?month=' + str(self.month) + '&day=' + str(self.day) + '&year=' + str(self.year)
