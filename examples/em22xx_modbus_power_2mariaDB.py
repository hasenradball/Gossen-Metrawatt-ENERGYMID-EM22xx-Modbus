#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode
from cEnergyMID_EM22xx import EnergyMID_EM22xx
from mariadb_config import MARIA_DB_CONFIG
from cMariaDB_mysql import cMariaDB_mysql as maria_db


# Main
if __name__ == "__main__":
    em2289_obj = EnergyMID_EM22xx("192.168.178.253")
    voltages = em2289_obj.get_voltages_primary()
    #print(voltages)

    currents = em2289_obj.get_currents_primary()
    #print(currents)

    power = em2289_obj.get_power_primary()
    #print(power)

    tablecolumns_U = ("`U12`, `U23`, `U31`, `mean_U12_23_31`, `U1N`, `U2N`, `U3N`, `mean_U123`")
    tablecolumns_I = ("`I1`, `I2`, `I3`, `IN`")
    tablecolumns_P = ("`P1`, `P2`, `P3`, `Ptot`")
    tablecolumns = tablecolumns_U + tablecolumns_I + tablecolumns_P
    print(tablecolumns)
    
    maria_obj = maria_db(MARIA_DB_CONFIG)
    maria_obj.insert_by_sql_insert_stmt("leistung", tablecolumns, voltages + currents + power)
    #print("INFO: Insert into mariaDB finished!")
    
