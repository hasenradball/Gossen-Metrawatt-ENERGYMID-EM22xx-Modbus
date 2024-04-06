#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode
from cEnergyMID_EM22xx import EnergyMID_EM22xx
from mariadb_config import CONFIG
from cMariaDB_mysql import cMariaDB_mysql as maria_db

def insert_Data2DB_MySql(voltages, currents, power):
    '''Function to to update mariadb
    '''
    try:
        # connect to db
        cnx = mysql.connector.connect(**CONFIG)
        #print("cnx: ", cnx)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ERROR: User/Password!")
            return False
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("ERROR: No Database!")
            return False
        elif err.errno == errorcode.CR_CONN_HOST_ERROR:
            print("ERROR: Connection!")
            return False
        else:
            print(f"ERROR: {err.errno}")
            return False
    else:
        try:
            # cursor object
            cursor = cnx.cursor()
            # form query string
            tablecolumns_U = "`U12`, `U23`, `U31`, `mean_U12_23_31`, `U1N`, `U2N`, `U3N`, `mean_U123`"
            tablecolumns_I = "`I1`, `I2`, `I3`, `IN`"
            tablecolumns_P = "`P1`, `P2`, `P3`, `Ptot`"
            tablecolumns = tablecolumns_U + ", " + tablecolumns_I + ", " + tablecolumns_P
            tablevalues = voltages + currents + power
            #print(tablecolumns)
            #print(tablevalues)
            query = ("INSERT INTO `waermepumpe`.`leistung` (" + tablecolumns + ") VALUES" + str(tablevalues))
            #print(query)
            # execute query
            cursor.execute(query)
            cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_PARSE_ERROR:
                print(f"ERROR: Syntax! ({err.errno})")
                return False
            else:
                print(f"ERROR: {err.errno}")
                return False
        cursor.close()
        cnx.close()
    finally:
        #print("finally")
        pass
    return True

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
    
    maria_obj = maria_db(CONFIG)
    maria_obj.insert_by_sql_insert_stmt("leistung", tablecolumns, voltages + currents + power)
    #print("INFO: Insert into mariaDB finished!")
    
