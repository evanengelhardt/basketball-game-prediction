from data_retrieval import database_functions as dbs
import data_retrieval.webscraper_v1 as ws
import variables as var



connect_dtls = dbs.connect_to_mysql()
cnx = connect_dtls[0]
cursor = connect_dtls[1]
dbs.create_database(cursor, var.DB_NAME)
new_table = dbs.add_tables(cnx, cursor, var.DB_NAME, False)
print("Adding New Data in table: " + var.TABLE_NAME_SIMP)

dbs.add_season_tables(cnx, cursor, var.DB_NAME, var.START_DATE['year'] + 1)


ws.get_data(cnx, cursor, var.isComplex)

dbs.close_cnx(cnx, cursor)
