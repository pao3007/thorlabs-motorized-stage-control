# thorlabs-motorized-stage-control
Control of motor for Thorlabs motorized stages, LNR502E with optical encoder using BSC201 controller.

![ETN053047-lrg](https://github.com/pao3007/thorlabs-motorized-stage-control/assets/35431691/6f3c447a-a1eb-46bf-b297-05aa61200c16)

Initialize class, we need to know serial number of controller and name of stage.
```python
tbc = ThorlabsBenchtopControl(serial_number, stage_name)
```
To move by some distance we use:
```python
tbc.move_relative(-25.0)
```
To move at some position we use 
```python
tbc.move_absolute(25.0)
```
To read position of optical encoder, you need to know max value of encoder to calculate distance:
```python
enc = tbc.get_optical_encoder_position()
```
Close connection:
```python
tbc.disconnect()
```

If there is error during initialization, most likely you need to turn off, turn on controller.
