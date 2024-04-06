"""Constants for use with EM22xx Modbus"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ModbusConstants:
    """Constants for use with pymodbus
    """
    TYPE_TO_LENGTH = {'U8': 1, 'U16': 1, 'U32': 2, 'U64': 4, \
                      'S8': 1, 'S16': 1, 'S32': 2, 'S64': 4}

class EM22xx_Features:
    """Class for EM22xx related constants"""
    TYPE = {0: 'U2281', 2: 'U2289', 3: 'U2381', 4: 'U2387', 5: 'U2389'}
    D    = {0: 'Gossen Metrawatt'}
    # Hilfs-Spannung
    H    = {0: 'not available'}
    M    = {0: 'no multifunctional', \
            1: 'with U, I, P, Q, S, PF, f, THD, In', \
            2: 'with Blindenergi', \
            3: 'with U, I, P, Q, S, PF, f, THD, In & Blindenergie'}
    #  Calibration
    P    = {0: 'with MID', 9: 'with MID + Eichschein'}
    """Übersetzungsverhältnis
       VT: des Spannungswandlers (Up/Us)
       CT: des Stromwandlers (Ip/Is)
    """
    Q    = {0: '1', 1: 'adustable', 9: 'CT/VT fixed by order'}
    # Betriebsspannung
    U  = {3: '100V / 110 V not in combination with Z2 possible', \
          5: ' 2 Leiter 230 V', \
          6: '400 V', \
          7: '500 V'}
    # Impuls-Ausgang
    V  = {0: 'no impulse output', \
          1: '1000 impulse/kWh, 24 V, 30 ms impulse width, > 30 ms impulse break', \
          2: 'S0 programmierbar, 24 V, 30 ms impulse width, > 30 ms impulse break', \
          3: '1000 impulse/kWh, 230 V, 30 ms impulse width, > 30 ms impulse break', \
          4: 'S0 programmierbar, 230 V, 30 ms impulse width, > 30 ms impulse break', \
          7: '100 impulse/kWh, 24 V, 130 ms impulse width, > 130 ms impulse break', \
          8: '1000 impulse/kWh, 24 V, 130 ms impulse width, > 130 ms impulse break', \
          9: 'Kundenspezifisch bestellt, 24 V'}
    # Businterface
    W  = {0: 'No Interface', \
          1: 'LON', \
          2: 'MBus', \
          4: 'TCP/IP', \
          7: 'MODBus RTU'}
    # Zählerstandsgang
    Z  = {0: 'without Zählerstandsgang', \
          1: 'mit Zählerstandsgang', \
          2: 'mit zertifiziertem Zählerstandsgang'}
    # Sonderausführung
    S  = {0: '0'}
