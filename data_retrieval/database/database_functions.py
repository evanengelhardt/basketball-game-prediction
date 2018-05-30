import mysql.connector as sql
from mysql.connector import errorcode

from main import variables as var, config

TABLES = {}
# Simple Table Ops

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
            print("database already exists.")
        else:
            print(err.msg)


def add_tables(cnx, cursor, db_name, isDetailed, year=None):
    cnx.database = db_name
    if isDetailed:
        TABLES[var.TABLE_NAME_DETAILED] = var.LARGE_TABLE['create_main_table'].format(var.TABLE_NAME_DETAILED
                                                                                      + str(var.START_DATE['year']) +
                                                                                      "_" + str(var.END_DATE['year']))
    else:
        TABLES[var.TABLE_NAME_SIMP] = var.SIMPLE_TABLE['create_main_table'].format(var.TABLE_NAME_SIMP + str(year))
    for name, ddl in TABLES.items():
        try:
            print("Creating table {}: ".format(name), end='')
            cursor.execute(ddl)
        except sql.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("game table already exists.")
                return False
            else:
                print(err.msg)
        else:
            print("OK")
            return True


def add_season_tables(cnx, cursor, db_name, year):
    cnx.database = db_name
    create_sql = var.TEAM_TABLE['create_team_table'].format(var.SEASON_TABLE_NAME + str(year))
    try:
        print("Creating season table: {} ".format(year))
        cursor.execute(create_sql)
    except sql.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
            return False
        else:
            print(err.msg)
    else:
        print("OK")
        return True


def add_game_comp(cnx, cursor, info):
    cursor.execute(var.LARGE_TABLE['insert_game'].format(var.TABLE_NAME_DETAILED + str(var.START_DATE['year']) + "_"
                                                         + str(var.END_DATE['year'])), info)
    cnx.commit()


def get_games_comp(cnx, cursor):
    cnx.database = var.DB_NAME
    cursor.execute(var.LARGE_TABLE['select_game'].format(var.TABLE_NAME_DETAILED + str(var.START_DATE['year']) + "_" +
                                                         str(var.END_DATE['year'])))
    results = cursor.fetchall()
    return results


def get_game_by_no(cnx, cursor, game_no, year):
    cnx.database = var.DB_NAME
    cursor.execute(var.SIMPLE_TABLE['select_game_no'].format(var.TABLE_NAME_SIMP+str(year), game_no))
    results = cursor.fetchall()
    return results[0]

def get_game_count(cnx, cursor, year):
    cnx.database = var.DB_NAME
    cursor.execute(var.SIMPLE_TABLE['game_count'].format(var.TABLE_NAME_SIMP + str(year)))
    results = cursor.fetchall()
    return results[0][0]

def add_game_simp(cnx, cursor, info, year):
    cursor.execute(var.SIMPLE_TABLE['insert_game'].format(var.TABLE_NAME_SIMP + str(year)), info)
    cnx.commit()


def get_games_simp(cnx, cursor, year):
    cnx.database = var.DB_NAME
    cursor.execute(var.SIMPLE_TABLE['select_game'].format(var.TABLE_NAME_SIMP + str(year)))
    results = cursor.fetchall()
    return results


def add_team(cnx, cursor, info, year):
    try:
        cursor.execute(var.TEAM_TABLE['insert_team'].format(var.SEASON_TABLE_NAME + str(year)), info)
    except sql.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("team already exists.")
            return False
        else:
            print(err.msg)
    cnx.commit()


def get_team(cnx, cursor, year, team):
    if team in var.TEAM_MAP:
        team = var.TEAM_MAP[team]

    cnx.database = var.DB_NAME
    cursor.execute(var.TEAM_TABLE['select_team'].format(var.SEASON_TABLE_NAME + str(year), team))
    results = cursor.fetchall()
    return results[0]


def close_cnx(cnx, cursor):
    cursor.close()
    cnx.close()

