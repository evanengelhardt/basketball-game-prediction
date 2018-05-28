from data_retrieval import database_functions as dbs
import variables as var
from data_retrieval.detail_table import detail_webscraper as dws


def run_data_script():
    connect_dtls = dbs.connect_to_mysql()
    cnx = connect_dtls[0]
    cursor = connect_dtls[1]
    dbs.create_database(cursor, var.DB_NAME)
    new_table = dbs.add_tables(cnx, cursor, var.DB_NAME, True)
    if new_table:
        print("Adding New Data in table: " + var.TABLE_NAME_DETAILED)
        dws.get_data(cnx, cursor)
    else:
        print("Table already exists, no new data being added")
    dbs.close_cnx(cnx, cursor)
