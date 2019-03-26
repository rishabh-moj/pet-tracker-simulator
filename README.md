# pet-tracker-simulator

This project contains the pet-tracker-simulator and it's various components. The pet tracker simulator provides modules to allow quick and easy simulation of pet tracker device messages e.g. location,device status etc. The underlying device communication protocol is lwm2m protocol.

The simulator internally leverages the nsep simultor. The pet tracker simulator communicates with nsep simulator using rest calls. The nsep simualator further process the rest calls, creates lwm2m objects and pushes it to nsep gateway which is then consume by the pet trakcer mojio platform.

## Getting Started

Pet tracker simulator is implemented as python package - pettrackersimulator.

### Prerequisites

python 3.x

### Installing


```
Give the example
```


### Usage

- Copy the package 'pettrackersimulator' to relevant directory.

- Example snippet 

```

from pettrackersimulator.simulator import Simulator
imeiList = ["1","2"] 
obj = Simulator(imeiList[0]) ### Create simulator object per imei

gps_coordinates = obj.get_gps_coordinates("1080 howe street, vancouver bc")
lat  = gps_coordinates['latitude']
long = gps_coordinates['longitude']

obj.generate_batterylevel(0.0,0.1,10); ### GPS coordinates should be in float

obj.generate_location(10.0,10.0)

```


## Contributing

You can enhance and make changes to the simulator by making in changes and creating pull requests in private. The pull request will be merged to develop after it's reviewed.

## Authors

* **Rishabh Dev Chandna** 

