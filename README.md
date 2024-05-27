# thorlabs-motorized-stage-control
Control of motor for Thorlabs motorized stages, LNR502E with optical encoder using BSC201 controller.

![ETN053047-lrg](https://github.com/pao3007/thorlabs-motorized-stage-control/assets/35431691/6f3c447a-a1eb-46bf-b297-05aa61200c16)

Initialize class, we need to know serial number of controller and name of stage.
```python
tbc = ThorlabsStageControl(serial_number='123456', stage_name='LNR502E', polling_rate=100, max_acc=5.0, max_vel=20.0)
```
Controller does not remember its position after turning off, so we need to home it to zero.
```python
tbc.home_motor()
```
To move by some distance we use [mm], (change timeout based on max acceleration and velocity):
```python
tbc.move_relative(distance=-25.0, timeout=5000)
```
DotNet function will wait till move finishes, if it does not finish in time it will raise exception.

To move at some position we use [mm]:
```python
tbc.move_absolute(position=25.0, timeout=5000)
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
