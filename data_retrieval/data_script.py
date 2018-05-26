from data_retrieval import database_functions as dbs
import config
import data_retrieval.webscraper_v1 as ws


def run_data_script():
    connect_dtls = dbs.connect_to_mysql()
    cnx = connect_dtls[0]
    cursor = connect_dtls[1]
    dbs.create_database(cursor, config.DB_NAME)
    new_table = dbs.add_tables(cnx, cursor, config.DB_NAME)
    if new_table:
        print("Adding New Data in table: " + config.TABLE_NAME)
        ws.get_data(10, 26, 2010, 4, 12, 2017, cnx, cursor)
    else:
        print("Table already exists, no new data being added")
    dbs.close_cnx(cnx, cursor)
