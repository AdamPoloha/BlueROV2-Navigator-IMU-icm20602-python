[BlueRobotics](https://bluerobotics.com/) has provided this library in a working order.

The new [test.py](https://github.com/AdamPoloha/BlueROV2-Navigator-IMU-icm20602-python/blob/master/icm20602/test.py) is only modified to print the sensor data instead of logging it with another library. Therefore, the script can be tested and then modified for anyone's use without installing unnecessary packages.

This fork aims to provide some documentation on the library.

**ICMData Interface Structure:**
+ \_\_init\_\_(rawdata) - raw values are extracted from rawdata, and then real values are calculated using information provided in the [datasheet](https://invensense.tdk.com/wp-content/uploads/2020/11/DS-000176-ICM-20602-v1.1.pdf)

Acceleration is in gs, so multiply by 9.81 to get ms^-2.
Angular Velocity is in dps (degrees per second).
Temperature is given in degrees Celsius.

**ICM20602 Interface Structure:**
+ \_\_init\_\_(bus=1, cs=2, bus_sp=10000000, afssel=0, gfssel=0, adlpf=0, gdlpf=1, afchb=0, gfchb=0) - set configuration parameters, open port, and run initialize()
+ closeport() - close SPI bus
+ initialize() - write configs and add small delay
+ reset() - restart ICM and return boolean to show success status
+ read_id() - read the REG_WHO_AM_I register
+ read(reg, nbytes=1) - read a number of bytes from the select register and successive registers
+ readbyte(reg) - run read at select register with 0 nbytes
+ read_all() - run read, and get 14 bytes starting from the first acceleromter register
+ self_test(passperc=14) - run builtin self-test, check to a pass percentage, default 14%
+ write(reg, data, ignorefail=0, nosleep=0) - write data to register, check by reading, and return xfer success, sleep if write-read mismatch

Currently, if you wish to change the configuration parameters of the ICM, you can either edit the library \_\_init\_\_ function and run [setup.py](https://github.com/AdamPoloha/BlueROV2-Navigator-IMU-icm20602-python/blob/master/setup.py) again, or you can use the write function in your code to send the parameters manually.

ICM20602 \_\_init\_\_() now allows the configuration of the bus, chip select, bus rate, AFS_SEL (0-3), FS_SEL (0-3), A_DLPF_CFG (0-7), DLPF_CFG (0-7), ACCEL_FCHOICE_B (0-1), FCHOICE_B (0-3).

write() now checks by reading the written register to confirm if the value has changed. Since some, like the reset register will not show a reset flag when reset; the function allows fails to be ignored, otherwise fails will make the program continue after a two-second sleep. The sleep can also be skipped in cases where one wants to do an immediate operation after writing even when failing.

==============

**Self-Test:**

self_test() was written using the equation included in the datasheet (Sections 9.8 and 9.33). As these do not clearly state what the variables are; a similar equation was observed from the MPU6050 datasheet. The MPU6050 equation revealed what some of the variables should most likely be, and since the ICM datasheet does not have the pass percentages; the MPU's 14% was used.

**Perform Self-Test at own risk**

The understanding goes as follows:
+ The masses inside the chip are electromagnetically bent to a location with an expected output reading.
+ Rangeless factory responses are recorded onto the chip so that the test can be performed again to see degradation.
+ To perform a test, one must subtract the normal output from the self-test-on output to get a new response.
+ Then one must use the given equation to get a factory response for the selected Full Scale range.
+ The new response and the factory response are compared to get the percentage difference.
+ The test difference is compared to the "provided" acceptable range.

Test results:
+ Once the given equation appeared to be working the gyroscope would have similar test responses as the factory, and so in the worst case there would be maybe 2% difference.
+ The accelerometer test also worked as expected, with only the axis that bore gravity failing, and the others passing not much worse that the gyroscope.
+ However, after python3 tests looked well, python2 was tested and had issues, the self-test would never be enabled and so the new response would be almost zero as readings were similar.
+ Then during diagnosis, python3 started having the same problem and so further testing had to be abandoned.

Therefore, it "should" be working, but there are no guarantees that the function does not have a bug or that it does not cause issues to the chip.
