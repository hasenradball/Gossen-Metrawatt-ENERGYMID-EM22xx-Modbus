#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode
from energymid_em22xx import EnergyMID_EM22xx
from mariadb_config import MARIA_DB_CONFIG
from maria_db_mysql import cMariaDB_mysql as maria_db


# Main
if __name__ == "__main__":
    em2289_obj = EnergyMIDEM22xx("192.168.178.253")
    voltages = em2289_obj.get_voltages_primary()
    #print(voltages)

    currents = em2289_obj.get_currents_primary()
    #print(currents)

    power = em2289_obj.get_power_primary()
    #print(power)

    tablecolumns_u = "`U12`, `U23`, `U31`, `mean_U12_23_31`, `U1N`, `U2N`, `U3N`, `mean_U123`"
    tablecolumns_i = "`I1`, `I2`, `I3`, `IN`"
    tablecolumns_p = "`P1`, `P2`, `P3`, `Ptot`"
    tablecolumns = tablecolumns_u + tablecolumns_i + tablecolumns_p
    print(tablecolumns)

    maria_obj = maria_db(MARIA_DB_CONFIG)
    maria_obj.insert_by_sql_insert_stmt("leistung", tablecolumns, voltages + currents + power)
    #print("INFO: Insert into mariaDB finished!")
