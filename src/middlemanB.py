from concurrent import futures
import logging
import grpc
import RL1_pb2
import RL1_pb2_grpc
import MessageQueue
from threading import Thread

messageQ = MessageQueue.MessageQueue()
CHANNEL = "channel"
REQUEST = "request"
MESSAGE = "message"

# TODO: Add multithreading to spool up a thread to constantly empty the message queue
# by sending the messages in the queue to ServerC.
class MiddleManB(RL1_pb2_grpc.MessagePassingServicer):
    def PassMessageToServer(self, request, context):
        channel = grpc.insecure_channel('localhost:50052')
        stub = RL1_pb2_grpc.MessagePassingStub(channel)
        print("Middle Man B received: " + request.textMessage)
        messageContents = {
            CHANNEL: channel,
            REQUEST: request,
            MESSAGE: request.textMessage
        }
        messageQ.printQueueContents()
        messageQ.addMessageToEndOfQueue(messageContents)
        messageQ.printQueueContents()
        return RL1_pb2.MessageResponse(textMessage="Node B received message")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    RL1_pb2_grpc.add_MessagePassingServicer_to_server(MiddleManB(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Middleman B has started")
    server.wait_for_termination()

def emptyMessageQueue():
    while(True):
        # print('in loop')
        if(messageQ.getQueueSize() > 0):
            msg = messageQ.popFirstMessageFromQueue()
            stub = RL1_pb2_grpc.MessagePassingStub(msg[CHANNEL])
            messageQ.printQueueContents()
            response = stub.GetServerResponse(RL1_pb2.Message(textMessage=msg[MESSAGE]))
            print("done")
            # return RL1_pb2.MessageResponse(textMessage=msg)

if __name__ == '__main__':
    logging.basicConfig()
    Thread(target=emptyMessageQueue).start()
    Thread(target=serve).start()
