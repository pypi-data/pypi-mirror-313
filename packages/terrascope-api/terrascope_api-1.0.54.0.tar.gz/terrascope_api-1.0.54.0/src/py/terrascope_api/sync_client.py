# Copyright 2017-2021 Orbital Insight Inc., all rights reserved.
# Contains confidential and trade secret information.
# Government Users:  Commercial Computer Software - Use governed by
# terms of Orbital Insight commercial license agreement.


# TODO:
# add retry
# handle exceptions
# add custom logic (request_id, ....)

import grpc
from terrascope_api.terrascope_base_api import TerrascopeBaseApi
from terrascope_api import models


class TerrascopeSyncClient:
    def __init__(self, oi_papi_url, port=443, secure=True, api_token=None):
        self.api = TerrascopeSyncApi(oi_papi_url, port, secure, api_token=api_token)
        self.models = models


class TerrascopeSyncApi(TerrascopeBaseApi):

    def _get_channel(self, channel_credentials: grpc.ChannelCredentials):
        token_creds = grpc.access_token_call_credentials(self.api_token)
        creds = grpc.composite_channel_credentials(channel_credentials, token_creds)
        return grpc.secure_channel(f"{self._oi_papi_url}:{self._port}",
                                   creds,
                                   options=self.options,
                                   compression=None)

    def __del__(self):
        self._channel.close()
