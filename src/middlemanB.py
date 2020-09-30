from concurrent import futures
import logging
import grpc
import RL1_pb2
import RL1_pb2_grpc

class MiddleManB(RL1_pb2_grpc.MessagePassingServicer):
    def PassMessageToServer(self, request, context):
        channel = grpc.insecure_channel('localhost:50052')
        stub = RL1_pb2_grpc.MessagePassingStub(channel)
        response = stub.GetServerResponse(RL1_pb2.Message(textMessage=request.textMessage))
        print("Middle Man B received: " + response.textMessage)
        return RL1_pb2.MessageResponse(textMessage='Hello, %s!' % request.textMessage)



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
