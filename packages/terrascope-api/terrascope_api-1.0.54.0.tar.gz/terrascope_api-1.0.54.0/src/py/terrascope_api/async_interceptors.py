import importlib
from typing import Callable, Union

import grpc
from grpc.aio import \
    UnaryUnaryClientInterceptor, \
    UnaryStreamClientInterceptor, \
    StreamUnaryClientInterceptor, \
    StreamStreamClientInterceptor, \
    ClientCallDetails
from grpc.aio._call import \
    UnaryUnaryCall, \
    UnaryStreamCall, \
    StreamUnaryCall, \
    StreamStreamCall

from grpc.aio._typing import RequestType, ResponseIterableType, ResponseType, \
    RequestIterableType

if importlib.util.find_spec('oi_tracing'):
    from oi_tracing import inject_current_span
else:
    def inject_current_span(_headers):
        pass

if importlib.util.find_spec('mercury_client'):
    from mercury_client.context import context_as_dict
else:
    def context_as_dict():
        return {}


def inject_current_context_into_header(client_call_details: ClientCallDetails)\
        -> ClientCallDetails:

    if client_call_details.metadata is None:  # grpc.aio._metadata.Metadata
        client_call_details.metadata = grpc.aio._metadata.Metadata()

    new_headers = context_as_dict()

    inject_current_span(new_headers)
    # inject_current_auth(new_headers)

    for k, v in new_headers.items():
        client_call_details.metadata.add(k, str(v))
    # todo not clear if it is safe to modify or a new copy needs to be made
    #   at this point returning modified original object
    return client_call_details


class ContextInjectorUnaryUnary(UnaryUnaryClientInterceptor):

    async def intercept_unary_unary(
            self, continuation: Callable[[ClientCallDetails, RequestType],
                                         UnaryUnaryCall],
            client_call_details: ClientCallDetails,
            request: RequestType) \
            -> Union[UnaryUnaryCall, ResponseType]:
        new_details = inject_current_context_into_header(client_call_details)
        response = continuation(new_details, request)
        return await response


class ContextInjectorUnaryStream(UnaryStreamClientInterceptor):

    async def intercept_unary_stream(
            self,
            continuation: Callable[[ClientCallDetails, RequestType],
                                   UnaryStreamCall],
            client_call_details: ClientCallDetails,
            request: RequestType) \
            -> Union[ResponseIterableType, UnaryStreamCall]:
        new_details = inject_current_context_into_header(client_call_details)
        response = continuation(new_details, request)
        return await response


class ContextInjectorStreamUnary(StreamUnaryClientInterceptor):

    async def intercept_stream_unary(
            self,
            continuation: Callable[[ClientCallDetails, RequestType],
                                   StreamUnaryCall],
            client_call_details: ClientCallDetails,
            request_iterator: RequestIterableType,
    ) -> StreamUnaryCall:
        new_details = inject_current_context_into_header(client_call_details)
        response = continuation(new_details, request_iterator)
        return await response


class ContextInjectorStreamStream(StreamStreamClientInterceptor):
    async def intercept_stream_stream(
            self,
            continuation: Callable[[ClientCallDetails, RequestType],
                                   StreamStreamCall],
            client_call_details: ClientCallDetails,
            request_iterator: RequestIterableType,
    ) -> Union[ResponseIterableType, StreamStreamCall]:
        new_details = inject_current_context_into_header(client_call_details)
        response = continuation(new_details, request_iterator)
        return await response
