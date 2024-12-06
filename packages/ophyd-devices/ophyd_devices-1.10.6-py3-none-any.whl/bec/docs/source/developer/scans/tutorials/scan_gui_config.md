# Automatic Scan GUI Generation

The gui_config feature is an optional addition for users who want to control their scans using the automatically
generated ScanControl GUI from `bec_widgets`. This configuration helps in organizing scan parameters into specific
groups, making the GUI more user-friendly and intuitive.

## Overview

The `gui_config` attribute in a scan class specifies how the parameters should be grouped in the GUI. This
configuration:

- Requires minimal user input.
- Focuses on grouping parameters into specific categories.
- Uses Pydantic validators to ensure integrity and completeness.

## Step-by-Step Guide

### Step 1: Add `gui_config` Attribute

Add the `gui_config` attribute to your scan class. This attribute is a dictionary where keys represent the group names
and values are lists of parameter names. These groups dictate how the parameters are organized in the GUI.

```python
class FermatSpiralScan(ScanBase):
    scan_name = "fermat_scan"
    required_kwargs = ["step", "relative"]
    gui_config = {
        "Device 1": ["motor1", "start_motor1", "stop_motor1"],
        "Device 2": ["motor2", "start_motor2", "stop_motor2"],
        "Movement Parameters": ["step", "relative"],
        "Acquisition Parameters": ["exp_time", "settling_time", "burst_at_each_point"],
    }
```

### Step 2: Ensure Complete Signatures and Docstrings

Make sure that the signatures of all parameters in your scan class are complete with types and detailed docstrings. This
ensures that Pydantic can validate and process the configuration without errors.

Example of a detailed `__init__` method:

```python
class FermatSpiralScan(ScanBase):
    scan_name = "fermat_scan"
    required_kwargs = ["step", "relative"]
    gui_config = {
        "Device 1": ["motor1", "start_motor1", "stop_motor1"],
        "Device 2": ["motor2", "start_motor2", "stop_motor2"],
        "Movement Parameters": ["step", "relative"],
        "Acquisition Parameters": ["exp_time", "settling_time", "burst_at_each_point"],
    }

    def __init__(
            self,
            motor1: DeviceBase,
            start_motor1: float,
            stop_motor1: float,
            motor2: DeviceBase,
            start_motor2: float,
            stop_motor2: float,
            step: float = 0.1,
            exp_time: float = 0,
            settling_time: float = 0,
            relative: bool = False,
            burst_at_each_point: int = 1,
            spiral_type: float = 0,
            optim_trajectory: Literal["corridor", None] = None,
            **kwargs,
    ):
        """
        A scan following Fermat's spiral.

        Args:
            motor1 (DeviceBase): first motor
            start_motor1 (float): start position motor 1
            stop_motor1 (float): end position motor 1
            motor2 (DeviceBase): second motor
            start_motor2 (float): start position motor 2
            stop_motor2 (float): end position motor 2
            step (float): step size in motor units. Default is 0.1.
            exp_time (float): exposure time in seconds. Default is 0.
            settling_time (float): settling time in seconds. Default is 0.
            relative (bool): if True, the motors will be moved relative to their current position. Default is False.
            burst_at_each_point (int): number of exposures at each point. Default is 1.
            spiral_type (float): type of spiral to use. Default is 0.
            optim_trajectory (str): trajectory optimization method. Default is None. Options are "corridor" and "none".

        Returns:
            ScanReport

        Examples:
            >>> scans.fermat_scan(dev.motor1, -5, 5, dev.motor2, -5, 5, step=0.5, exp_time=0.1, relative=True, optim_trajectory="corridor")
        """
```

Note that you can omit certain parameters from the `gui_config` if they are not required to be displayed in the GUI or
not expose them to the user.

### Step 3: Utilize Pydantic Validators

Pydantic validators are used to enhance the `gui_config` by:

- **Validating the arguments**: Ensuring that each argument specified in the `gui_config` exists within the scan class.
- **Formatting display names**: Creating user-friendly display names for labels based on parameter names.
- **Extracting tooltips**: Deriving tooltips from the first sentence of each parameter's docstring.
- **Retrieving default values**: Obtaining default values for each parameter.

The Pydantic is automatically applied when the `bec-scan-server` starts up, and it will raise an error if
the `gui_config` is incomplete or incorrect.

```{note}
Note that if the signature or docstring of a parameter is incomplete, Pydantic will raise an error during a `bec-scan-server` startup!
```

## Example of a Complete Scan Class with `gui_config`

Here is the complete example of the `FermatSpiralScan` class with the `gui_config` implemented:

````{dropdown} View code: ScanBase class
:icon: code-square
:animate: fade-in-slide-down

```{literalinclude} ../../../../bec_server/bec_server/scan_server/scans.py
:language: python
:pyobject: FermatSpiralScan
```
````

By following these steps, you can easily configure the GUI for your scans, making them more user-friendly and intuitive
for users who want to use the ScanControl GUI from `bec_widgets`.

The resulting GUI will display the parameters in the specified groups, making it easier for users to understand and
interact with the scan settings:

```{figure} ../assets/scan_GUI_example.png
```