#!/usr/bin/python3

from icm20602 import ICM20602
   
#import time

device = "icm20602"
 
icm = ICM20602()

def data_getter():
    data = icm.read_all()
    print(data.a.x, data.a.y, data.a.z, data.g.x, data.g.y, data.g.z, data.t,
        data.a_raw.x, data.a_raw.y, data.a_raw.z,
        data.g_raw.x, data.g_raw.y, data.g_raw.z, data.t_raw)
   
try:
    while True: 
        #time.sleep(1)
        data_getter() # prints the returned values of data_getter()
            
except KeyboardInterrupt:
    icm.closeport()
    print('Finish!!')
