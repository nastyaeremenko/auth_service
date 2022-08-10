from concurrent import futures

# from flask import Flask
import grpc
import jwt
from grpc_interceptor.exceptions import PermissionDenied

from app.main import app
from app.services.user_help import role_and_permission
from grpc_app.config import JWT_SECRET_KEY
from grpc_app.interceptor import ExceptionToStatusInterceptor, \
    UnprocessableEntity
from messages import profile_pb2_grpc, profile_pb2
from jwt import exceptions

class Profile(profile_pb2_grpc.ProfileServicer):

    def GetPermission(self, request, context):
        token = request.token
        try:
            payload = jwt.decode(
                token,
                key=JWT_SECRET_KEY,
                algorithms=['HS256']
            )
        except exceptions.DecodeError:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, 'Error Token')
        except exceptions.ExpiredSignatureError:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'Token Signature Error')
        except exceptions.InvalidSignatureError:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "PERMISSION_DENIED")
        with app.app_context():
            jwt_roles = payload.get('roles')
            roles, permissions = role_and_permission(jwt_roles)
        return profile_pb2.ProfilePermissionResponse(permissions=permissions,
                                                     roles=roles)


if __name__ == '__main__':
    interceptors = [ExceptionToStatusInterceptor()]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         interceptors=interceptors)
    profile_pb2_grpc.add_ProfileServicer_to_server(Profile(), server)
    server.add_insecure_port('[::]:5005')
    server.start()
    server.wait_for_termination()
