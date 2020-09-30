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


class ServerC(RL1_pb2_grpc.MessagePassingServicer):
    def GetServerResponse(self, request, context):
        return RL1_pb2.MessageResponse(textMessage='Hello, %s!' % request.textMessage)


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
