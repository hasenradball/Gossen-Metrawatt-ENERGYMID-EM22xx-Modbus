"""Class definition for the EM2289"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client import ModbusTcpClient as ModBusClient
from .Modbus_Constants import Modbus_Constants as CONSTS
from .Modbus_Constants import EM22xx_Features as FEATURE

class EM22xx_Modbus:
    '''Base class for the EM2289 energy meter
    '''
    def __init__(self, ip, port=502, device_unit_id=0):
        self._client = ModBusClient(ip, port)
        self._device_unit_id = device_unit_id
        #print("Device Unit: ", self._device_unit_id)
        self.connect()

    def __del__(self):
        self.close()
        del self._device_unit_id
        del self._client


    def connect(self):
        '''Establish conncetion of client
        '''
        try:
            if not self._client.connect():
                print("ERROR: client cannot connect to ModBus-Server!")
            else:
                #print("INFO: client connected successfully to Modbus-Server!")
                pass
        except:
            print("ERROR: Propably an Syntax Error!")

        finally:
            pass

    def close(self):
        '''Close connection of client
        '''
        if self._client.is_socket_open():
            self._client.close()
            #print("INFO: Connection closed!")
        return None

    def read_input_register(self, register_address, datatype, count = 1):
        '''Read the inoput register from EM2289 device
           Function code: 0x04
        '''
        length = CONSTS.TYPE_TO_LENGTH[datatype] * count
        #print(f'length : {length}')
        result = self._client.read_input_registers(register_address, length, \
                slave=self._device_unit_id)
        #print(type(result.registers), ": ", result.registers)
        data = self.decode_register_readings(result, datatype, count)
        return data

    def read_holding_register(self, register_address, datatype, count = 1):
        '''Read the inoput register from EM2289 device
           Function code: 0x03
        '''
        length = CONSTS.TYPE_TO_LENGTH[datatype] * count
        #print(f'length : {length}')
        result = self._client.read_holding_registers(register_address, \
                length, slave=self._device_unit_id)
        #print(type(result.registers), ": ", result.registers)
        data = self.decode_register_readings(result, datatype, count)
        return data

    def decode_register_readings(self, readings, datatype, count):
        '''Decode the register readings dependend on datatype
        '''
        decoder = BinaryPayloadDecoder.fromRegisters(readings.registers, \
            byteorder=Endian.BIG, wordorder=Endian.BIG)
        #print(f'decoder : {decoder}')
        if datatype == 'U8':
            data = [decoder.decode_8bit_uint() for i in range(count)]
        elif datatype == 'U16':
            data = [decoder.decode_16bit_uint() for i in range(count)]
        elif datatype == 'U32':
            data = [decoder.decode_32bit_uint() for i in range(count)]
        elif datatype == 'U64':
            data = [decoder.decode_64bit_uint() for i in range(count)]
        elif datatype == 'S8':
            data = [decoder.decode_8bit_int() for i in range(count)]
        elif datatype == 'S16':
            data = [decoder.decode_16bit_int() for i in range(count)]
        elif datatype == 'S32':
            data = [decoder.decode_32bit_int() for i in range(count)]
        elif datatype == 'S64':
            data = [decoder.decode_64bit_int() for i in range(count)]
        return data


class EnergyMID_EM22xx(EM22xx_Modbus):
    '''Class for communicating with the EM2289 energy meter
       1.) make sure the python lib 'pymodbus' is installed
       2.) Please check if the TCP port in the sma device is activated!
       3.) check Register description --> see specific documentation of manufacturer
       e.g.: https://www.gmc-instruments.de/produkte/industrielle-messtechnik/energiemanagement/energiezaehler/mid-zertifizierte-energiezaehler/em2281em2389/em2289-mid-kwh-4-l-5-80-a-tcp/
    '''


    def get_voltages_primary(self):
        '''Read the voltages
           Function code: 0x04; read input registers
           The voltages has the format:
           mantissa * 10 ^ exponent

           Read the Dreieck voltages as described
            U12
            U23
            U31
            mean U(L12, L23, L31)
            U1N
            U2N
            U3N
            mean U(L1, L2, L3)
           Unit: V
        '''
        # first query the exponent
        exponent = self.read_input_register(12, 'S16')[0]
        factor = 10**exponent
        #print("Faktor: ", factor)

        # read the voltages (mantissa)
        voltages = self.read_input_register(0, 'S16', 8)
        u_12 = round(voltages[0] * factor, 1)
        #print("U12:\t", U_12)
        u_23 = round(voltages[1] * factor, 1)
        #print("U23:\t", U_23)
        u_31 = round(voltages[2] * factor, 1)
        #print("U31:\t", U_31)
        u_mean_12_23_31 = round(voltages[3] * factor, 1)
        #print("U mean Dreieck:\t", U_mean_12_23_31, end="\n\n")

        u_1n = round(voltages[4] * factor, 1)
        #print("U1N:\t", U_1N)
        u_2n = round(voltages[5] * factor, 1)
        #print("U2N: \t", U_2N)
        u_3n = round(voltages[6] * factor, 1)
        #print("U3N:\t", U_3N)
        u_mean_123 = round(voltages[7] * factor, 1)
        #print("U mean Stern:\t%5.1f" %U_mean_123)
        return (u_12, u_23, u_31, u_mean_12_23_31, u_1n, u_2n, u_3n, u_mean_123)

    def get_currents_primary(self):
        '''Read the currents
           Function code: 0x04; read input registers
           The currents has the format:
           mantissa * 10 ^ exponent

           Read the currents in L1, L2, L3, N path
            i1
            i2
            i3
            i mean123
            i_n
           Unit: A
        '''
        # first query the exponent
        exponent = self.read_input_register(108, 'S16')[0]
        factor = 10**exponent
        #print("Faktor: ", factor)

        # read the currents (mantissa)
        currents = self.read_input_register(100, 'S16', 5)
        i_1 = round(currents[0] * factor, 2)
        #print("I 1:\t\t", I_1)
        i_2 = round(currents[1] * factor, 2)
        #print("I 2:\t\t", I_2)
        i_3 = round(currents[2] * factor, 2)
        #print("I 3:\t\t", I_3)
        i_mean_123 = round(currents[3] * factor, 2)
        #print("I mean 123:\t", I_mean_123)
        i_n = round(currents[4] * factor, 2)
        #print("I N:\t\t", I_N)
        return (i_1, i_2, i_3, i_mean_123, i_n)

    def get_power_primary(self):
        '''Read the primary power
           Function code: 0x04; read input registers
           The power has the format:
           mantissa * 10 ^ exponent

           Read the primary power 
            p1
            p2
            p3
            p_tot
           Unit: kW
        '''
        # first query the exponent
        exponent = self.read_input_register(212, 'S16')[0]
        factor = 10**exponent
        #print("Faktor: ", factor)

        # read the power (mantissa)
        powers = self.read_input_register(200, 'S16', 4)
        p_1 = round(powers[0] * factor, 2)
        #print("P 1:\t", P_1)
        p_2 = round(powers[1] * factor, 2)
        #print("P 2:\t", P_2)
        p_3 = round(powers[2] * factor, 2)
        #print("P 3:\t", P_3)
        p_tot = round(powers[3] * factor, 2)
        #print("P tot:\t", P_tot)
        return (p_1, p_2, p_3, p_tot)

    def get_energy_import_total(self):
        '''Read energy import 
           Function code: 0x04; read input registers
           The energy has the format:
           mantissa * primary_energy_factor
           or 
           mantissa * 10 ^ exponent
           -------------------------------------
           Read the primary energy of all tarifs
           Unit: kWh
        '''
        # first query Primary Energy factor
        energy_factor_primary = self.read_input_register(408, 'U32')[0]
        #print("Energie Faktor Primär: ", energy_factor_primary
        # read the mantissa of import total
        mantissa_import_total = self.read_input_register(300, 'U32')[0]
        energy_import = mantissa_import_total * energy_factor_primary / 1000
        #print("Energy import:\t", energy_import)
        return energy_import

    def get_energy_export_total(self):
        '''Read energy export
           Function code: 0x04; read input registers
           The energy has the format:
           mantissa * primary_energy_factor
           or 
           mantissa * 10 ^ exponent
           -------------------------------------
           Read the primary energy of all tarifs
           Unit: kWh
        '''
        # first query Primary Energy factor
        energy_factor_primary = self.read_input_register(408, 'U32')[0]
        #print("Energie Faktor Primär: ", energy_factor_primary
        # read the mantissa of export total
        mantissa_export_total = self.read_input_register(302, 'U32', 2)[0]
        energy_export = mantissa_export_total * energy_factor_primary / 1000
        #print("Energy export:\t", energy_export)
        return energy_export

    def read_device_features(self):
        '''Read the device fetures of the EM22xx device
        '''
        print("Device Features")
        features = self.read_input_register(3000, 'U8', 11)
        #print(features)
        print(f'\tType: {FEATURE.TYPE[features[0]]}')
        print(f'\tD   : {FEATURE.D[features[1]]}')
        print(f'\tH   : {FEATURE.H[features[2]]}')
        print(f'\tM   : {FEATURE.M[features[3]]}')
        print(f'\tP   : {FEATURE.P[features[4]]}')
        print(f'\tQ   : {FEATURE.Q[features[5]]}')
        print(f'\tU   : {FEATURE.U[features[6]]}')
        print(f'\tV   : {FEATURE.V[features[7]]}')
        print(f'\tW   : {FEATURE.W[features[8]]}')
        print(f'\tZ   : {FEATURE.Z[features[9]]}')
        print(f'\tS   : {FEATURE.S[features[10]]}\n')
        return None

    def read_firmware_version(self):
        '''Read the firmware version
        '''
        print("Firmware Version")
        #version = self.read_input_register(3012, 'U16')[0]
        #print(version)
        readings = self._client.read_input_registers(3012, 2, slave=self._device_unit_id)
        decoder = BinaryPayloadDecoder.fromRegisters(readings.registers, \
                byteorder=Endian.BIG, wordorder=Endian.BIG)
        version = [*str(decoder.decode_16bit_uint())]
        version_str = f'v{version[0]:}.{version[1]:}{version[2]:}'
        print(f'\tversion :{version_str}')
        return None

    def read_device_information(self):
        '''Read Device Information
           Function code: 0x04; read input registers
           Read device options and informations
        '''
        print("Device Information")
        readings = self._client.read_input_registers(3000, 36, slave=self._device_unit_id)
        #print("readings.registers: ", readings.registers)
        #decoder = BinaryPayloadDecoder.fromRegisters(readings.registers, \
        #        byteorder=Endian.BIG, wordorder=Endian.BIG)
        features = self.decode_register_readings(readings, 'U8', 11)
        print(features)
        serial_number = self.decode_register_readings(readings, 'U8', 8)
        print(serial_number)
        calibration_day = self.decode_register_readings(readings, 'U8', 1)
        print(calibration_day)
        calibration_month = self.decode_register_readings(readings, 'U8', 1)
        print(calibration_month)
        calibration_year = self.decode_register_readings(readings, 'U16', 1)
        print(calibration_year)
        #data = decoder.decode_8bit_uint()
        #int_to_type = {0: 'U2281', 2: 'U2289', 3: 'U2381', 4: 'U2387', 5: 'U2389'}
        #print(f'Type: {int_to_type[data]}')
        #data = decoder.decode_8bit_uint()
        return None

    def read_webserver_status(self):
        '''Read the webserver status
           Function code: 0x03; read holding registers
           Read if the webserver is enabled or not
        '''
        status = self.read_holding_register(11000, 'U16')[0]
        if status:
            print(">>> Webserver is enabled!")
        else:
            print(">>> Webserver is disabled!")
        return status

    def set_disable_webserver(self):
        '''Disable the webserver
           Function code: 0x16; mask_write_register
           Disable the webserver
        '''
        #result = self._client.write_register(11000, 0, slave=self._device_unit_id)
        #print("response:\t", result)
        return None

    def set_enable_webserver(self):
        '''Enable the Webserver
           Function code: 0x16; mask_write_register
           Enable the webserver
        '''
        #ressult = self._client.write_register(11000, 1, slave=self._device_unit_id)
        #print("response:\t", result)
        return None
