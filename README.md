# CMPE275_RL1

## Prerequisites
 
* Install python 3.8

## Install Instructions

* Run the command, `pip3 install grpcio`

* If the command above does not work, try running `pip install grpcio`

* `pip install grpcio-tools`

* `python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. RL1.proto`

## Run the code

* cd into src/

* Start the server first using the command, `python server.py`

* Next, start the client server using the command, `python client.py`

* You will recieve a response from the server on the client terminal window
