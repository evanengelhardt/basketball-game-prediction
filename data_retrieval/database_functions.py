import mysql.connector as sql
from mysql.connector import errorcode
import config


TABLES = {}

TABLES[config.TABLE_NAME] = (
    "CREATE TABLE `" + config.TABLE_NAME + "` ("
    "   `game_no` int(11) NOT NULL AUTO_INCREMENT,"
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

insert_game = ("INSERT INTO " + config.TABLE_NAME + " (visitor_win_pct, visitor_ppg, visitor_oppg, home_win_pct, "
               "home_ppg, home_oppg, winner) VALUES (%s, %s, %s, %s, %s, %s, %s)")


def connect_to_mysql(db_name = None):
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
            else:
                print(err.msg)
        else:
            print("OK")


def add_game(cnx, cursor, info):
    cursor.execute(insert_game, info)
    cnx.commit()


def close_cnx(cnx, cursor):
    cursor.close()
    cnx.close()

