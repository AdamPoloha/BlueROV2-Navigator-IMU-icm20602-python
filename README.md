[BlueRobotics](https://bluerobotics.com/) has provided this library in a working order.

The new [test.py](https://github.com/AdamPoloha/BlueROV2-Navigator-IMU-icm20602-python/blob/master/icm20602/test.py) is only modified to print the sensor data instead of logging it with another library. Therefore, the script can be tested and then modified for anyone's use without installing unnecessary packages.

This fork aims to provide some documentation on the library.

**ICMData Interface Structure:**
+ \_\_init\_\_(rawdata) - raw values are extracted from rawdata, and then real values are calculated using information provided in the [datasheet](https://invensense.tdk.com/wp-content/uploads/2020/11/DS-000176-ICM-20602-v1.1.pdf)

Acceleration is in gs, so multiply by 9.81 to get ms^-2.
Angular Velocity is in dps (degrees per second).
Temperature is given in degrees Celsius.

**ICM20602 Interface Structure:**
+ \_\_init\_\_(self, bus=1, cs=2) - set configuration parameters, open port, and run initialize()
+ closeport() - close SPI bus
+ initialize() - write configs and add small delay
+ reset() - restart ICM and return boolean to show success status
+ read_id() - read the REG_WHO_AM_I register
+ read(reg, nbytes=1) - read a number of bytes from the select register and successive registers
+ readbyte(reg) - run read at select register with 0 nbytes
+ read_all() - run read, and get 14 bytes starting from the first acceleromter register
+ self_test() - **no implementation -todo run ICM self-test**
+ write(reg, data) - write data to register and return xfer success **-todo verify by read after write**

Currently, if you wish to change the configuration parameters of the ICM, you can either edit the library \_\_init\_\_ function and run [setup.py](https://github.com/AdamPoloha/BlueROV2-Navigator-IMU-icm20602-python/blob/master/setup.py) again, or you can use the write function in your code to send the parameters manually.

**Todo - edit \_\_init\_\_ to allow setting configuration parameters that are now hardcoded.**
