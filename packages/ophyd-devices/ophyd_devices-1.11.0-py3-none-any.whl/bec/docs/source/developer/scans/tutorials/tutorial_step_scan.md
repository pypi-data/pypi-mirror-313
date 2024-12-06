# Step Scan
In this tutorial, we will show you how to create a new scan plugin for BEC. We will create a step scan that moves a motor from one position to another in steps and repeats this process a certain number of times. With each iteration, a temperature controller will be set to a new temperature. 

```{note}
For equally spaced steps of the temperature controller, one could simply use the `grid_scan` scan. However, the step scan is a good example to demonstrate the basic structure of a scan plugin.
```

## Step 1: Create a new scan plugin
Let's start by creating a new scan file in the `scans` directory of our plugin repository and name it tutorial_temperature_step_scan.py. We will start by importing the necessary modules and defining the scan class. 

```python
import numpy as np

from bec_lib.device import DeviceBase
from bec_server.scan_server.scans import ScanBase

class TutorialTemperatureStepScan(ScanBase):
    scan_name = "tutorial_temperature_step_scan"
    
```

To make the scan available in BEC, we need to register it in the `__init__.py` file of the `scans` directory. 

```python
from .tutorial_temperature_step_scan import TutorialTemperatureStepScan
```

## Step 2: Define the scan parameters
Next, we will define the scan parameters. In our case, we need to specify the motor, the start and end position, the number of steps, and the temperature values. 

```python
class TutorialTemperatureStepScan(ScanBase):
    scan_name = "tutorial_temperature_step_scan"
    def __init__(
        self,
        motor: DeviceBase,
        start: float,
        end: float,
        steps: int,
        temperature_values: list,
        exp_time: float,
        relative: bool = False,
        **kwargs,
    ):
        self.motor = motor
        self.start = start
        self.end = end
        self.steps = steps
        self.exp_time = exp_time
        self.relative = relative
        self.temperature_values = temperature_values
        super().__init__(exp_time=exp_time, relative=relative, **kwargs)
        self.readout_priority = {"monitored": [self.motor, self.temperature_controller]}

    def update_scan_motors(self):
        self.scan_motors = [self.motor]
```

In the `__init__` method, we store the motor, start, end, steps, temperature values, exposure time, and relative flag. We also call the super constructor to initialize the scan. The `update_scan_motors` method is used to update the scan motors. In our case, we only have one motor, so we set it to the `scan_motors` attribute. Scan motors are automatically elevated to readout priority "monitored". In our case, we want to also monitor the temperature controller. To ensure that the temperature controller is read out, we add it to the `readout_priority` dictionary. 

```{note}
Without modifications to the `readout_priority` dictionary, the temperature controller would only be read out throughout the scan if its default readout priority is set to "monitored", c.f. [device configuration](/developer/devices/device_configuration.md).
```

To make the life of our users easier, let's add a docstring to the scan class:
```python
class TutorialTemperatureStepScan(ScanBase):
    scan_name = "tutorial_temperature_step_scan"
    def __init__(
        self,
        motor: DeviceBase,
        start: float,
        end: float,
        steps: int,
        temperature_controller: DeviceBase,
        temperature_values: list,
        exp_time: float = 0,
        relative: bool = False,
        **kwargs,
    ):
        """
        A step scan that moves a motor from one position to another in steps and repeats this process for each temperature value.

        Args: 
            motor(DeviceBase): The motor to be moved.
            start(float): The start position of the motor.
            end(float): The end position of the motor.
            steps(int): The number of steps.
            temperature_controller(DeviceBase): The temperature controller.
            temperature_values(list): The temperature values.
            exp_time(float): The exposure time.
            relative(bool): If True, the motor will move relative to the current position. Default is False.
            **kwargs: Additional keyword arguments.

        Example:
            >>> scans.tutorial_temperature_step_scan(dev.motor, -5, 5, 10, dev.temperature_controller, [20, 30, 40])

        """
        self.motor = motor
        self.start = start
        self.end = end
        self.steps = steps
        self.exp_time = exp_time
        self.relative = relative
        self.temperature_controller = temperature_controller
        self.temperature_values = temperature_values
        super().__init__(exp_time=exp_time, relative=relative, **kwargs)
        self.readout_priority = {"monitored": [self.motor, self.temperature_controller]}

    def update_scan_motors(self):
        self.scan_motors = [self.motor]
```

