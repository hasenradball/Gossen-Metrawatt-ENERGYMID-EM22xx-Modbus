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

The result may look like:

```
>>> Webserver is enabled!
Webserver status: 1


Voltages Primary: (416.2, 417.0, 417.5, 416.9, 240.4, 240.7, 240.9, 240.7) V
Currents Primary: (0.0, 0.0, 0.0, 0.0, 0.0) A
Power Primary   : (0, 0, 0, 0) W


Energy import total : 11600.56 kWh
Energy export total : 1.01 kWh
Device Features
[2, 0, 0, 1, 0, 0, 6, 0, 4, 0, 0]
        Type: U2289
        D   : Gossen Metrawatt
        H   : not available
        M   : with U, I, P, Q, S, PF, f, THD, In
        P   : with MID
        Q   : 1
        U   : 400 V
        V   : no impulse output
        W   : TCP/IP
        Z   : without Zählerstandsgang
        S   : 0

Firmware Version
        version :v1.21

INFO: test finished in 0.026 s
```

# License
This library is licensed under MIT Licence.

# Helpful Links
* [ESP8266-01-Adapter](https://esp8266-01-adapter.de)