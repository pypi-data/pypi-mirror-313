(introduction)=
# Introduction

BEC is a **B**eamline **E**xperiment **C**ontrol system that relies on multiple small services for orchestrating and steering the experiment at large research facilities. The usage of small services allows for a more modular system and facilitates the long-term maintainability. 

The system is designed to be deployed at large research facilities where the interoperability with other systems is a key requirement. As shown in the figure below, the system can be connected to other services such as an electronic logbook, a data catalogue / archiving solution or a data processing pipeline. More services can be added easily by using the provided bec library.  

```{figure} ../assets/BEC_context_user_centric.png
```

Multiple users can be connected to the system at the same time while the scan server uses a queue to schedule the requests received from users or other services such as feedback loops from automatic data-processing pipelines. This client-server architecture keeps the system responsive even under heavy load whilst providing the flexibility to adjust for future requirements. 


