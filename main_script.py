import data_retrieval.data_script as data
import algorithms.logistic_main as logistic
import data_retrieval.database_functions as db

get_data = True
run_algorithm = False

if get_data:
    data.run_data_script()

if run_algorithm:
    cnx_dtls = db.connect_to_mysql()
    cnx = cnx_dtls[0]
    cursor = cnx_dtls[1]
    raw_data = db.get_games(cnx, cursor)

    logistic.run_logistic_reg(raw_data)
