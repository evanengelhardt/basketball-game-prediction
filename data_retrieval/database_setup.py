import mysql.connector as sql
from mysql.connector import errorcode


TABLES = {}

TABLES['nba_basic'] = (
    "CREATE TABLE `nba_basic` ("
    "   `game_no` int(11) NOT NULL AUTO_INCREMENT,"
    "   `visitor_win_pct` float NOT NULL,"
    "   `visitor_ppg` float NOT NULL,"
    "   `visitor_oppg` float NOT NULL,"
    "   `home_win_pct` float NOT NULL,"
    "   `home_ppg` float NOT NULL,"
    "   `home_oppg` float NOT NULL,"
    "   PRIMARY KEY (`game_no`)"
    ") ENGINE=InnoDB"
)


def connect_to_mysql():
    cnx = sql.connect(user='root', password='Mydadsagirl', host='localhost')
    cursor = cnx.cursor()
    return cursor


def create_database(cursor, db_name):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name)
        )

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

    except sql.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)



