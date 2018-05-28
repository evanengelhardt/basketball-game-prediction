TEAM_MAP = {
    "Atlanta": "Atlanta",
    "Boston": "Boston",
    "Brooklyn": "Brooklyn",
    "Charlotte": "Charlotte",
    "Chicago": "Chicago",
    "Cleveland": "Cleveland",
    "Dallas": "Dallas",
    "Denver": "Denver",
    "Detroit": "Detroit",
    "Golden State": "Golden State",
    "Houston": "Houston",
    "Indiana": "Indiana",
    "LA Clippers": "L.A. Clippers",
    "LA Lakers": "L.A. Lakers",
    "L.A. Clippers": "L.A. Clippers",
    "L.A. Lakers": "L.A. Lakers",
    "Memphis": "Memphis",
    "Miami": "Miami",
    "Milwaukee": "Milwaukee",
    "Minnesota": "Minnesota",
    "New Jersey": "New Jersey",
    "Seattle": "Seattle",
    "New Orleans": "New Orleans",
    "New York": "New York",
    "Oklahoma City": "Oklahoma City",
    "Orlando": "Orlando",
    "Philadelphia": "Philadelphia",
    "Phoenix": "Phoenix",
    "Portland": "Portland",
    "Sacramento": "Sacramento",
    "San Antonio": "San Antonio",
    "Toronto": "Toronto",
    "Utah": "Utah",
    "Washington": "Washington"
}


START_DATE = {
    'month': 12,
    'day': 30,
    'year': 2010
}

END_DATE = {
    'month': 4,
    'day': 12,
    'year': 2017
}

ALGORITHM_INFO = {
    'train_size': 4000,
    'test_size': 2000,
    'epochs': 500,
    'learn_step': 0.2,
    'init_wgt': 0
}

DB_NAME = "nba_db"
TABLE_NAME_COMP = "nba_table_comp"
TABLE_NAME_SIMP = "nba_table_simple"
SEASON_TABLE_NAME = "nba_season_"
isComplex = False

LARGE_TABLE = {
    # Detailed Table Ops
    'create_main_table': (
        "CREATE TABLE `" + TABLE_NAME_COMP + "` ("
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
    ),

    'insert_game': ("INSERT INTO " + TABLE_NAME_COMP + " (favorite, visitor_win_pct, home_win_pct, visitor_ppg, home_ppg,"
                                                    " visitor_oppg, home_oppg, visitor_fgp, home_fgp, visitor_ofgp,"
                                                    " home_ofgp, visitor_3fgp, home_3fgp, visitor_o3fgp, home_o3fgp, "
                                                    " visitor_tov, home_tov, visitor_rpg, home_rpg, visitor_apg,"
                                                    " home_apg, visitor_spg, home_spg, visitor_bpg, home_bpg,"
                                                    " winner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                                                    " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),

    'select_game': ("SELECT favorite, visitor_win_pct, home_win_pct, visitor_ppg, home_ppg,"
                                                " visitor_oppg, home_oppg, visitor_fgp, home_fgp, visitor_ofgp, "
                                                " home_ofgp, visitor_3fgp, home_3fgp, visitor_o3fgp, home_o3fgp, "
                                                " visitor_tov, home_tov, visitor_rpg, home_rpg, visitor_apg, "
                                                " home_apg, visitor_spg, home_spg, visitor_bpg, home_bpg, "
                                                " winner FROM " + TABLE_NAME_COMP)

}

SIMPLE_TABLE = {
    'create_main_table': (
        "CREATE TABLE `" + TABLE_NAME_SIMP + "` ("
        "   `game_no` int(11) NOT NULL AUTO_INCREMENT,"
        "   `favorite` int NOT NULL,"
        "   `visitor` varchar(25) NOT NULL,"
        "   `home` varchar(25) NOT NULL,"
        "   `visitor_win_pct` float NOT NULL,"
        "   `home_win_pct` float NOT NULL,"
        "   `visitor_ppg` float NOT NULL,"
        "   `home_ppg` float NOT NULL,"
        "   `visitor_oppg` float NOT NULL,"
        "   `home_oppg` float NOT NULL,"
        "   `winner` int NOT NULL,"
        "   PRIMARY KEY (`game_no`)"
        ") ENGINE=InnoDB"
    ),

    'insert_game': ("INSERT INTO " + TABLE_NAME_SIMP + " (favorite, visitor, home, visitor_win_pct, home_win_pct,"
                                                   " visitor_ppg, home_ppg, visitor_oppg, home_oppg, "
                                                    " winner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),

    'select_game': ("SELECT favorite, visitor, home, visitor_win_pct, home_win_pct, visitor_ppg, home_ppg,"
                                                " visitor_oppg, home_oppg, winner FROM " + TABLE_NAME_SIMP)
}

TEAM_TABLE = {
    'create_team_table': (
        "CREATE TABLE `{}` ("
        "   `team_name` varchar(25) NOT NULL,"
        "   `fgp` float NOT NULL,"
        "   `ofgp` float NOT NULL,"
        "   `3fgp` float NOT NULL,"
        "   `o3fgp` float NOT NULL,"
        "   `tov` float NOT NULL,"
        "   `rpg` float NOT NULL,"
        "   `apg` float NOT NULL,"
        "   `spg` float NOT NULL,"
        "   `bpg` float NOT NULL,"
        "   PRIMARY KEY (`team_name`)"
        ") ENGINE=InnoDB"
    ),

    'insert_team': ("INSERT INTO {} (team_name, fgp, ofgp, 3fgp, o3fgp, tov, rpg, apg, spg, bpg)"
                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),

    'select_team': ("SELECT team_name, fgp, ofgp, 3fgp, o3fgp, tov, rpg, apg, spg, bpg FROM {} WHERE team_name = '{}'")
}