import algorithms.logistic_main as logistic
import data_retrieval.data_set_up.data_script as season
import data_retrieval.database.database_functions as db
from main import variables as var

if var.GET_DATA:
    season.run_data_script()

if var.RUN_ALGO:
    cnx_dtls = db.connect_to_mysql()
    cnx = cnx_dtls[0]
    cursor = cnx_dtls[1]
    raw_data = db.get_games(cnx, cursor)

    logistic.run_logistic_reg(raw_data)
