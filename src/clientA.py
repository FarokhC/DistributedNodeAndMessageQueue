from __future__ import print_function
import logging
import grpc
import RL1_pb2
import RL1_pb2_grpc

def sendMessageToServerC():
    channel = grpc.insecure_channel('localhost:50052')
    stub = RL1_pb2_grpc.MessagePassingStub(channel)
    response = stub.GetServerResponse(RL1_pb2.Message(textMessage='you'))
    print("Greeter client received: " + response.textMessage)

def sendMessageToMiddleManB():
    channel = grpc.insecure_channel('localhost:50051')
    stub = RL1_pb2_grpc.MessagePassingStub(channel)
    response = stub.PassMessageToServer(RL1_pb2.Message(textMessage="Hello World!"))
    print("Greeter client received: " + response.textMessage)

if __name__ == '__main__':
    logging.basicConfig()
    sendMessageToMiddleManB()
