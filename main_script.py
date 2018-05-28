import data_retrieval.season_table.season_data_script as season
import data_retrieval.detail_table.detail_data_script as detailed
import algorithms.logistic_main as logistic
import data_retrieval.database_functions as db
import variables as var


if var.GET_DATA:
    if var.TYPE_OF_TABLES is 'season':
        season.run_data_script()
    else:
        detailed.run_data_script()


if var.RUN_ALGO:
    cnx_dtls = db.connect_to_mysql()
    cnx = cnx_dtls[0]
    cursor = cnx_dtls[1]
    raw_data = db.get_games(cnx, cursor)

    logistic.run_logistic_reg(raw_data)
