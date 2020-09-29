# CMPE275_RL1

## Prerequisites
 
* Install python 3.8

## Install Instructions

* Run the command, `pip3 install grpcio`

* If the command above does not work, try running `pip install grpcio`

* `pip install grpcio-tools`

* `python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. RL1.proto`
