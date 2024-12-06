(developer.logging)=
# Logging
Logging is an essential part of BEC. It helps to understand the system's behavior and to debug issues. BEC uses the Python tool loguru to log messages. Loguru is a flexible and powerful logging library that provides a simple and convenient way to log messages. The loguru library is already included in the BEC environment. 

Loguru's output is configured by socalled sinks. A sink is a destination where log messages are written to. BEC uses the following sinks:
- stdout: Writes log messages to the standard output stream, i.e. the terminal.
- file: Writes log messages to a log file.
- redis: Writes log messages to a Redis database.

Depending on globally set log level for a service, log messages of a specific type are forwarded to the sinks. The log level can be set in the launch file of the service and can be set to the following values:  

- TRACE: Detailed information, typically of interest only when diagnosing problems. This is the most detailed log level and also includes the stack trace and thread information.
- DEBUG: Detailed information for diagnosing problems. This is the second most detailed log level, including the thread information.
- INFO: Confirmation that things are working as expected.
- SUCCESS: Information about successful completion of an operation.
- WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. 'disk space low'). The software is still working as expected.
- ERROR: Due to a more serious problem, the software has not been able to perform some function.

Setting the log level to e.g. DEBUG will forward all log messages of type DEBUG, INFO, SUCCESS, WARNING, and ERROR to the sinks. Setting the log level to e.g. INFO will forward all log messages of type INFO, SUCCESS, WARNING, and ERROR to the sinks.

```{warning}
Setting the log level to TRACE or DEBUG can generate a large amount of log messages and can slow down the system. It is recommended to set the log level to INFO or higher in a production environment.
```
```{note}
The log level can be set for each service and even each sink individually. While this is normally not necessary, it can be useful for not flooding the terminal with log messages. To this end, the default log level of the stdout sink of the client is set to SUCCESS while the log level of the file sink is set to INFO.
```

## Usage
Using the logger in BEC is straightforward. The logger is already included in the BEC environment and can be imported via

```python
from bec_lib.logger import bec_logger
logger = bec_logger.logger
```

`logger` can be used to log messages of different types. The following example shows how to log messages of different types:

```python
logger.trace("This is a trace message")
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.success("This is a success message")
logger.warning("This is a warning message")
logger.error("This is an error message")
```

## BEC's log monitor
To monitor the log messages of BEC, BEC provides a log monitor. The log monitor is a cli-based tool that allows you to monitor the log messages of BEC in real-time. The log monitor can be started via

```bash
bec-log-monitor
```

````{note}
If redis is running on a different host or port, you can specify the redis address via the `--redis` flag, e.g. 
```bash
bec-log-monitor --redis my_bec_vm:6379
```
````

The log monitor also allows you to filter log messages by strings or regular expressions. To this end, you can specify the filter via the `--filter` flag, e.g. 

```bash
bec-log-monitor --filter "my_device"
```

Every log message that contains the string `my_device` will be displayed in the log monitor.

## Example: Debugging a device
1. Start the device server with a log level of TRACE. To this end, open the launch file and set the log level to TRACE
    ```python
    bec_logger.level = bec_logger.LOGLEVEL.TRACE
    ```

1. Start the log monitor and filter for the device's name
    ```bash
    bec-log-monitor --filter "my_device"
    ```
    If you only want to receive log messages of the device server, you can also filter for the device server's name
    ```bash
    bec-log-monitor --filter "device_server.*my_device"
    ```
    or even filter to a specific file
    ```bash
    bec-log-monitor --filter "*my_device_communication.py.*"
    ```
1. Start a scan or command that involves the device
1. Analyze the log messages in the log monitor. 
1. Once you have found the issue, set the log level back to INFO or higher to avoid flooding the log monitor with log messages.
    ```python
    bec_logger.level = bec_logger.LOGLEVEL.INFO
    ```


