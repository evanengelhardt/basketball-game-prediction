from data_retrieval.data_set_up import data_webscraper as sws
from data_retrieval.database import database_functions as dbs
from main import variables as var


def run_data_script():
    connect_dtls = dbs.connect_to_mysql()
    cnx = connect_dtls[0]
    cursor = connect_dtls[1]
    dbs.create_database(cursor, var.DB_NAME)
    print("Adding New Data in table: " + var.TABLE_NAME_SIMP)
    sws.get_data(cnx, cursor)
    combine_data(cnx, cursor)
    dbs.close_cnx(cnx, cursor)


def combine_data(cnx,cursor):
    dbs.add_tables(cnx, cursor, var.DB_NAME, True)
    curr_year = var.START_DATE['year'] + 1

    while curr_year <= var.END_DATE['year']:
        print("Starting year {}".format(str(curr_year)))
        game_count = dbs.get_game_count(cnx, cursor, curr_year)
        curr_game = 1
        while curr_game <= game_count:
            curr_game_info = dbs.get_game_by_no(cnx, cursor, curr_game, curr_year)
            visitor = curr_game_info[1]
            home = curr_game_info[2]
            new_entry = (curr_game_info[0],) + curr_game_info[3:-1]
            visitor_data = dbs.get_team(cnx, cursor, curr_year, visitor)[1:]
            home_data = dbs.get_team(cnx, cursor, curr_year, home)[1:]
            zipped_data = list(zip(visitor_data, home_data))
            for t in zipped_data:
                new_entry += t

            new_entry += (curr_game_info[-1],)
            dbs.add_game_comp(cnx,cursor, new_entry)
            print("Year: {} Game: {} added".format(str(curr_year), str(curr_game)))
            curr_game += 1

        curr_year += 1
