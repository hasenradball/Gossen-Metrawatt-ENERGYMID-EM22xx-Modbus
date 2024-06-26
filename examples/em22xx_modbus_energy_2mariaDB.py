"""Script to read energy data from EM22xx energy meter and send to mariadb"""
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
    energy_import = em2289_obj.get_energy_import_total()
    energy_export = em2289_obj.get_energy_export_total()
    energy = (energy_import, energy_export)
    #print(energy)
    maria_obj = maria_db(MARIA_DB_CONFIG)
    maria_obj.insert_by_sql_insert_stmt("energie", ("`E_import_tot`", "`E_export_tot`"), energy)
    #insert_Data2DB_MySql(energy)
    print("INFO: Insert into mariaDB finished!")
