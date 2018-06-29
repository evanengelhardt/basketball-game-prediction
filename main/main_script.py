import algorithms.logistic_regression.logistic_script as logistic
import algorithms.neural_net.neural_net_script as nn_script
import data_retrieval.data_set_up.data_script as season
import data_retrieval.database.database_functions as db
from main import variables as var

if var.GET_DATA:
    season.run_data_script()

if var.RUN_ALGO:
    cnx_dtls = db.connect_to_mysql()
    cnx = cnx_dtls[0]
    cursor = cnx_dtls[1]
    raw_data = db.get_games_comp(cnx, cursor)
    db.close_cnx(cnx, cursor)

    #logistic.run_logistic_reg(raw_data)
    nn_script.run_neural_net(raw_data, [23, 6, 1])
