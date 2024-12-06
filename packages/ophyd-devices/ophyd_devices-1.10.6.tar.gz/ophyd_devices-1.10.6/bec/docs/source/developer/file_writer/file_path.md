(developer.file_writer.modifying_file_path)=
# Modifying the file path and name
## Base path
When the service starts, a **base_path** is configured, and all data can only be written to disk relative to this path. By default, the relative path follows the template `/data/S00000-S00999/S00001/S00001_master.h5` for scan number 1. To compile the appropriate path for secondary services, we provide the utility class [`bec_lib.file_utils.FileWriter`](/api_reference/_autosummary/bec_lib.file_utils.FileWriter.rst#bec_lib.file_utils.FileWriter) with the method [`compile_full_filename`](/api_reference/_autosummary/bec_lib.file_utils.FileWriter.rst#bec_lib.file_utils.FileWriter.compile_full_filename), which automatically prepares the correct filepath. 
If secondary services within *ophyd_devices* need to be configured with the appropriate file path, we recommend using this function since it will ensure that all custom changes to the file name and directory will be properly compiled and returned.

## Path and file name configuration
The relative filepath can be configured and adapted dynamically. 
We provide the possibility to change the file directory or add a suffix to the file name through a **system_config**.
Keep in mind that the file_directory will always be considered relative to the **base_path**. Providing an absolute path by accident will be transformed into a relative path. 
In addition, both file_suffix and file_directory may only contain alphanumeric ASCII characters and the following special characters: `-`, `_` and `/`. 
This will be automatically checked, and raise for an invalid input.<br>
To adjust the suffix and directory name to your needs, you may use one of the two options below:

1. **Changing the system_config**

    The `system_config` is accessible via [`bec.system_config`](/api_reference/_autosummary/bec_lib.client.SystemConfig) and can be used to change file_suffix and file_directory. It is directly exposed to users via the client. Changing the `file_suffix` and `file_directory` will be considered for all following scans.
    ```python
    bec.system_config.file_suffix = 'sampleA'
    bec.system_config.file_directory = 'my_dir/my_setup'
    ```
    Assuming the *basepath* to be `'/bec/data'` and a `scannr = 101`, the file writer now writes to the following filepath: `'/bec/data/my_dir/my_setup/S00101_master_sampleA.h5'`.
    If you only provide `file_suffix`, but no additional `file_directory`, the filepath will be:`'/bec/data/S00000-S00999/S00101_sampleA/S00101_master_sampleA.h5'`. 

1.  **Adding additional arguments to a scan**

    You can also add the `file_suffix` and `file_directory` as arguments to the scan command. This will only affect the current scan and will not be considered for following scans. Adding the arguments to the scan command has priority and will override the information provided in *system_config*.
    ```python
    scans.line_scan(dev.samx, -5, 5, steps=1, relative=True, file_suffix='sampleA', file_directory='my_dir/my_setup')
    ```

```{important}
Please keep in mind that changing the file name and writing to different directories will further complicate the development of automated data processing steps and should only be used if necessary. Moreover, the file name should not be used to store metadata. Instead, we recommend using the metadata field in the HDF5 file.
```