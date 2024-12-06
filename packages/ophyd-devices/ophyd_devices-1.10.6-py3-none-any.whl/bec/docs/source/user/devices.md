(user.devices)=
# Devices
BEC without devices is not of much use. 
To inform BEC about your devices, you need to create a device config file.
## Create a new device config

The device config is a yaml file that contains all information about your devices.
If you already have a list of your devices and their config, you can skip the following step and move on to explore how you can - *Load, save and update the config*.

```{note}
The config file is a yaml file. If you are not familiar with yaml, please have a look at the [yaml documentation](https://yaml.org/).
```

But don't worry, we have prepared a device config with simulated devices for you, which allows us to explore BEC right away.

(user.devices.load_demo_config)=
### Load demo device config for simulation
You can load the demo config `demo_config.yaml` directly in the command-line interface via: 

```{code-block} python
bec.config.load_demo_config()
```
Once loaded, the device config will be stored on the running Redis server, and remain intact even after restarting the client or the server.
With the demo config loaded, we can now explore the conventional way of loading a device config into BEC. 

### Export the current device config

To save the current session to disk, use

```{code-block} python
bec.config.save_current_session("./config_saved.yaml")
```
which will save a file `config_saved.yaml` in the directory in which the client is running.
To modify and add a new device to the config, open `config_saved.yaml` with a suitable editor, for instance *VSCode*, and add a new device to the device config. 
For this, you may use the device gauss_bpm which is shown below. 

``` {code-block} yaml
---
name: user.devices.add_gauss_bpm
---

gauss_bpm:
  readoutPriority: monitored
  deviceClass: ophyd_devices.sim.sim_monitor.SimMonitor
  deviceConfig:
    sim_init:
      model: GaussianModel
      params:
        amplitude: 500
        center: 0
        sigma: 1
  deviceTags:
    - beamline
  enabled: true
  readOnly: false
  softwareTrigger: true
```
For more information about various topics linked to Ophyd and the simulation, please also check our developer section of the documentation. In particular, [Ophyd](#developer.ophyd), the [Ophyd device configuration](#developer.ophyd_device_config) and the [simulation framework](#developer.bec_sim).
### Upload a new device config

From the client, you can now run the follow command to update the session with a new device config file.
You can now reload the config from the BEC client.
```{code-block} python
bec.config.update_session_with_file(<my-config.yaml>)
```
In our case, `<my-config.yaml>` could be for example the stored and updated config `config_saved.yaml` from above.
Throughout these steps, you have exported and imported a device config, and in addition also extended the config with a new device.

## Update the device config
We can update the device config from the command line interface. 
This allows us for instance to enable/disable, set limits or store user_parameter (e.g. in/out positions) in the config file that will be hosted, and if wanted, also exported with the device config.  

### Enable / disable a device

To disable a device (e.g. samx), use

```{code-block} python
dev.samx.enabled=False 
```
The device `samx` is now disabled on all services as well as for the BEC database (MongoDB) if connected. 

### Set the readout priority

To change the readout priority of a device (e.g. samx), use

```{code-block} python
dev.samx.readout_priority = "monitored" 
```

Possible values are `monitored`, `baseline`, `on_request`, `async` and `continuous`. More details on the readout priority and the different modes can be found in the [developer guide](#developer.ophyd_device_config).

(user.devices.update_device_config)=
### Update the device config

To update the device config, use

```{code-block}  python
dev.samx.set_device_config({"tolerance":0.02})
```
 which will update the tolerance window for the motor to reach its target position. 
 Keep in mind though, that the parameter exposed through the device_config must be configurable in the [ophyd_device](#developer.ophyd.ophyd_device) of the bespoken device.

### Set or update the user parameters

To set the device's user parameters (such as in/out positions), use

```{code-block}  python
dev.samx.set_user_parameter({"in": 2.6, "out": 0.2})
```

If instead you only want to update the user parameters, use

```{code-block} python
dev.samx.update_user_parameter({"in":2.8})
```

```{hint}
The user parameters can be seen as a python dictionary. Therefore, the above commands are equivalent to updating a python dictionary using

```python
user_parameter = {"in": 2.6, "out": 0.2}    # equivalent to set_user_parameter
print(f"Set user parameter: {user_parameter}")


user_parameter.update({"in": 2.8})          # equivalent to update_user_parameter
print(f"Updated user parameter: {user_parameter}")
```

This will output:

``` 
Set user parameter: {'in': 2.6, 'out': 0.2}
Updated user parameter: {'in': 2.8, 'out': 0.2}
```