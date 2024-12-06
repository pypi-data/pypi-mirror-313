# Copyright 2017-2021 Orbital Insight Inc., all rights reserved.
# Contains confidential and trade secret information.
# Government Users:  Commercial Computer Software - Use governed by
# terms of Orbital Insight commercial license agreement.


import os
from abc import ABC, abstractmethod

import json

import grpc
from terrascope_api import stubs


API_TOKEN = 'TERRASCOPE_API_TOKEN'


class TerrascopeBaseApi(ABC):
    def __init__(self, oi_papi_url, port=443, secure=True, api_token=None, root_certificates_file=None):
        self._oi_papi_url = oi_papi_url
        self._port = port

        self.api_token = os.environ.get(API_TOKEN, "").strip() if api_token is None else api_token.strip()
        self.options = [('grpc.max_send_message_length', -1),
                        ('grpc.max_receive_message_length', -1),
                        ('grpc.max_metadata_size', 16000)]
        service_config_json = json.dumps({
            "methodConfig": [{
                "name": [{}],  # Apply retry to all methods by using [{}]
                "retryPolicy": {
                    "maxAttempts": 5,
                    "initialBackoff": "1.0s",
                    "maxBackoff": "60s",
                    "backoffMultiplier": 2,
                    "retryableStatusCodes": ["UNAVAILABLE"],
                },
            }]
        })
        self.options.append(("grpc.service_config", service_config_json))
        self._channel = self._get_channel(self._get_ssl_channel_credentials(
            secure, root_certificates_file=root_certificates_file))

        # unauthenticated users can access forgot_password
        self.forgot_password = stubs.forgot_password.ForgotPasswordApiStub(self._channel)

        if self.api_token:
            self.algorithm = stubs.algorithm.AlgorithmApiStub(self._channel)
            self.algorithm_version = stubs.algorithm_version.AlgorithmVersionApiStub(self._channel)
            self.algorithm_config = stubs.algorithm_config.AlgorithmConfigApiStub(self._channel)
            self.aoi = stubs.aoi.AOIApiStub(self._channel)
            self.aoi_collection = stubs.aoi_collection.AOICollectionApiStub(self._channel)
            self.aoi_version = stubs.aoi_version.AOIVersionApiStub(self._channel)
            self.aoi_catalog = stubs.aoi_catalog.AOICatalogApiStub(self._channel)
            self.aoi_transaction = stubs.aoi_transaction.AOITransactionApiStub(self._channel)
            self.aoi_export = stubs.aoi_export.AOIExportApiStub(self._channel)
            self.algorithm_computation = stubs.algorithm_computation.AlgorithmComputationApiStub(self._channel)
            self.algorithm_computation_execution = stubs.algorithm_computation_execution.AlgorithmComputationExecutionApiStub(self._channel)
            self.analysis = stubs.analysis.AnalysisApiStub(self._channel)
            self.analysis_version = stubs.analysis_version.AnalysisVersionApiStub(self._channel)
            self.credit = stubs.credit.CreditApiStub(self._channel)
            self.result = stubs.result.ResultApiStub(self._channel)
            self.analysis_config = stubs.analysis_config.AnalysisConfigApiStub(self._channel)
            self.analysis_computation = stubs.analysis_computation.AnalysisComputationApiStub(self._channel)
            self.system = stubs.system.SystemApiStub(self._channel)
            self.toi = stubs.toi.TOIApiStub(self._channel)
            self.permission = stubs.permission.PermissionApiStub(self._channel)
            self.user = stubs.user.UserApiStub(self._channel)
            self.user_collection = stubs.user_collection.UserCollectionApiStub(self._channel)
            self.token = stubs.token.TokenApiStub(self._channel)
            self.visualization = stubs.visualization.VisualizationApiStub(self._channel)
            self.tile = stubs.tile.TileApiStub(self._channel)
            self.imagery = stubs.imagery.ImageryApiStub(self._channel)
            self.notification = stubs.notification.NotificationApiStub(self._channel)
            self.data_source = stubs.data_source.DataSourceAPIStub(self._channel)
            self.data_type = stubs.data_type.DataTypeAPIStub(self._channel)
            self.data_search = stubs.data_search.DataSearchApiStub(self._channel)
            self.data_tracking = stubs.data_tracking.DataTrackingApiStub(self._channel)
            self.project = stubs.project.ProjectApiStub(self._channel)
            self.project_analysis_config = stubs.project_analysis_config.ProjectAnalysisConfigApiStub(self._channel)
            self.project_collaborator = stubs.project_collaborator.ProjectCollaboratorApiStub(self._channel)
            self.project_group = stubs.project_group.ProjectGroupApiStub(self._channel)
            self.project_result = stubs.project_result.ProjectResultApiStub(self._channel)
            self.project_filter = stubs.project_filter.ProjectFilterApiStub(self._channel)
            self.filter = stubs.filter.FilterApiStub(self._channel)
            self.project_aoi = stubs.project_aoi.ProjectAOIApiStub(self._channel)
            self.order = stubs.order.OrderApiStub(self._channel)
            self.order_recommendation = stubs.order_recommendation.OrderRecommendationApiStub(self._channel)
            self.tasking_order = stubs.tasking_order.TaskingOrderApiStub(self._channel)
            self.provider_quotas = stubs.provider_quotas.ProviderQuotasApiStub(self._channel)
            self.resource = stubs.resource.ResourceApiStub(self._channel)

    def _get_ssl_channel_credentials(self, secure, root_certificates_file=None):
        # note: with all defaults, gRPC will search for cert as described here:
        #  https://github.com/grpc/grpc/blob/7a63bd5407d5e14b30f19a5aaf4b6cd1b80f00e1/include/grpc/grpc_security.h#L287
        # for local env, use local_channel_credentials:
        #  https://grpc.github.io/grpc/python/grpc.html#grpc.local_channel_credentials
        if secure:
            root_certificates = None
            if root_certificates_file:
                with open(root_certificates_file, 'rb') as file:
                    root_certificates = file.read()

            return grpc.ssl_channel_credentials(root_certificates=root_certificates,
                                                private_key=None, certificate_chain=None)
        return grpc.local_channel_credentials()

    @abstractmethod
    def _get_channel(self, channel_credentials: grpc.ChannelCredentials):
        ...
