import json
import os

import psutil

type = 'Core'
dict_cpu_temp = {}
if hasattr(psutil, "sensors_temperatures"):
    temps = psutil.sensors_temperatures()
else:
    temps = {}

print(temps)
