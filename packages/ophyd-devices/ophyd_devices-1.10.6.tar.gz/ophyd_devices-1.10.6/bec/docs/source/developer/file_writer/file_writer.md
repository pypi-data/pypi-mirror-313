(developer.file_writer)=
# File Writer
BEC’s file writer is a dedicated service that writes [HDF5](https://www.hdfgroup.org/solutions/hdf5) files to disk. It is highly customizable and facilitates the adoption of community-driven file and data structures, cf. [NeXus application definition](https://manual.nexusformat.org/classes/applications/index.html). Beamline-specific file structures can be implemented through file writer plugins. The file writer can also be used to add external links to files written by other services, such as data backends for large data sources such as 2D detectors. 

The following sections provide an overview of the file writer service and how to customize the file path, file format, and file writer plugins. 

```{seealso}
If you are new to HDF5, we recommend heading over to the [HDF5 documentation](https://www.hdfgroup.org/solutions/hdf5) to get a better understanding of the file format. HDF5 also provides a [getting started guide](https://portal.hdfgroup.org/hdf5/v1_14_4/_getting_started.html) that might be helpful.

For more information on the NeXus format, please refer to the [NeXus documentation](https://manual.nexusformat.org/introduction.html).
```

```{note}
There are various community-developed tools available that can be used to visualize and analyze HDF5 files. The following list is by no means exhaustive, but it provides a good starting point:
- [HDFView](https://www.hdfgroup.org/downloads/hdfview/): Official HDF5 viewer developed by the HDF Group
- [NeXpy](https://nexpy.github.io/nexpy/): Python-based viewer for NeXus files
- [silx view](http://www.silx.org/doc/silx/latest/applications/view.html#silx-view): Python-based viewer for scientific data developed by the European Synchrotron Radiation Facility
- [h5web VSCode extension](https://marketplace.visualstudio.com/items?itemName=h5web.vscode-h5web): Visual Studio Code extension for viewing HDF5 files
```

```{toctree}
---
maxdepth: 1
hidden: true
---
file_path/
file_format/

```




