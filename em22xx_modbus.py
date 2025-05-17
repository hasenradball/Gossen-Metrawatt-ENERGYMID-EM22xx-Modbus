"""Script to test the ES2289 functionality"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from energymid_em22xx import EnergyMIDEM22xx

# Main
if __name__ == "__main__":
    start = time.perf_counter()
    em2289_obj = EnergyMIDEM22xx("192.168.178.253")
    # just for testing
    #em2289_obj.set_enable_webserver()
    print(f'Webserver status: {em2289_obj.read_webserver_status()}')
    print('\n')
    print(f'Voltages Primary: {em2289_obj.get_voltages_primary()} V')
    print(f'Currents Primary: {em2289_obj.get_currents_primary()} A')
    print(f'Power Primary   : {em2289_obj.get_power_primary()} W')
    print('\n')
    print(f'Energy import total : {em2289_obj.get_energy_import_total()} kWh')
    print(f'Energy export total : {em2289_obj.get_energy_export_total()} kWh')
    #em2289_obj.read_device_features()
    em2289_obj.read_firmware_version()
    stop = time.perf_counter()

    print(f'\nINFO: test finished in {stop-start:.3f} s')
