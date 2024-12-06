(developer.architecture)= 
# Architecture
BEC is an event-driven system with Redis as the central component for message passing with a service-oriented backend server. The backend server is composed of multiple smaller services that can be deployed independently. The services are connected to Redis and can communicate with each other solely through the message broker.

```{figure} ../../assets/bec_architecture.png
Architecture diagram. BEC relies on a service-oriented backend server with multiple smaller services and Redis as a central message broker and in-memory database. Moreover, any client can be considered as another service to the entire system with access to the same message broker instance. 
```

## Scan Server
The Scan Server acts as the primary interface for user requests, tasked with the choreography of the data acquisition. The primary components are:
* **Scan Guard**: 
The scan guard checks the incoming requests for validity and rejects invalid requests.
* **Scan Assembler**:
The scan assembler assembles the scan instructions from the incoming requests inserts them into the scan queue. Requested scans must be either one of BEC's core scans or a custom scan plugin. 
* **Scan Queue**:
The scan queue holds the scan instructions and is responsible for scheduling the scans. Although by default only the primary queue is set up, separate queues can be added, and their corresponding workers are added and removed automatically. This allows for multiple, independent scan queues if parallel activities are required.
* **Scan Worker**:
The scan worker executes the scan instructions and if necessary publishes device instructions to Redis. While it does not read out the devices, it potentially waits for devices to complete their operations before continuing with the scan.

## Device Server
This service provides a thin layer on top of Bluesky’s Ophyd library to support remote procedure calls (RPC) through Redis. 
It listens to device instructions sent to Redis and performs the specified operations on [Ophyd objects](#developer.ophyd). 
The available Ophyd objects are determined by loading a [device configuration](#developer.ophyd_device_config), typically by loading a YAML file from the command-line interface.
Providing Ophyd objects through a service layer also facilitates sharing access to devices that require a direct socket connection, bypassing the EPICS layer. 

## Scan Bundler
Data streams in a control system are inherently asynchronous. 
Yet, to simplify the user feedback and data analysis, asynchronous readouts are often synchronized afterwards. 
The Scan Bundler creates such synchronization barriers based on metadata entries of the individual readouts (e.g., point IDs or time stamps) and broadcasts these synchronized readings as a new data stream to the BEC system. 

## Filer Writer
Beyond simply writing [HDF5 files](https://portal.hdfgroup.org/hdf5/develop/) with [NeXus](http://www.nexusformat.org)-compatible metadata entries to disk, the file writer also adds external links to the NeXus master file to any other large data file, such as detector files. 
The internal NeXus structure can be adjusted using customizable plugins to comply with a desired NeXus application definition. 

## SciHub connector
A service to connect a BEC instance to external cloud services such as an electronic logbook [SciLog](https://scilog.psi.ch) ([SciLog GitHub](https://github.com/paulscherrerinstitute/scilog)), a data catalogue and archiving solution [SciCat](https://discovery.psi.ch) ( [SciCat project](https://scicatproject.github.io)) and the BEC database. 

## Data Analysis Pipeline
While simple data processing routines such as live data fitting using e.g., [LMfit](https://lmfit.github.io/lmfit-py/), can be performed directly on the server, more computationally expensive operations can be controlled e.g., through [Slurm](https://slurm.schedmd.com) jobs. 
Alternatively, any process with access to Redis can react to live events and trigger analysis pipelines.
Results or metadata thereof can be fed back into the BEC and potentially used to dynamically adjust the data acquisition. 