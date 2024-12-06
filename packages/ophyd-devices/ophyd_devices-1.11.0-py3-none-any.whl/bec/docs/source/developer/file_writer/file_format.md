# File writer plugins
The HDF5 file's internal structure can be customized by implementing file writer plugins. These plugins are Python classes that inherit from the [`DefaultFormat`](/api_reference/_autosummary/bec_server.file_writer.default_writer.DefaultFormat.rst#bec_server.file_writer.default_writer.DefaultFormat) class and override the `format` method. 

````{dropdown} View code: Default format
:icon: code-square
:animate: fade-in-slide-down

```{literalinclude} ../../../../bec_server/bec_server/file_writer/default_writer.py
:language: python
:pyobject: DefaultFormat.format
:dedent: 4
```
````

To simplify the implementation and readability of the file format definition, we provide a helper class [`HDF5Storage`](/api_reference/_autosummary/bec_server.file_writer.file_writer.HDF5Storage.rst#bec_server.file_writer.file_writer.HDF5Storage) that allows for easy access to the HDF5 file structure. The `HDF5Storage` class provides methods to create groups, datasets, links and attributes in the HDF5 file. 

The following example demonstrates how to create a simple file writer plugin that writes a dataset to the HDF5 file. 

````{dropdown} View code: Simple file writer plugin
:icon: code-square
:animate: fade-in-slide-down

```python
from bec_server.file_writer.default_writer import DefaultFormat

class SimpleFormat(DefaultFormat):
    def format(self):
        # create a group "entry" in the HDF5 file
        entry = self.storage.create_group("entry")

        # add an attribute "NX_class" to the group "entry"
        entry.attrs["NX_class"] = "NXentry"

        # within the group "entry", create another group "instrument"
        instrument = entry.create_group("instrument")

        # add an attribute "NX_class" to the group "NXinstrument"
        instrument.attrs["NX_class"] = "NXinstrument"

        # create a dataset "sigma_x" in the group "instrument" with a value of 0.202 and units "mm" 
        sigma_x = source.create_dataset(name="sigma_x", data=0.202)
        sigma_x.attrs["units"] = "mm"

        # create a dataset "sample_translation_x" in the group "instrument" and retrieve the data from the device "samx"
        sample_translation_x = source.create_dataset(name="sample_translation_x", data=self.get_entry("samx))

        # add a group "eiger9m" to the group "instrument", but only if the device "eiger9m" is available
        if (
            "eiger9m" in self.device_manager.devices
            and self.device_manager.devices.eiger9m.enabled
            and "eiger9m" in self.file_references
        ):
            eiger9m = instrument.create_group("eiger9m")
            eiger9m.attrs["NX_class"] = "NXdetector"
            description = eiger9m.create_dataset(
                name="description",
                data="Eiger9M detector, in-house developed, Paul Scherrer Institute",
            )

            # create an external link to the data and status datasets of the Eiger9M detector
            data = eiger9m.create_ext_link("data", file_references["eiger9m"]["path"], "EG9M/data")
            status = eiger9m.create_ext_link(
                "status", file_references["eiger9m"]["path"], "EG9M/status"
            )

```
````

You can save your file writer plugin in the dedicated folder `<plugin_repo_name>/file_writer/<my_file_writer_plugin>.py`. Please note that you need to add it to the `__init__.py` file in the same folder to make it available to the file writer service. Afterwards, you can use the plugin in the BEC file writer service by setting the plugin name in the service configuration. 
