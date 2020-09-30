# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging
import grpc
import RL1_pb2
import RL1_pb2_grpc
# import time
# import threading

#inherit the RL1_pb2_grpc messagepassing service 
class ServerC(RL1_pb2_grpc.MessagePassingServicer):
    #how many messages it sends in a certain time 
    # def __init__(self):
    #     self.counter = 0
    #     self.last_print_time = time.time()

    def GetServerResponse(self, request, context):
        # self.counter += 1
        print("Got request from client: " + str(request.testMessage))
        response_message = "Got Request. This is a response message"
        return RL1_pb2.MessageResponse(testResponse=response_message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    RL1_pb2_grpc.add_MessagePassingServicer_to_server(ServerC(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server Started")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
