import sys

import grpc
from google.protobuf.json_format import MessageToDict

from messages import profile_pb2
from messages import profile_pb2_grpc

if __name__ == '__main__':
    channel = grpc.insecure_channel('localhost:5005')
    stub = profile_pb2_grpc.ProfileStub(channel)
    print(stub)

    try:
        response: profile_pb2.ProfilePermissionRequest = stub.GetPermission(
            profile_pb2.ProfilePermissionRequest(
                # token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjUxNTk5NjQ4LCJqdGkiOiJkMjE0ZDIwOC0xMTQ1LTQwYzgtOWIzMy1jZTM1ZjZlMjU3ZDYiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiOGI1Y2QzYTUtMjE3OS00NDM0LWIwMGMtNzlmZjdkNTMyNzgxIiwibmJmIjoxNjUxNTk5NjQ4LCJleHAiOjE2NTE2MDMyNDgsInNlc3Npb24iOiJhYmNjYTVmMi1iM2U3LTRhMTMtYWZlZC1hYzcwMTQ2NmNiMzMiLCJyb2xlcyI6WyJzdXBlcnVzZXIiXX0.AFhklfrj7UiRDU48jjcC21fiZz_BHd30p6QS5XiWpg4'
                token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjUxOTExNzk2LCJqdGkiOiIxZjhkYTA5OC04ZGU3LTQ2ZTgtOGI2Ny0wNWM4MjAxMmQ3MzEiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiOGZjMDcwNDQtMjI1Ni00M2FmLTllNjUtYmY3ZTE0NjMzNTA2IiwibmJmIjoxNjUxOTExNzk2LCJleHAiOjE2NTE5MTUzOTYsInNlc3Npb24iOiJjMTQ5MWYwYi0yMjc3LTQ4YmItYjIwNC1lNGRlNjBiMmJjYmEiLCJyb2xlcyI6W119.0jTVkGaLeNRRqY73wgJYTbfIssZdeRKWgdNU50-8fnY'
            )
        )
    except grpc._channel._InactiveRpcError as err:
        print(err.code())
        print(err)
    else:
        print(f"Profile access: {MessageToDict(response)}")
