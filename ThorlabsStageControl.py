import time
import pythonnet
import clr

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.PositionReadoutEncoderCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import *
from Thorlabs.MotionControl.PositionReadoutEncoderCLI import *
from System import Decimal


class ThorlabsStageControl:

    def __init__(self, serial_number, stage_name, polling_rate=100, max_acc=5.0, max_vel=20.0):
        """
        Class for controlling stage, motor.
        :param serial_number: Serial number of the controller.
        :param stage_name: Name of the stage/benchtop.
        :param polling_rate: Polling rate in ms, default 100ms.
        :param max_acc: Max acceleration of motor, default 5.0 ms-2.
        :param max_vel: Max velocity of motor, default 20.0 ms-1.
        """
        """Connects to device manager"""
        self.dmCLI = DeviceManagerCLI
        """Builds list of available devices"""
        self.dmCLI.BuildDeviceList()
        self.serial_no = serial_number  # Replace this line with your device's serial number
        """Creates class for motor control using serial number of controller"""
        self.device = BenchtopStepperMotor.CreateBenchtopStepperMotor(self.serial_no)
        """Connects to the controller"""
        self.device.Connect(self.serial_no)
        self.polling_rate = polling_rate
        time.sleep(0.5)
        """Gets channel at which controller communicates with stage/benchtop"""
        self.channel = self.device.GetChannel(1)
        """Initializes settings in the controller"""
        if not self.channel.IsSettingsInitialized():
            self.channel.WaitForSettingsInitialized(10000)  # 10 second timeout
            assert self.channel.IsSettingsInitialized() is True
        """Starts polling"""
        self.channel.StartPolling(self.polling_rate * 2)
        time.sleep(0.5)
        """Enables device so we can control motor"""
        self.channel.EnableDevice()
        time.sleep(0.5)
        """Some settings to change acceleration, velocity"""
        self.channel_config = self.channel.LoadMotorConfiguration(
            self.serial_no)  # If using BSC203, change serial_no to channel.DeviceID.
        self.chan_settings = self.channel.MotorDeviceSettings

        self.channel.GetSettings(self.chan_settings)
        self.chan_settings.Control.DefAccn = Decimal(max_acc)
        self.chan_settings.Control.DefMaxVel = Decimal(max_vel)
        self.channel.SetSettings(self.chan_settings, False)
        """Needs to have correct stage name or it will most likely malfunction"""
        self.channel_config.DeviceSettingsName = stage_name
        """Update changed configuration"""
        self.channel_config.UpdateCurrentConfiguration()
        time.sleep(0.5)

    def move_relative(self, distance, timeout=10000):
        """
        Move by some distance. If the movement is not completed in time, dotnet function will raise exception.
        :param distance: Distance to move by.
        :param timeout: Timeout to complete the movement, default 10000ms.
        """
        self.channel.SetMoveRelativeDistance(
            Decimal(distance))
        self.channel.MoveRelative(timeout)

    def move_absolute(self, position, timeout=10000):
        """
        Move to some position. If the movement is not completed in time, dotnet function will raise exception.
        :param position: Position to move to.
        :param timeout: Timeout to complete the movement, default 10000ms.
        """
        self.channel.MoveTo(Decimal(position), timeout)

    def home_motor(self, timeout=60000):
        """
        Home motor to zero. If the movement is not completed in time, dotnet function will raise exception.
        :param timeout: Timeout to complete the movement, default 60000ms.
        """
        self.channel.Home(timeout)

    def get_optical_encoder_position(self):
        """Returns value of optical encoder."""
        return self.channel.GetEncoderCounter()

    def disconnect(self):
        """Closes communication with controller"""
        self.channel.StopPolling()
        self.device.Disconnect()


# example
# serial_number = "12345678"
# stage_name = "LNR502E"
# tbc = ThorlabsStageControl(serial_number, stage_name)
# tbc.home_motor()
# tbc.move_absolute(25.0) # moves to 25mm
# # it will wait till move finishes
# enc = tbc.get_optical_encoder_position()
# tbc.move_relative(-25.0)
# tbc.disconnect()
