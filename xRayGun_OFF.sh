#Check status
./xray_client_tcp 192.168.1.4 22, 
#22,0,1,0,
#Which means:
#0 - HV OFF
#1/0 - Interlock Open/Close
#0 - No Fault

# Program kV Setpoint: should be 50 K
./xray_client_tcp 192.168.1.4 10,4095, #Where: = 0 - 4095 in ASCII format

# Program mA Setpoint: should be 1 mA (4095 = 2 mA)
./xray_client_tcp 192.168.1.4 11,2047,

# Program Filament Preheat: should be 0.2 A (4095 = 10 A)
./xray_client_tcp 192.168.1.4 12,82,

# Program Filament Current Limit: should be 1.7 A (4095 = 10 A)
./xray_client_tcp 192.168.1.4 13,696,

# Program Filament Ramp Time: 4000 ms
./xray_client_tcp 192.168.1.4 47,1,4000,

# Turn high voltage ON
./xray_client_tcp 192.168.1.4 99,1,
# Turn high voltage OFF
#./xray_client_tcp 192.168.1.4 99,0,

# Request Analog Monitor Readbacks
#./xray_client_tcp 192.168.1.4 20,
#<ARG1> = Control Board Temperature Sensor Reading, range 0-4095
#<ARG2> = Low Voltage Supply Monitor, range 0-4095
#<ARG3> = kV Feedback Reading, range 0-4095
#<ARG4> = mA Feedback Reading, range 0-4095
#<ARG5> = Filament Current Reading, range 0-4095
#<ARG6> = Filament Voltage Reading, range 0-4095
#<ARG7> = High Voltage Board Temperature Sensor, range 0-4095
