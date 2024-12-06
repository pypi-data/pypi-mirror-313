# Copyright 2017-2021 Orbital Insight Inc., all rights reserved.
# Contains confidential and trade secret information.
# Government Users:  Commercial Computer Software - Use governed by
# terms of Orbital Insight commercial license agreement.


import grpc
from terrascope_api.terrascope_base_api import TerrascopeBaseApi
from terrascope_api import models
from terrascope_api.async_interceptors import (
    ContextInjectorUnaryUnary, ContextInjectorStreamUnary, ContextInjectorUnaryStream, ContextInjectorStreamStream
)


class TerrascopeAsyncClient:
    def __init__(self, oi_papi_url, port=443, secure=True, api_token=None, root_certificates_file=None):
        self.api = TerrascopeAsyncApi(oi_papi_url, port, secure, api_token=api_token,
                                      root_certificates_file=root_certificates_file)
        self.models = models


class TerrascopeAsyncApi(TerrascopeBaseApi):
    def __init__(self, oi_papi_url, port=443, secure=True, api_token=None, root_certificates_file=None):
        self.context_injecting_interceptors = [
            # materialize distributed context from request headers
            ContextInjectorUnaryUnary(), ContextInjectorUnaryStream(),
            ContextInjectorStreamUnary(), ContextInjectorStreamStream()
        ]
        super(TerrascopeAsyncApi, self).__init__(oi_papi_url, port, secure, api_token,
                                                 root_certificates_file)

    def _get_channel(self, channel_credentials: grpc.ChannelCredentials):
        token_creds = grpc.access_token_call_credentials(self.api_token)
        creds = grpc.composite_channel_credentials(channel_credentials, token_creds)
        return grpc.aio.secure_channel(f"{self._oi_papi_url}:{self._port}",
                                       creds,
                                       options=self.options,
                                       compression=None,
                                       interceptors=self.context_injecting_interceptors)

    # TODO: async destructor
    def __adel__(self):
        self._channel.close()
