from typing import Any, Callable

import grpc
from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import GrpcException


class ExceptionToStatusInterceptor(ServerInterceptor):
    def intercept(
            self,
            method: Callable,
            request: Any,
            context: grpc.ServicerContext,
            method_name: str,
    ) -> Any:
        """Override this method to implement a custom interceptor.
         You should call method(request, context) to invoke the
         next handler (either the RPC method implementation, or the
         next interceptor in the list).
         Args:
             method: The next interceptor, or method implementation.
             request: The RPC request, as a protobuf message.
             context: The ServicerContext pass by gRPC to the service.
             method_name: A string of the form
                 "/protobuf.package.Service/Method"
         Returns:
             This should generally return the result of
             method(request, context), which is typically the RPC
             method response, as a protobuf message. The interceptor
             is free to modify this in some way, however.
         """
        try:
            return method(request, context)
        except GrpcException as e:
            context.set_code(e.status_code)
            context.set_details(e.details)
            raise

class UnprocessableEntity(GrpcException):

    status_code = grpc.StatusCode.INVALID_ARGUMENT
    details = "Unprocessable Entity"
