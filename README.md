## **Spellman HV power supply control**

This set of tools is providing control for the HV power supply. This power supply is used for the Mini-XRay tube.

Main commands list: [importantCommands.md](https://github.com/mohaas33/xRay/blob/main/importantCommands.md) 

### **Monitoring**

`./monitorXRay.py &`

### **Scripts to setup tube**

- Setup: `./setup_xRayGun.sh`
- Turn ON: `./xRayGun_ON.sh`
- Turn OFF: `./xRayGun_OFF.sh`

### Configuration from [setup_xRayGun.sh](https://github.com/mohaas33/xRay/blob/main/setup_xRayGun.sh):

Program kV Setpoint: 50 K

Program mA Setpoint: 1 mA (4095 = 2 mA)

Program Filament Preheat: 0.2 A (4095 = 10 A)

Program Filament Current Limit: 1.7 A (4095 = 10 A)

Program Filament Ramp Time: 4000 ms
