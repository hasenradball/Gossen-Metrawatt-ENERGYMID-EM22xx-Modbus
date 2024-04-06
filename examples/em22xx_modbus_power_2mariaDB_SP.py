"""Script to read data from EM22xx energy meter and send to mariadb via stored procedure"""
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

    maria_obj = maria_db(MARIA_DB_CONFIG)
    maria_obj.insert_by_stored_procedure("insert_into_leistung", voltages + currents + power)
    #print("INFO: Insert into mariaDB finished!")
