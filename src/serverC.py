from concurrent import futures
import logging
import grpc
import RL1_pb2
import RL1_pb2_grpc

class ServerC(RL1_pb2_grpc.MessagePassingServicer):
    def GetServerResponse(self, request, context):
        receivedMessage = request.textMessage
        print("Server C received message: " + receivedMessage)
        return RL1_pb2.MessageResponse(textMessage='ServerC successfully received message: ' + receivedMessage)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    RL1_pb2_grpc.add_MessagePassingServicer_to_server(ServerC(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Server Started")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
