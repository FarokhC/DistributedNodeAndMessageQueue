from concurrent import futures
import logging
import grpc
import RL1_pb2
import RL1_pb2_grpc
import MessageQueue

messageQ = MessageQueue.MessageQueue()

# TODO: Add multithreading to spool up a thread to constantly empty the message queue
# by sending the messages in the queue to ServerC.
class MiddleManB(RL1_pb2_grpc.MessagePassingServicer):
    def PassMessageToServer(self, request, context):
        channel = grpc.insecure_channel('localhost:50052')
        stub = RL1_pb2_grpc.MessagePassingStub(channel)
        print("Middle Man B received: " + request.textMessage)
        messageQ.printQueueContents()
        messageQ.addMessageToEndOfQueue(request.textMessage)
        messageQ.printQueueContents()
        msg = messageQ.popFirstMessageFromQueue()
        messageQ.printQueueContents()
        response = stub.GetServerResponse(RL1_pb2.Message(textMessage=request.textMessage))
        return RL1_pb2.MessageResponse(textMessage=msg)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    RL1_pb2_grpc.add_MessagePassingServicer_to_server(MiddleManB(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Middleman B has started")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
