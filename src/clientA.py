from __future__ import print_function
import logging
import grpc
import RL1_pb2
import RL1_pb2_grpc
import threading
import time
import utilities

CLIENTS = utilities.getNumberOfClients()
totalCount = 0
threadCount = 0
MAX_THREAD_COUNT = 100
threads = []
threadLimit = threading.Semaphore(MAX_THREAD_COUNT)
address = 'localhost:50051'

# TODO: Create multiple instances of ClientA and have them send
# messages to the message queue all at once. Then have the message
# queue send the data to single instance C

def sendMessage(threadId, address):
    global threadCount, totalCount
    threadLimit.acquire()
    totalCount = totalCount + 1
    threadCount = threadCount + 1
    print("total count: " + str(totalCount))
    print("thread count: " + str(threadCount))
    channel = grpc.insecure_channel(address)
    stub = RL1_pb2_grpc.MessagePassingStub(channel)
    if("50052" in address):
        response = stub.GetServerResponse(RL1_pb2.Message(textMessage="Hello World! " + str(threadId)))
    elif("50051" in address):
        response = stub.PassMessageToServer(RL1_pb2.Message(textMessage="Hello World! " + str(threadId)))
    print("Greeter client received: " + response.textMessage)
    # threadCount = threadCount - 1
    threadLimit.release()
    threadCount = threadCount - 1
    print("thread count: " + str(threadCount))

if __name__ == '__main__':
    startTime = time.time()

    logging.basicConfig()
    threadNum = 0

    #setup threads
    for i in range(CLIENTS):
        thread = threading.Thread(target=sendMessage, args=(threadNum, address,))
        threads.append(thread)
        threadNum = threadNum + 1

    # Start threads
    for x in threads:
        x.start()

    # Wait for all threads to finish
    for x in threads:
        x.join()

    endTime = time.time()
    totalTime = endTime - startTime
    print("Total Client Run Time: {} seconds".format(str(totalTime)))
