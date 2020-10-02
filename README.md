# Distributed Nodes And Messaging Queue

## Prerequisites
 
* Install python 3.8

## Install Instructions

* Run the command, `pip3 install grpcio`

* If the command above does not work, try running `pip install grpcio`

* `pip install grpcio-tools`

* `pip install memory_profiler`

* If you have made changes to the proto file (RL1.proto), cd into src/, run `python -m grpc_tools.protoc -I./src --python_out=. --grpc_python_out=. RL1.proto` to recompile

## Run the code

* cd into src/

* Start the server first using the command, `python serverC.py`

* Start the middleman, B, using the command, `python middlemanB.py`

* Next, start the client server using the command, `python clientA.py`

* To monitor elapsed time and memory consumption, run clientA.py, `python -m cProfile clientA.py > cprofile_output.txt` and `python -m memory_profiler clientA.py > memory_output.txt`. Open cprofile_output.txt and memory_output.txt to see results.

* You will see that the textMessage specified in clientA.py's code will be passed to middlemanB.py, and printed. The message will then be passed to serverC.py and printed there too.
