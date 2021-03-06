from concurrent import futures
import logging
import grpc
import RL1_pb2
import RL1_pb2_grpc
import utilities
import time
from memory_profiler import profile

count = 0
startTime = None
endTime = None
totalTime = None

class ServerC(RL1_pb2_grpc.MessagePassingServicer):
    @profile
    def GetServerResponse(self, request, context):
        global count, startTime, endTime, totalTime
        if(count == 0):
            startTime = time.time()
        receivedMessage = request.textMessage
        print("Server C received message: " + receivedMessage)
        count = count + 1
        if(count == utilities.getNumberOfClients()):
            endTime = time.time()
            totalTime = endTime - startTime
            print("Total Message Transfer Run Time: {} seconds".format(str(totalTime)))
            messagesPerSecond = utilities.getNumberOfClients() / totalTime
            print("Messages per second: " + str(messagesPerSecond))
        return RL1_pb2.MessageResponse(textMessage='ServerC successfully received message: ' + receivedMessage)

@profile
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    RL1_pb2_grpc.add_MessagePassingServicer_to_server(ServerC(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Server Started")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
