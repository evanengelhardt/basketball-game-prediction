import mysql.connector as sql
from mysql.connector import errorcode
import config
import data_retrieval.dataloader as dl


TABLES = {}
# Simple Table Ops
"""
TABLES[config.TABLE_NAME] = (
    "CREATE TABLE `" + config.TABLE_NAME + "` ("
    "   `game_no` int(11) NOT NULL AUTO_INCREMENT,"
    "   `favorite` int NOT NULL,"
    "   `visitor_win_pct` float NOT NULL,"
    "   `visitor_ppg` float NOT NULL,"
    "   `visitor_oppg` float NOT NULL,"
    "   `home_win_pct` float NOT NULL,"
    "   `home_ppg` float NOT NULL,"
    "   `home_oppg` float NOT NULL,"
    "   `winner` int NOT NULL,"
    "   PRIMARY KEY (`game_no`)"
    ") ENGINE=InnoDB"
)

insert_game = ("INSERT INTO " + config.TABLE_NAME + " (favorite, visitor_win_pct, visitor_ppg, visitor_oppg, "
                "home_win_pct, home_ppg, home_oppg, winner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

select_game = ("SELECT favorite, visitor_win_pct, visitor_ppg, visitor_oppg, home_win_pct, home_ppg, home_oppg, winner "
               "FROM " + config.TABLE_NAME)
"""

# Detailed Table Ops
TABLES[config.TABLE_NAME] = (
    "CREATE TABLE `" + config.TABLE_NAME + "` ("
    "   `game_no` int(11) NOT NULL AUTO_INCREMENT,"
    "   `favorite` int NOT NULL,"
    "   `visitor_win_pct` float NOT NULL,"
    "   `home_win_pct` float NOT NULL,"
    "   `visitor_ppg` float NOT NULL,"
    "   `home_ppg` float NOT NULL,"
    "   `visitor_oppg` float NOT NULL,"
    "   `home_oppg` float NOT NULL,"
    "   `visitor_fgp` float NOT NULL,"
    "   `home_fgp` float NOT NULL,"
    "   `visitor_ofgp` float NOT NULL,"
    "   `home_ofgp` float NOT NULL,"
    "   `visitor_3fgp` float NOT NULL,"
    "   `home_3fgp` float NOT NULL,"
    "   `visitor_o3fgp` float NOT NULL,"
    "   `home_o3fgp` float NOT NULL,"
    "   `visitor_tov` float NOT NULL,"
    "   `home_tov` float NOT NULL,"
    "   `visitor_rpg` float NOT NULL,"
    "   `home_rpg` float NOT NULL,"
    "   `visitor_apg` float NOT NULL,"
    "   `home_apg` float NOT NULL,"
    "   `visitor_spg` float NOT NULL,"
    "   `home_spg` float NOT NULL,"
    "   `visitor_bpg` float NOT NULL,"
    "   `home_bpg` float NOT NULL,"
    "   `winner` int NOT NULL,"
    "   PRIMARY KEY (`game_no`)"
    ") ENGINE=InnoDB"
)

insert_game = ("INSERT INTO " + config.TABLE_NAME + " (favorite, visitor_win_pct, home_win_pct, visitor_ppg, home_ppg,"
                                                    " visitor_oppg, home_oppg, visitor_fgp, home_fgp, visitor_ofgp,"
                                                    " home_ofgp, visitor_3fgp, home_3fgp, visitor_o3fgp, home_o3fgp, "
                                                    " visitor_tov, home_tov, visitor_rpg, home_rpg, visitor_apg,"
                                                    " home_apg, visitor_spg, home_spg, visitor_bpg, home_bpg,"
                                                    " winner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                                                    " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

select_game = ("SELECT favorite, visitor_win_pct, home_win_pct, visitor_ppg, home_ppg,"
                                                " visitor_oppg, home_oppg, visitor_fgp, home_fgp, visitor_ofgp, "
                                                " home_ofgp, visitor_3fgp, home_3fgp, visitor_o3fgp, home_o3fgp, "
                                                " visitor_tov, home_tov, visitor_rpg, home_rpg, visitor_apg, "
                                                " home_apg, visitor_spg, home_spg, visitor_bpg, home_bpg, "
                                                " winner FROM " + config.TABLE_NAME)


def connect_to_mysql(db_name=None):
    if db_name is not None:
        cnx = sql.connect(user=config.MYSQL['user'], password=config.MYSQL['password'], host=config.MYSQL['host'], database=db_name)
    else:
        cnx = sql.connect(user=config.MYSQL['user'], password=config.MYSQL['password'], host=config.MYSQL['host'])
    cursor = cnx.cursor()
    return cnx, cursor


def create_database(cursor, db_name):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name)
        )
    except sql.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)


def add_tables(cnx, cursor, db_name):
    cnx.database = db_name
    for name, ddl in TABLES.items():
        try:
            print("Creating table {}: ".format(name), end='')
            cursor.execute(ddl)
        except sql.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
                return False
            else:
                print(err.msg)
        else:
            print("OK")
            return True


def add_game(cnx, cursor, info):
    cursor.execute(insert_game, info)
    cnx.commit()


def get_games(cnx, cursor):
    cnx.database = config.DB_NAME
    cursor.execute(select_game)
    results = cursor.fetchall()
    return results


def close_cnx(cnx, cursor):
    cursor.close()
    cnx.close()

