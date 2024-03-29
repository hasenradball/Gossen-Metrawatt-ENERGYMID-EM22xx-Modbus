# Gossen-Metrawatt-ENERGYMID-EM22xx-Modbus
python solution for connecting the energy meter EM22xx

## Contents
* [Prerecquisites](#prerecquisites)
* [Usage](#usage)
* [License](#license)
* [Helpful Links](#helpful-links)

## Prerecquisites
1) For the use of this python code it is necessary to install the python libs `pymodbus` and `pyserial`:

    `python3 -m pip install pymodbus`
    `python3 -m pip install pyserial`
    
    Remark: use the minimum the version of 3.6.x

## Usage
Check the python code in the script `em22xx_modbus.py` and change the settings if necessary.
Then you can check the communucation via:

`python3 em22xx_modbus.py`

# License
This library is licensed under MIT Licence.

# Helpful Links
* [ESP8266-01-Adapter](https://esp8266-01-adapter.de)