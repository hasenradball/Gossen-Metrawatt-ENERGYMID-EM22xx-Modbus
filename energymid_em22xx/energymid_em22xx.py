"""Class definition for the EM2289"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymodbus.client import ModbusTcpClient as ModBusClient
from pymodbus import (FramerType, ExceptionResponse, ModbusException)
from .constants import ModbusConstants as CONSTS
from .constants import EM22xxFeatures as FEATURE

class EM22xxModbus:
    """Base class for the EM2289 energy meter
    """
    def __init__(self, ip, port = 502, device_unit_id = 0):
        """Constructor of EM22xx_Modbus object
        -----
         Args:
            ip: ip address of device
            port: port which is used (default 502)
            device_unit_id: UnitID (default 0) 
        """
        self._client = ModBusClient(ip, port=port, framer=FramerType.SOCKET)
        self._device_unit_id = device_unit_id
        #print("Device Unit: ", self._device_unit_id)
        self.connect()

    def __del__(self):
        self.close()
        del self._device_unit_id
        del self._client


    def connect(self):
        """Establish conncetion of client
        -----
        """
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
        """Close connection of client
        -----
        """
        if self._client.is_socket_open():
            self._client.close()
            #print("INFO: Connection closed!")
        return None

    def read_input_register(self, register_address, datatype, count = 1) -> list:
        """Read the input register from EM2289 device
        
        Read register with function code 0x04
        -----
        Args:
            register_address:
            datatype: U16, U32 , etc...
            count: number of datatypes to be converted
        
        Returns:
            data: list of decoded values
        """
        length = CONSTS.TYPE_TO_LENGTH[datatype] * count
        #print(f'length : {length}')
        try:
            result = self._client.read_input_registers(register_address, count=length, \
                                                     slave=self._device_unit_id)
            #print(result, type(result))
        except ModbusException as exc:
            print(f">>> read_input_register: Received ModbusException({exc}) from library")
        if result.isError():
            print(f">>> read_input_register: Received Modbus library error({result})")
        if isinstance(result, ExceptionResponse):
            print(f">>> read_input_register: Received Modbus library exception ({result})")
            # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
            return False
        #print(type(result.registers), ": ", result.registers)
        data = self.decode_register_readings(result, datatype, count)
        return data

    def read_holding_register(self, register_address, datatype, count = 1) -> list:
        """Read the inoput register from EM2289 device
        
        Read register with function code 0x03
        -----
        Args:
            register_address:
            datatype: U16, U32 , etc...
            count: number of datatypes to be converted
        
        Returns:
            data: list of decoded values
        """
        length = CONSTS.TYPE_TO_LENGTH[datatype] * count
        #print(f'length : {length}')
        try:
            result = self._client.read_holding_registers(register_address, \
                count=length, slave=self._device_unit_id)
            #print(result, type(result))
        except ModbusException as exc:
            print(f">>> read_holding_register: Received ModbusException({exc}) from library")
        if result.isError():
            print(f">>> read_holding_register: Received Modbus library error({result})")
        if isinstance(result, ExceptionResponse):
            print(f">>> read_holding_register: Received Modbus library exception ({result})")
            # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
            return False
        #print(type(result.registers), ": ", result.registers)
        data = self.decode_register_readings(result, datatype, count)
        return data

    def convert_uint16_to_uint8_array(self, uint16_array, count):
        """
        Convert an 16-bit array into an 8-bit array,
        and return only specific number of elements by count
        """
        uint8_array = []
        for value in (uint16_array):
            high_byte = (value >> 8) & 0xFF
            low_byte = value & 0xFF
            uint8_array.extend([high_byte, low_byte])
        return uint8_array[0:count]

    def decode_register_readings(self, readings, datatype, count) -> list:
        """Decode the register readings 
        
        Decode readings depending on datatype given
        -----
        Args:
            readings: dats read from register
            datatype: U16, U32 , etc...
            count: number of datatypes to be converted
        
        Returns:
            data: list of decoded values
        """
        #print(f'decoder : {decoder}')
        data = []
        if datatype == 'U8':
            data = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.UINT16)
            data = self.convert_uint16_to_uint8_array(data, count)
        elif datatype == 'U16':
            data = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.UINT16)
        elif datatype == 'U32':
            data = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.UINT32)
        elif datatype == 'U64':
            data = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.UINT64)
        elif datatype == 'S16':
            data = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.INT16)
        elif datatype == 'S32':
            data = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.INT32)
        elif datatype == 'S64':
            data = self._client.convert_from_registers(readings.registers, data_type=self._client.DATATYPE.INT64)
        return data


class EnergyMIDEM22xx(EM22xxModbus):
    """Class for communicating with the EM2289 energy meter
    -----

    Remarks:
       1.) make sure the python lib 'pymodbus' is installed

       2.) Please check if the TCP port in the sma device is activated!

       3.) check Register description --> see specific documentation of manufacturer

       site: https://www.gossenmetrawatt.de/produkte/messen-steuern-regeln/energiemanagement/mid-zertifizierte-energiezaehler/energymid-em2281em2389
    """

    def get_voltages_primary(self) -> tuple:
        """Get voltages

        Read the primary voltages
        -----
           
        The voltages has the format:
            mantissa * 10 ^ exponent

        Read the Dreieck voltages as described:
            U12, U23, U31, mean U(L12, L23, L31)

            U1N, U2N, U3N, mean U(L1, L2, L3)

        Returns:
            (u_12, u_23, u_31, u_mean_12_23_31, u_1n, u_2n, u_3n, u_mean_123)
        -----
        Register address: 12, 0-7; S16
        Function code: 0x04; read input registers
        Unit: V
        """
        # first query the exponent
        exponent = self.read_input_register(12, 'S16')
        factor = 10**exponent
        #print("Faktor: ", factor)

        # read the voltages (mantissa)
        voltages = self.read_input_register(0, 'S16', 8)
        # tuple has format: (u_12, u_23, u_31, u_mean_12_23_31, u_1n, u_2n, u_3n, u_mean_123)
        u = tuple(round(i*factor, 1) for i in voltages)
        #print(f"tuple of u: {u} V")
        #print(f"U12:\t{u[0]} V")
        #print(f"U23:\t{u[1]} V")
        #print(f"U31:\t{u[2]} V")
        #print(f"U mean Dreieck:\t{u[3]} V", end="\n\n")

        #print(f"U1N:\t{u[4]} V")
        #print(f"U2N: \t{u[5]} V")
        #print(f"U3N:\t{u[6]} V")
        #print(f"U mean Stern:\t{u[7]:5.1f}")
        return u

    def get_currents_primary(self) -> tuple:
        """Get currents

        Read the primary currents
        -----

        The currents has the format:
        mantissa * 10 ^ exponent

        Read the currents in L1, L2, L3, N path:
            i1, i2, i3, i mean123, i_n
        
        Returns:
            (i_1, i_2, i_3, i_mean_123, i_n)
        -----
        Register address: 108, 100-104; S16
        Function code: 0x04; read input registers
        Unit: A
        """
        # first query the exponent
        exponent = self.read_input_register(108, 'S16')
        factor = 10**exponent
        #print("Faktor: ", factor)

        # read the currents (mantissa)
        currents = self.read_input_register(100, 'S16', 5)
        # tuple has format: (i_1, i_2, i_3, i_mean_123, i_n)
        i = tuple(round(i*factor, 2) for i in currents)
        #print(f"tuple of i: {i} A")
        #print(f"I 1:\t\t{i_1} A")
        #print(f"I 2:\t\t{i_2} A")
        #print(f"I 3:\t\t{i_3} A")
        #print(f"I mean 123:\t{i_mean_123} A")
        #print(f"I N:\t\t{i_n} A")
        return i

    def get_power_primary(self) -> tuple:
        """Get primary power
        
        Read the primary power
        -----
        The power has the format:
           mantissa * 10 ^ exponent

        Read the primary power 
            p1, p2, p3, p_tot
        Returns:
            (p_1, p_2, p_3, p_tot)
        -----
        Register address: 212, 200-203; S16
        Function code: 0x04; read input registers
        Unit: W
        """
        # first query the exponent
        exponent = self.read_input_register(212, 'S16')
        factor = 10**exponent
        #print("Faktor: ", factor)

        # read the power (mantissa)
        powers = self.read_input_register(200, 'S16', 4)
        # tuple has format: (p_1, p_2, p_3, p_tot)
        p = tuple(round(i*factor, 2) for i in powers)
        #print(f"tuple of p: {p} W")
        #print(f"P 1:\t{p[0]} W")
        #print(f"P 2:\t{p[1]} W")
        #print(f"P 3:\t{p[2]} W")
        #print(f"P tot:\t{p[3]} W")
        return p

    def get_energy_import_total(self) -> float:
        """Get energy import
        
        Read the primary energy import total (all tarifs)
        -----
        The energy has the format:
           mantissa * primary_energy_factor
           or 
           mantissa * 10 ^ exponent
        
        Returns:
            energy_import
        -----
        Register address: 408, 300; U32
        Function code: 0x04; read input registers
        Unit: kWh
        """
        # first query Primary Energy factor
        energy_factor_primary = self.read_input_register(408, 'U32')
        #print("Energie Faktor Primär: ", energy_factor_primary
        # read the mantissa of import total
        mantissa_import_total = self.read_input_register(300, 'U32')
        energy_import = mantissa_import_total * energy_factor_primary / 1000
        #print("Energy import:\t", energy_import)
        return energy_import

    def get_energy_export_total(self) -> float:
        """Get energy export

        Read the energy export total (all tarifs)
        -----
        The energy has the format:
           mantissa * primary_energy_factor
           or 
           mantissa * 10 ^ exponent
        
        Returns:
            energy_export
        -----
        Register address: 408, 302; U32
        Function code: 0x04; read input registers
        Unit: kWh
        """
        # first query Primary Energy factor
        energy_factor_primary = self.read_input_register(408, 'U32')
        #print("Energie Faktor Primär: ", energy_factor_primary
        # read the mantissa of export total
        mantissa_export_total = self.read_input_register(302, 'U32')
        energy_export = mantissa_export_total * energy_factor_primary / 1000
        #print("Energy export:\t", energy_export)
        return energy_export

    def read_device_features(self):
        """Read the device fetures of the EM22xx device
        -----
        Register address: 3000; U8
        Function code: 0x04; read input registers
        """
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
        """Read the firmware version
        -----
        Register address: 3012; U16
        Function code: 0x04; read input registers
        """
        print("Firmware Version")
        version = self.read_input_register(3012, 'U16')
        #print(version)
        version_arr = [*str(version)]
        version_str = f'v{version_arr[0]:}.{version_arr[1]:}{version_arr[2]:}'
        print(f'\tversion :{version_str}')
        return None

    def read_device_information(self):
        """Read Device Information

        Read device options and informations
        -----
        Register address: 3000;
        Function code: 0x04; read input registers
        """
        print("Device Information")
        readings = self.read_input_register(3000, 'U8', 23)
        print(readings)
        features = readings[0:11]
        print(features)
        serial_number = readings[11:19]
        print(serial_number)
        calibration_day = readings[19]
        print(calibration_day)
        calibration_month = readings[20]
        print(calibration_month)
        calibration_year = (readings[22] << 8) | readings[21]
        print(calibration_year)
        return None

    def read_webserver_status(self) -> int:
        """Read the webserver status

        Read if the webserver is enabled or not
        -----
        Register address: 11000; U16
        Function code: 0x03; read holding registers
        """
        status = self.read_holding_register(11000, 'U16')
        if status:
            print(">>> Webserver is enabled!")
        else:
            print(">>> Webserver is disabled!")
        return status

    def set_disable_webserver(self) -> bool:
        """Disable the webserver
        -----
        write 0 to disable
        
        -----
        Register address: 11000; U16
        Function code: 0x10; write_registers
        """
        register_value = self._client.convert_to_registers(0, data_type=self._client.DATATYPE.UINT16)
        response = self._client.write_registers(11000, values=register_value, slave=self._device_unit_id)
        if response.isError():
            print("Error during disabling webserver!")
            return False
        else:
            print("Successfully disabled webserver!")
            return True

    def set_enable_webserver(self) -> bool:
        """Enable the Webserver
        -----
        write 1 to enable
        
        -----
        Register address: 11000; U16
        Function code: 0x10; write_registers
        """
        register_value = self._client.convert_to_registers(1, data_type=self._client.DATATYPE.UINT16)
        response = self._client.write_registers(11000, values=register_value, slave=self._device_unit_id)
        if response.isError():
            print("Error during enabling webserver!")
            return False
        else:
            print("Successfully enalbed webserver!")
            return True
