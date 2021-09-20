## Important Spellman commands summary:
### Program kV Setpoint
Syntax: <STX><10><,><ARG><,><CSUM><ETX>
Where: <ARG> = 0 - 4095 in ASCII format
Example: <STX>10,4095,<CSUM><ETX>
Response:
- Success: <STX><10><,><$><,><CSUM><ETX>
- Error : <STX><10><,><ARG><,><CSUM><ETX>
where <ARG> = error code
Error Codes, 1=out of range
### Program mA Setpoint
Syntax: <STX><11><,><ARG><,><CSUM><ETX>
Where: <ARG> = 0 - 4095 in ASCII format
Example: <STX>11,4095,<CSUM><ETX>
Response:
- Success: <STX><11><,><$><,><CSUM><ETX>
- Error: <STX><11><,><ARG><,><CSUM><ETX>
where <ARG> = error code
Error Codes TBD, 1=out of rang

### Program Filament Preheat
Syntax: <STX><12><,><ARG><,><CSUM><ETX>
Where: <ARG> = 0 - 4095 in ASCII format
Example: <STX>12,4095,<CSUM><ETX>
Response:
- Success: <STX><12><,><$><,><CSUM><ETX>
- Error: <STX><12><,><ARG><,><CSUM><ETX>
where <ARG> = error code
Error Codes TBD, 1 = out of range

### Program Filament Current Limit
Syntax: <STX><13><,><ARG><,><CSUM><ETX>
Where: <ARG> = 0 - 4095 in ASCII format
Example: <STX>13,4095,<CSUM><ETX>
Response:
- Success: <STX><13><,><$><,><CSUM><ETX>
- Error: <STX><13><,><ARG><,><CSUM><ETX>
where <ARG> = error code
Error Codes TBD, 1 = out of range

### Request Analog Monitor Readbacks
Syntax: <STX><20><,><CSUM><ETX>
Example: <STX>20,<CSUM><ETX>
Response: <STX><20><,><ARG1><,><ARG2><,><ARG3><,><ARG4><,>
<ARG5><,><ARG6><,><ARG7>,<CSUM><ETX>
Where:
\<ARG1\> = Control Board Temperature Sensor Reading, range 0-4095
\<ARG2\> = Low Voltage Supply Monitor, range 0-4095
\<ARG3\> = kV Feedback Reading, range 0-4095
\<ARG4\> = mA Feedback Reading, range 0-4095
\<ARG5\> = Filament Current Reading, range 0-4095
\<ARG6\> = Filament Voltage Reading, range 0-4095
\<ARG7\> = High Voltage Board Temperature Sensor, range 0-4095
Example:
<STX>19,500,2048,4095,4095,4095,4095,4095,4095,650,
<CSUM><ETX>

### Request Expanded Status
Syntax: <STX><32><,><CSUM><ETX>
Example: <STX>32,<CSUM><ETX>
Response: <STX><32><,><ARG1><,><ARG2><,><ARG3><,><ARG4><,><ARG5><,><ARG6><,><ARG7><,><CSUM><ETX>
Where:
\<ARG1\> 1 = Hv On, 0 = Hv Off
\<ARG2\> 1 = Interlock 1 Open, 0 = Interlock 1 Closed
\<ARG3\> 1 = Interlock Fault, 0 = No Interlock Fault
\<ARG4\> 1 = Over-voltage Fault, 0 = No Over-voltage Fault
\<ARG5\> 1 = Configuration Fault, 0 = No Configuration Fault
\<ARG6\> 1 = Overpower Fault, 0 = No Overpower Fault
\<ARG7\> 1 = 24V Undervoltage Fault, 0 = No Undervoltage Fault
Example Response for HV on, interlock closed, no faults:
<STX>32,1,0,0,0,0,<CSUM><ETX>

### Program Filament Ramp Time
This command is used to enable the filament / mA ramping function and to
set the ramp time. When the ramping function is enabled the filament
current and mA set point value are ramped up from zero to their set values
starting when the high voltage is turned on. When the ramping function is
disabled the filament preheat current and mA setpoint go immediately to
their set values. There are 2 arguments sent with the command. The first
argument determines if the ramping function is enabled or disabled. The
second is the ramp time in milliseconds. The maximum allowed ramp time
is 10000 ms (10 seconds).
Syntax: <STX><47><,><ARG1><,><ARG2><,><CSUM><ETX>
Where: 
\<ARG1\> = 0 or 1 in ASCII format. “0” disables the ramping function, “1”
enables it.
\<ARG2\> = 0 – 10000 in ASCII format. This is the ramp time in
milliseconds. Note that if \<ARG1\> is set to 0, the ramp time \<ARG2\> must
also be set to 0. If \<ARG1\> is set to 1, then the ramp time \<ARG2\> must
be set to be greater than 0. The ramp can not be enabled with ramp time
set to 0.
Examples:
- Ramp Off: <STX>47,0,0,<CSUM><ETX>
- Ramp On, Ramp Time 2000ms: <STX>47,1,2000,<CSUM><ETX>

Response: <STX><47><,><$><,><CSUM><ETX>
Error Codes, 1 = One (or possibly both) of the arguments is out of range.

### Request Filament Ramp Time
Syntax: <STX><48><,><CSUM><ETX>
Example: <STX>48,<CSUM><ETX>
Response: <STX><48><,>< ARG1><,><ARG2><,><CSUM><ETX>
Where:
\<ARG1\> is ASCII 1 or 0, with 1 = Ramping Enabled, 0 = Ramping
Disabled.
\<ARG2\> is the Ramp Time in milliseconds, Range 0 - 10000
Example Responses:
- Ramp is Off <STX>48,0,0,<CSUM><ETX>
- Ramp On, Ramp Time = 500ms: <STX>48,1,500,<CSUM><ETX>