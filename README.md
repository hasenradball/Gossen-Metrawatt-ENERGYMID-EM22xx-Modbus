# Gossen-Metrawatt-ENERGYMID-EM22xx-Modbus
python solution for connecting the energy meter EM22xx via Modbus

![EM2289](./docs/EM2289.jpg)

## Contents
* [Prerecquisites](#prerecquisites)
* [Usage](#usage)
* [License](#license)
* [Helpful Links](#helpful-links)

## Prerecquisites
1) For the use of this python code it is necessary to install the python libs `pymodbus` and `pyserial`:

```
python3 -m pip install pymodbus
python3 -m pip install pyserial
```
>Remark: for pymodbus use minimum the version of 3.9.2, tested with pymodbus==3.9.2

## Usage
Check the python code in the script `em22xx_modbus.py`.<br>
Adapt your settings and change the ip address according to your settings.
```
em2289_obj = EnergyMID_EM22xx("192.168.178.253")`
```

Then you can check the communucation via:

`python3 em22xx_modbus.py`

# License
This library is licensed under MIT Licence.

# Helpful Links
* [ESP8266-01-Adapter](https://esp8266-01-adapter.de)