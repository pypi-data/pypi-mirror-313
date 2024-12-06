This project is based on [plutocontrol](https://github.com/DronaAviation/plutocontrol) By [Saail Chavan](mailto:saailchavan02@gmail.com)

# plutocontrol

plutocontrol is a Python library for controlling Pluto drones. This library provides various methods to interact with the drone, including connecting, controlling movements, and accessing sensor data.

## Installation

```bash
pip install pypluto-christ
```

## Usage

After installing the package, you can import and use the `Pluto` class in your Python scripts.

### Example Usage

#### Example 1

```python
from pypluto import pluto

# Create an instance of the Pluto class
pluto = pluto()

# Connect to the drone
pluto.connect()

# Arm the drone
pluto.arm()

# Disarm the drone
pluto.disarm()

# Disconnect from the drone
pluto.disconnect()
```

## Class and Methods

### Pluto Class

#### `Connection`

Commands to connect/ disconnect to the drone server.

```python
#Connects from the drone server.
pluto.connect()

#Disconnects from the drone server.
pluto.disconnect()
```

#### `Comera module`

Sets the IP and port for the camera connection. should be intialized before pluto.connect().

```python
pluto.cam()
```

#### `Arm and Disarm Commands`

```python
#Arms the drone, setting it to a ready state.
pluto.arm()

#Disarms the drone, stopping all motors.
Pluto.disarm()
```

#### `Pitch Commands`

```python
#Sets the drone to move forward.
pluto.forward()

#Sets the drone to move backward.
pluto.backward()
```

#### `Roll Commands`

```python
#Sets the drone to move left (roll).
pluto.left()

#Sets the drone to move right (roll).
pluto.right()
```

#### `Yaw Commands`

```python
#Sets the drone to yaw right.
pluto.right_yaw()

#Sets the drone to yaw left.
pluto.left_yaw()
```

#### `Throttle Commands`

Increase/ Decrease the drone's height.

```Python
#Increases the drone's height.
pluto.increase_height()

#Decreases the drone's height.
pluto.decrease_height()
```

#### `Takeoff and Land`

```Python
#Arms the drone and prepares it for takeoff.
pluto.take_off()

#Commands the drone to land.
pluto.land()
```

#### `Developer Mode`

Toggle Developer Mode

```Python
#Turns the Developer mode ON
pluto.DevOn()

#Turns the Developer mode OFF
pluto.DevOff()
```

#### `motor_speed(motor_index, speed)`

Sets the speed of a specific motor (motor index from 0 to 3).

```Python
pluto.motor_speed(0, 1500)
```

#### `Get MSP_ALTITUDE Values`

```python
#Returns the height of the drone from the sensors.
height = pluto.get_height()

#Returns the rate of change of altitude from the sensors.
vario = pluto.get_vario()
```

#### `Get MSP_ALTITUDE Values`

```python
#Returns the roll value from the drone.
roll = pluto.get_roll()

#Returns the pitch value from the drone.
pitch = pluto.get_pitch()

#Returns the yaw value from the drone.
yaw = pluto.get_yaw()
```

#### `Get MSP_RAW_IMU Values`

##### `Accelerometer`

Returns the accelerometer value for the x,y,z - axis.

```python
#Returns the accelerometer value for the x-axis.
acc_x = pluto.get_acc_x()

#Returns the accelerometer value for the y-axis.
acc_y = pluto.get_acc_y()

#Returns the accelerometer value for the z-axis.
acc_z = pluto.get_acc_z()
```

#### `Gyroscope`

Returns the Gyroscope value for the x,y,z - axis.

```python
#Returns the Gyroscope value for the x-axis.
gyro_x = pluto.get_gyro_x()

#Returns the Gyroscope value for the y-axis.
gyro_y = pluto.get_gyro_y()

#Returns the Gyroscope value for the z-axis.
gyro_z = pluto.get_gyro_z()
```

#### `Magnetometer`

Returns the Magntometer value for the x,y,z - axis.

```python
#Returns the Magnetometer value for the x-axis.
mag_x = pluto.get_mag_x()

#Returns the Magnetometer value for the y-axis.
mag_y = pluto.get_mag_y()

#Returns the Magnetometer value for the z-axis.
mag_z = pluto.get_mag_z()
```

#### `Calibration Commands`

```python
#Calibrates the accelerometer.
pluto.calibrate_acceleration()

#Calibrates the magnetometer.
pluto.calibrate_magnetometer()
```

#### `Get MSP_Analog Values`

```python
#Returns the battery value in volts from the drone.
battery = pluto.get_battery()

#Returns the battery percentage from the drone.
battery_percentage = pluto.get_battery_percentage()
```
