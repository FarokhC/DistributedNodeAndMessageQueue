# DistributedNodeAndMessageQueue

## Prerequisites
 
* Install python 3.8

## Install Instructions

* Run the command, `pip3 install grpcio`

* If the command above does not work, try running `pip install grpcio`

* `pip install grpcio-tools`

* If you have made changes to the proto file (RL1.proto), run `python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. RL1.proto` to recompile

## Run the code

* cd into src/

* Start the server first using the command, `python -m cProfile serverC.py > server_output.txt`

* Start the middleman, B, using the command, `python middlemanB.py`

* Next, start the client server using the command, `python -m cProfile clientA.py > client_output.txt`

* You will see that the textMessage specified in clientA.py's code will be passed to middlemanB.py, and printed. The message will then be passed to serverC.py and printed there too.

## Additional Functionality

* You can change the address in clientA.py. Port 50051 will connect to B, and 50052 will connect to C.