## Step 3: Prepare the positions
Before we start the scan, we need to prepare the positions. We will calculate the positions based on the start, end, and number of steps. 

```python
    def prepare_positions(self):
        self.positions = np.linspace(self.start, self.end, self.steps).reshape(-1, 1)
        self.num_pos = len(self.positions) * len(self.temperature_values)
        yield from self._set_position_offset()
```

Positions should be defined as a 2D array of shape (N, M) where N is the number of steps and M is the number of motors. In our case, we only have one motor, so the shape will be (N, 1). Numpy provides a convenient function `linspace` to generate an array of evenly spaced values over a specified interval. The `reshape` function is used to convert the 1D array to a 2D array with one column.

## Step 4: Define the scan logic
Next, we will define the scan logic and implement it in the `scan_core` method. In our case, we will set the temperature controller to a new value for each iteration and move the motor to a new position. Once settled, we will trigger all devices that are configured to receive software triggers and read out all monitored devices. This read operation should be associated with a new scan segment. We will therefore increment the point_id for each iteration. 
To achieve this, we will use the [`set`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.set), [`trigger`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.trigger), and [`read`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.read) scan stubs provided by BEC.


```python 
    def scan_core(self):
        for temp in self.temperature_values:
            yield from self.stubs.set(device=self.temperature_controller, value=temp)
            for pos in self.positions:
                yield from self.stubs.set(device=self.motor, value=pos[0])
                yield from self.stubs.trigger(min_wait=self.exp_time)
                yield from self.stubs.read(group="monitored", point_id=self.point_id)
                self.point_id += 1
```

Your class is now complete and should look like this:

```python
import numpy as np

from bec_lib.device import DeviceBase
from bec_server.scan_server.scans import ScanBase


class TutorialTemperatureStepScan(ScanBase):
    scan_name = "tutorial_temperature_step_scan"

    def __init__(
        self,
        motor: DeviceBase,
        start: float,
        end: float,
        steps: int,
        temperature_controller: DeviceBase,
        temperature_values: list,
        exp_time: float = 0,
        relative: bool = False,
        **kwargs,
    ):
        """
        A step scan that moves a motor from one position to another in steps and repeats this process for each temperature value.

        Args: 
            motor(DeviceBase): The motor to be moved.
            start(float): The start position of the motor.
            end(float): The end position of the motor.
            steps(int): The number of steps.
            temperature_controller(DeviceBase): The temperature controller.
            temperature_values(list): The temperature values.
            exp_time(float): The exposure time.
            relative(bool): If True, the motor will move relative to the current position. Default is False.
            **kwargs: Additional keyword arguments.

        Example:
            >>> scans.tutorial_temperature_step_scan(dev.motor, -5, 5, 10, dev.temperature_controller, [20, 30, 40])
            
        """
        self.motor = motor
        self.start = start
        self.end = end
        self.steps = steps
        self.exp_time = exp_time
        self.relative = relative
        self.temperature_controller = temperature_controller
        self.temperature_values = temperature_values
        super().__init__(exp_time=exp_time, relative=relative, **kwargs)
        self.readout_priority = {"monitored": [self.motor, self.temperature_controller]}

    def update_scan_motors(self):
        self.scan_motors = [self.motor]

    def prepare_positions(self):
        self.positions = np.linspace(self.start, self.end, self.steps).reshape(-1, 1)
        self.num_pos = len(self.positions) * len(self.temperature_values)
        yield from self._set_position_offset()

    def scan_core(self):
        for temp in self.temperature_values:
            yield from self.stubs.set(device=self.temperature_controller, value=temp)
            for pos in self.positions:
                yield from self.stubs.set(device=self.motor, value=pos[0])
                yield from self.stubs.trigger(min_wait=self.exp_time)
                yield from self.stubs.read(group="monitored", point_id=self.point_id)
                self.point_id += 1
```

Once you have saved the file, restart the BEC server and the client. You should now be able to see your new scan showing up as `tutorial_temperature_step_scan` within `scans.<tab>`.

```{note}
For information on how to test your newly written scan plugin, please refer to the [fly scan tutorial](developer.scans.tutorials.fly_scan_cont_line).
```

