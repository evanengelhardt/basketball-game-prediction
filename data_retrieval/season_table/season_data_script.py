from data_retrieval import database_functions as dbs
import variables as var
from data_retrieval.season_table import season_webscraper as sws


def run_data_script():
    connect_dtls = dbs.connect_to_mysql()
    cnx = connect_dtls[0]
    cursor = connect_dtls[1]
    dbs.create_database(cursor, var.DB_NAME)
    print("Adding New Data in table: " + var.TABLE_NAME_SIMP)
    sws.get_data(cnx, cursor)
    dbs.close_cnx(cnx, cursor)
