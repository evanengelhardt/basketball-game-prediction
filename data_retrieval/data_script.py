from data_retrieval import database_functions as dbs
from data_retrieval import webscraper_v1 as ws
import config

connect_dtls = dbs.connect_to_mysql()
cnx = connect_dtls[0]
cursor = connect_dtls[1]
dbs.create_database(cursor, config.DB_NAME)
dbs.add_tables(cnx, cursor, config.DB_NAME)

ws.get_data(10, 30, 2015, 4, 1, 2016, cnx, cursor)
dbs.close_cnx(cnx, cursor)