(developer.scans.scan_metadata)=
# Scan Metadata
During an experiment, it can be quite useful for users to store additional metadata about their scan. We believe that this should be possible for users, potentially dynamically ans as easy as possible. The so-defined user metadata will go to all recorded metadata and therefore also stored on disk. 

To add new metadata for a single scan, you can simply add a metadata dictionary to your scan command.
```python
scans.line_scan(dev.samx,-5,5,steps=100,relative=True, metadata={ 'my_user_metadata' : 'second alignment scan of sample'})
```
This command adds a new key-value pair to the metadata dictionary of the scan, which will also be stored in the HDF5 file. 
If you want to add metadata to all scans, you can also do this by simply adding your metadata to 
```python
bec.metadata = { 'my_user_metadata' : 'second alignment scan of sample'}
```